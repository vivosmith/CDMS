import os
import sys
from sys import platform
path=os.path.dirname(os.path.realpath(__file__))
if platform!=="win32":
   os.system('sudo python3'+' '+path+'/getpip.py')
   os.system('sudo python3'+' '+path+'/initialize.py')
   os.system('sudo pip3 install pillow')
   os.system('sudo pip3 install mechanicalsoup')
   os.system('sudo pip3 install python3-tk')
else:
   os.system('python3'+' '+path+'/getpip.py')
   os.system('python3'+' '+path+'/initialize.py')
   os.system('pip3 install pillow')
   os.system('pip3 install mechanicalsoup')
   os.system('pip3 install python3-tk')