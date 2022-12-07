import os
import scipy.fftpack
import scipy.optimize
import numpy
import time

#For debug only
def PerformanceAnalysis(func):
    def func_wrapper(*args, **kwargs):
        starting_time=time.time()
        flag=func(*args, **kwargs)
        print('time=%f' %(time.time()-starting_time))
        return flag
    return func_wrapper

def ParseStrainFile(path,format_type,ori_obj):
    #Determine readability
    readability=os.access(path,os.R_OK)
    if not readability:
        return

    #Read file
    with open(path,'r') as f:
        if format_type=='a':
            header=ReadHeaderInfo_1(f)
            strain=ReadStrain_1(f,header['channels'])

    #Define interface variable
    sd={'starting_time':header['starting_time'],'sampling':header['sampling'],\
    'channels':header['channels'],'intervals':[]}

    #Data processing
    time_interval=300.0
    points=int(time_interval*header['sampling'])
    total_point_no=len(strain['time'])
    full_interval_no=int(total_point_no/points)
    sd['intervals']=[time_interval*float(n) for n in range(0,full_interval_no)]
    sd['intervals'].append(float(total_point_no)/float(header['sampling']))
    sd['channels']={}
    for n in header['channels']:
        sd['channels'][n]={'frequency':[],'amplitude':[],'mean':[],'phase':[]}
        for m in range(0,full_interval_no):
            discrete_slice=strain[n][m*points:(m+1)*points]
            freq=Frequency(discrete_slice,header['sampling'])
            [amp,phase,mean]=GetCurvePara(discrete_slice,header['sampling'],freq)
            sd['channels'][n]['frequency'].append(freq)
            sd['channels'][n]['amplitude'].append(amp)
            sd['channels'][n]['mean'].append(mean)
            sd['channels'][n]['phase'].append(phase)
        discrete_slice=strain[n][full_interval_no*points:]
        freq=Frequency(discrete_slice,header['sampling'])
        [amp,phase,mean]=GetCurvePara(discrete_slice,header['sampling'],freq)
        sd['channels'][n]['frequency'].append(freq)
        sd['channels'][n]['amplitude'].append(amp)
        sd['channels'][n]['mean'].append(mean)
        sd['channels'][n]['phase'].append(phase)

    #Return to GUI
    if not ori_obj=='unit_test':
        ori_obj.StrainParsingFinishedRedirector(sd)
    else:
        return sd

    '''
    Interface:
    dic['starting_time']=float
       ['sampling']=int
       ['md5']=tuple
       ['intervals']=tuple
       ['channels']=tuple
       ['channel']['channel_name']['freqency']['interval_no']=float
                                  ['amplitude']['interval_no']=float
                                  ['mean']['interval_no']=float
                                  ['phase']['interval_no']=float
    '''

def ReadHeaderInfo_1(f):
    #header['starting_time']
    #      ['sampling']
    #      ['channels']
    header={}
    header['starting_time']=None
    #f.readline()
    line_content=f.readline()
    sampling_str=''
    for n in line_content:
        if n.isdigit():
            sampling_str=sampling_str+n
    header['sampling']=int(sampling_str)
    line_content=f.readline()
    line_elements=line_content.split()
    header['channels']=line_elements[1:]
    return header

#@PerformanceAnalysis
def ReadStrain_1(f,channels):
    #strain['channel name']
    #      ['time']
    strain={}
    strain['time']=[]
    for key in channels:
        strain[key]=[]
    while 1:
        line_content=f.readline()
        line_elements=line_content.split()
        if len(line_elements)==0:
            break
        strain['time'].append(float(line_elements[0]))
        for n in range(0,len(channels)):
            strain[channels[n]].append(float(line_elements[n+1]))
    return strain

def Frequency(discrete,samp_freq):
    #discrete is a tuple of strains
    #samp_freq is a float indicating sampling frequency [Hz]
    value_no=len(discrete)
    value_no_f=float(value_no)
    x=(float(n)/samp_freq for n in range(0,value_no))
    yf=scipy.fftpack.fft(discrete)
    xf=[]
    sample_time=1.0/samp_freq
    for n in range(0,int(value_no/2)):
        xf.append(1.0/(2.0*sample_time)/(value_no_f/2.0)*float(n))
    xf=xf[1:]
    yf2=[]
    for n in range(1,int(value_no/2)):
        yf2.append(2.0/value_no_f*numpy.abs(yf[n]))
    freq=xf[yf2.index(max(yf2))]
    return freq

#@PerformanceAnalysis
def SineFit(discrete,samp_freq,freq):
    point_no=len(discrete)
    time_interval=1.0/float(samp_freq)
    t=numpy.linspace(0.0,time_interval*float(point_no),point_no,endpoint=False)
    ini_amp=(max(discrete)-min(discrete))/2.0
    ini_mean=numpy.mean(discrete)
    w=2.0*numpy.pi*freq
    ini_phase=0.0 #A better initial estimation of phase is to be implemented.

    fit_function=lambda x: x[0]*numpy.sin(w*t+x[1])+x[2]-discrete
    fit_amp,fit_phase,fit_mean=scipy.optimize.leastsq(fit_function,[ini_amp,ini_phase,ini_mean])[0]
    return [fit_amp,fit_phase,fit_mean]

def JumpFilter(discrete,samp_freq,freq,amp,phase,mean):
    point_no=len(discrete)
    time_interval=1.0/float(samp_freq)
    w=2.0*numpy.pi*freq
    t_full=numpy.linspace(0.0,time_interval*float(point_no),point_no,endpoint=False)
    dif=abs(amp*numpy.sin(w*t_full+phase)+mean-discrete)
    avg_dif=numpy.mean(dif)
    threshold=2.0*(2.0**0.5)*avg_dif
    t_filted=[]
    discrete_filted=[]
    for n in range(0,len(t_full)):
        if dif[n]<threshold:
            t_filted.append(t_full[n])
            discrete_filted.append(discrete[n])
    return [t_filted,discrete_filted,avg_dif]

def FiltedSineFit(t_filted,discrete_filted,freq,ini_amp,ini_phase,ini_mean):
    w=2.0*numpy.pi*freq
    t_filted=numpy.array(t_filted)
    fit_function=lambda x: x[0]*numpy.sin(w*t_filted+x[1])+x[2]-discrete_filted
    fit_amp,fit_phase,fit_mean=scipy.optimize.leastsq(fit_function,[ini_amp,ini_phase,ini_mean])[0]
    return [fit_amp,fit_phase,fit_mean]

def Deviation(t_filted,discrete_filted,freq,fit_amp,fit_phase,fit_mean):
    w=2.0*numpy.pi*freq
    t_filted=numpy.array(t_filted)
    dif=abs(fit_amp*numpy.sin(w*t_filted+fit_phase)+fit_mean-discrete_filted)
    new_avg_dif=numpy.mean(dif)
    return new_avg_dif

def GetCurvePara(discrete_slice,sampling,freq):
    [amp_ini,phase_ini,mean_ini]=SineFit(discrete_slice,sampling,freq)
    [t_filted,discrete_filted,avg_dif_ori]=\
    JumpFilter(discrete_slice,sampling,freq,amp_ini,phase_ini,mean_ini)
    [amp_fit,phase_fit,mean_fit]=FiltedSineFit\
    (t_filted,discrete_filted,freq,amp_ini,phase_ini,mean_ini)
    avg_dif_new=Deviation(t_filted,discrete_filted,freq,amp_fit,phase_fit,mean_fit)
    if avg_dif_new<avg_dif_ori:
        return [amp_fit,phase_fit,mean_fit]
    else:
        return [amp_ini,phase_ini,mean_ini]