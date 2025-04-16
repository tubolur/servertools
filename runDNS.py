from modules.DNSServer import *

s=DNSServer();
s.run();
print("Hit ctrl+c to exit");
s.stop();