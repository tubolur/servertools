import os
from modules.MessageBoard import *
from modules.HTTPSServer import *

os.system('cls' if os.name == 'nt' else 'clear')

WORKINGDIR=os.path.join(os.path.join(os.path.join(os.getenv("HOME"),'dev'),'servertools'));

if not os.path.exists(WORKINGDIR):
        os.mkdir(WORKINGDIR)

UTILSDIR=os.path.join(WORKINGDIR,"utils")

rh=MessageBoardHTTPRequestHandler;
mb=MessageBoard(
                databasePath=os.path.join(UTILSDIR,"database.db"),
                workingPath=os.path.join(WORKINGDIR,"mb"),
                requestHandler=rh
                htmlBasePath=os.path.join(UTILSDIR,"messageBoard.html"),
                cssPath=os.path.join(UTILSDIR,"style.css")
               );#,requestHandler=rh

s=HTTPSServer(keyPath=os.path.join(UTILSDIR,"key.pem"),certPath=os.path.join(UTILSDIR,"cert.pem"),requestHandler=rh);#,requestHandler=rh
print("Hit ctrl+c to exit");
