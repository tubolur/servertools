from dnserver import DNSServer
from modules.Utils import *

class DNSServer():
    def __init__(self,zones='utils/example_zones.toml',port=5053):
        self.log("Init DNS Server")
        self.zones=zones;
        self.port=port;
        self.server=None;
        self.thread=None;

    def log(self,message,severity="INFO"):
        logger(source="DNSSV",msg=message,severity=severity);

    def run(self):

        self.log(f"Starting DNS Server from {self.zones} on port {self.port}")

        server = DNSServer.from_toml(self.zones, port=self.port)
        
        self.server=server;
        self.thread = threading.Thread(target=server.start(), args=());
        self.thread.setDaemon(True);
        try:
            self.log(f"DNS Server active")
            self.thread.start();
        except Exception as error:
            printErrors(error);
            
        # now you can do some requests with your favorite dns library

    def stop(self):
        if self.thread != None:
            self.thread.join();
            self.server.stop();