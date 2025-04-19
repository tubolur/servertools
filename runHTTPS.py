from modules.HTTPSServer import *

WORKINGDIR=os.path.join(os.path.join(os.path.join(os.getenv("HOME"),'dev'),'servertools'));

if not os.path.exists(WORKINGDIR):
        os.mkdir(WORKINGDIR)

UTILS=os.path.join(WORKINGDIR,"utils")

s=HTTPSServer(keyPath=os.path.join(UTILS,"key.pem"),certPath=os.path.join(UTILS,"cert.pem"));
print("Hit ctrl+c to exit");
