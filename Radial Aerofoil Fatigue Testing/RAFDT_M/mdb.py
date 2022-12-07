import sys
import os

#Program version
version=(0,0,0)

#Major version of the Python running
python_version=sys.version_info.major

#Absolute pathes of the package and program
current_path=os.getcwd()
package_path=os.path.dirname(__file__)

#Default parameters to be read from env.ini
language='ch'