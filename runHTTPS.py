from modules.HTTPSServer import *

WORKINGDIR=os.path.join(os.path.join(os.path.join(os.getenv("HOME"),'dev'),'servertools'));

if not os.path.exists(WORKINGDIR):
        os.mkdir(WORKINGDIR)

UTILSDIR=os.path.join(WORKINGDIR,"utils")

s=HTTPSServer(keyPath=os.path.join(UTILSDIR,"key.pem"),certPath=os.path.join(UTILSDIR,"cert.pem"));
print("Hit ctrl+c to exit");
