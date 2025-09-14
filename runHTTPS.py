from modules.HTTPSServer import *
import sys


WORKINGDIR=os.path.join(os.path.join(os.path.join(os.getenv("HOME"),'dev'),'servertools'));

if not os.path.exists(WORKINGDIR):
        os.mkdir(WORKINGDIR)

if len(sys.argv)>1:
        UTILSDIR=sys.argv[1];
else:
        UTILSDIR=os.path.join(WORKINGDIR,"utils")

s=HTTPSServer(keyPath=os.path.join(UTILSDIR,"key.pem"),certPath=os.path.join(UTILSDIR,"cert.pem"));
print("Hit ctrl+c to exit");
