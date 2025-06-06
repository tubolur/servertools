from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl
import os
import socket
from modules.Utils import *

class HTTPServerV6(HTTPServer):
    address_family = socket.AF_INET6;

class HTTPSServer():
    def __init__(self,keyPath="utils/server.pem",certPath="utils/cert.pem",port=4443,address="",requestHandler=SimpleHTTPRequestHandler):
        self.keyPath=keyPath;
        self.certPath=certPath;
        self.address=address;
        self.port=port;
        self.requestHandler=requestHandler;
        
        if not os.path.exists(self.keyPath) or not os.path.exists(self.certPath):
            self.createCertificate();

        self.daemon=self.run();

    def log(self,message,severity="INFO"):
        logger(source="HTTPS",msg=message,severity=severity);

    def createCertificate(self):

        self.log(f"Creating key {self.keyPath} cert {self.certPath}");
  
        os.system(f"openssl req -x509 -newkey rsa:2048 -keyout {self.keyPath} -out {self.certPath} -days 365");

    def run(self):
        if os.path.exists(self.keyPath) and os.path.exists(self.certPath):

            self.log(f"Starting server on {self.address} port {self.port}");
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER);
            context.load_cert_chain(certfile=self.certPath, keyfile=self.keyPath);
            context.check_hostname = False;

            httpd=HTTPServerV6((self.address, self.port), self.requestHandler);
            httpd.socket = context.wrap_socket(httpd.socket, server_side=True);
            self.log("Server Running");
            httpd.serve_forever();
            return httpd;

        else:
            self.log("Error cert or key not found");
            return None;