import copy
import os
import io
from html.parser import HTMLParser
from http.server import SimpleHTTPRequestHandler
from modules.Utils import *
from modules.Database import *

class MessageBoardHTTPRequestHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        print(self.path)
        if "mb" in self.path[1:]:

            if "/?" in self.path:

                data=self.parseRequest(self.path);

                print(data)

                if "password" in data.keys():
                    if data["password"] == "pass":  
                        print("password OK");

                        if hasattr(self,"messageBoardApp"):
                            db=self.messageBoardApp.database;     
                            data["username"] = filterUrlCharacters(data["username"]);
                            data["message"] = filterUrlCharacters(data["message"]);           
                            db.insertVariableIntoTable("MESSAGEBOARD",(data["username"],data["message"],dateToTimestamp(datetime.datetime.now())));                         
                            print("message added to database");

                if "userFilter" in data.keys():
                    self.messageBoardApp.messageFilter=self.messageBoardApp.getUserFilter(self.htmlCode,data["userFilter"]);
                    
            if hasattr(self,"htmlCode"):
                self.send_header("Content-type", "text/html")
                self.end_headers();
                self.messageBoardApp.generateHTML();
                htmlCode=f"<!DOCTYPE HTML><html>{self.htmlCode}</html>"
        
        else:
            directoryListingBytes=self.list_directory(os.path.join(os.getcwd(),self.path[1:]))
            wrapper = io.TextIOWrapper(directoryListingBytes, encoding='utf-8')
            htmlCode=wrapper.read();
        
        self.wfile.write(bytes(htmlCode, "utf-8"))

    def log_message(self, format, *args):
        logger(f"{self.client_address[0]} | {str(args)}","HTMLD");
        return   

    def parseRequest(self,request):
        data=request[request.index("/?")+2:]
        outputData={};

        for d in data.split('&'):
            
            variable=d[:d.index("=")]
            value=d[d.index("=")+1:]

            outputData |={variable:value};

        return outputData;

class MessageBoard():

    def __init__(self,databasePath,workingPath,requestHandler=None,htmlBasePath="utils/messageBoard.html",cssPath="utils/style.css"):
        self.log("Init Message Board")
        self.tableScheme={
                "name":'MESSAGEBOARD',
                "scheme":[  
                            "id INTEGER PRIMARY KEY", 
                            "user text NOT NULL", 
                            "message text NOT NULL", 
                            "date DATE" 
                            ],
                "data":[
                        "user",
                        "message",
                        "date"
                        ],
                "examples":[
                    ("michel",'coucou',dateToTimestamp(datetime.datetime.now())),
                    ("grandma",'taste this delicious pie',dateToTimestamp(datetime.datetime.now()))
                ]
            };
        
        self.database=Database(databasePath,tableSchemes=[self.tableScheme]);
        self.workingPath=workingPath;
        self.htmlBasePath=htmlBasePath;
        self.cssPath=cssPath;
        self.requestHandler=requestHandler;
        self.messageFilter="All";

        self.generateHTML();

    def log(self,text,source='MSGBD',severity='INFO',sameline=False):
        logger(text,source=source,severity=severity,sameline=sameline);

    def getHTMLBase(self):

        f = open(self.htmlBasePath, "r")
        return f.read()

    def getCSS(self):
        f = open(self.cssPath, "r")
        return f.read()

    def generateHTML(self,writeFiles=False):
        self.log("Rendering Message Board HTML/CSS files")
        htmlBase=self.getHTMLBase();
        css=self.getCSS();
        htmlBase=htmlBase.replace("<head>",f"<head><style>{css}</style");

        tableData=self.database.readTable(self.tableScheme["name"])
        posts=""
        tableDataReversed=copy.deepcopy(tableData).data;
        tableDataReversed.reverse();

        if self.messageFilter != "All":
            newData=[]
            for data in tableDataReversed:
                if data['user'] == self.messageFilter:
                    newData.append(data)
            tableDataReversed=newData;
            

        for data in tableDataReversed:
            #self.log(data)
            post=   f'                        <p class="post">\n\
                            <div class="date"> {datetime.datetime.fromtimestamp(int(data["date"]))} </div>\n\
                            <div class="userName"><span>By: {data["user"]}</span></div>\n\
                            <div class="body">{data["message"]}</div>\n\
                        </p>\n'
            posts+=post

        html=htmlBase.replace('<p class="reply">',f'<p class="reply">\n{posts}')

        html=self.updateUserFilter(html);
        #for t in html.split("\n"):
        #    self.log(t);
        
        if writeFiles:
            for fileData in [ ["index.html",html], ["style.css",css] ]:

                fileToWrite=open(os.path.join(self.workingPath,fileData[0]),"w");
                fileToWrite.write(fileData[1]);
                fileToWrite.close();
                self.log(f'file {fileData[0]} written');
        
        if self.requestHandler != None:
            self.requestHandler.htmlCode=html;
            self.requestHandler.messageBoardApp=self;

        #self.log("Rendering HTML/CSS ended");

    def updateUserFilter(self,html):
        firstEntry='<option value=0>All</option>'
        htmlCode='';
        htmlCode+=firstEntry;
        users=["All"]

        for messageIndex,message in enumerate(self.database.readTable("MESSAGEBOARD").data):

            if message['user'] not in users and len(users)<100:
                users.append(message['user'])
                htmlCode+=f"\n<option value={len(users)-1}>{message['user']}</option>"

        return html.replace(firstEntry,htmlCode);

    def getUserFilter(self,html,filterIndex):
        htmlToFind=f'<option value={filterIndex}>';
        html[html.index(htmlToFind):]
        userFilter=html[html.index(htmlToFind)+len(htmlToFind):html.index(htmlToFind)+html[html.index(htmlToFind):].index("</option>")]

        if len(userFilter)>0 and len(userFilter)<200:
            return userFilter;
        else:
            return "All";
