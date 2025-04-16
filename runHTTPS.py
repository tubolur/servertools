from modules.HTTPSServer import *
UTILS=os.path.join(os.path.abspath(__file__),"utils")
s=HTTPSServer(keyFile=os.path.join(UTILS,"key.pem"),certFile=os.path.join(UTILS,"cert.pem"));
print("Hit ctrl+c to exit");
