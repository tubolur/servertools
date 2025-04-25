import sqlite3
import os
import pathlib
import datetime
import shutil
import datetime
from modules.Utils import *

class table():
    def __init__(self,data,keys):
        self.data=data;
        self.keys=keys;

class Database():
    def __init__(self,path,tableSchemes):
        self.path=path;
        self.log('connecting to database ' + path);
        self.connection = sqlite3.connect(path);
        self.log('db total_changes = ' + str(self.connection.total_changes));
        self.cursor=self.connection.cursor();
        self.fileScanCache=[];
        self.tables=[];

        self.tableSchemes=tableSchemes;
        for table in tableSchemes:
            self.tables.append(table["name"]);

        self.initDb();
       
    def log(self,text,source='SQLDB',severity='INFO',sameline=False):
        logger(text,source=source,severity=severity,sameline=sameline);

    def initDb(self):
        tables=self.getTableList();

        found=False;

        for tableName in self.tables:

            for table in tables:
                if tableName == table[0]:
                    found=True;

            if not found:
                self.log(f"{tableName} table not found, creating...");
                self.createTable(tableName);    
            else:
                self.log(f'table {tableName} found')   
                self.printTable(tableName);    

            if self.readTable(tableName).data == []:
                self.log("Table empty, adding examples")
                tableScheme=self.getTableScheme(tableName);
                for entry in tableScheme["examples"]:
                    self.insertVariableIntoTable(tableName,entry)
                #self.addMessageToBoard("michel","coucou")

            #self.log(self.getColumnNames(tableName))
            #self.printTable(tableName);
        #self.deleteTable(tableName)

    def getColumnNames(self,tableName):
        c = self.cursor;
        requestString="select * from " + tableName;
        c.execute(requestString);
        return [member[0] for member in c.description]
        
    def readAll(self,silent=False):
        tables=self.tables;
        if not silent:self.log('Reading database tables ...');
        tableCounter=0;
        for table in tables:
            if not silent: self.log('  table : '  + table);
            setattr(self,table,self.readTable(table))
            tableCounter+=1;
            #for entry in getattr(self,table).data : self.log(entry);

        if not silent:self.log('Read ' + str(tableCounter) + ' tables');

        if getattr(self,'Information',None) != None and not silent: 
            self.log('database schema version : ' + str(self.Information.data[0]['schemaVersionMajor']) + '.' + str(self.Information.data[0]['schemaVersionMinor']) + '.' + str(self.Information.data[0]['schemaVersionPatch']))

    def getTableList(self):
        cursor=self.cursor;
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        self.log(f"Database tables : {tables}")
        return tables

    def createTable(self,tableName):
        self.log(f"Creating table {tableName}");
        command = ""

        for tableScheme in self.tableSchemes:
            if tableScheme["name"]==tableName:
                self.log(f"Using scheme {tableScheme["scheme"]}")
    
                command=f"CREATE TABLE IF NOT EXISTS {tableName} ( {", ".join(tableScheme["scheme"])} );"

                cursor = self.cursor;
                cursor.execute(command); 
                self.connection.commit();

    def deleteTable(self,tableName):
        self.log(f"Deleting table table {tableName}");
        conn=self.connection;
        cursor=self.cursor;
        cursor.execute(f"DROP TABLE {tableName}")
        
        #Commit your changes in the database
        conn.commit()

        #Closing the connection
        conn.close()

        self.log(f"Table {tableName} dropped... ")

    def readTable(self,tableName):
        cursor=self.cursor;
        #self.connection.execute("PRAGMA table_info");
        #self.log('Database table keys: ' + tableName + ' dump :')
        cursor.execute("PRAGMA table_info({})".format(tableName));
        rows = cursor.fetchall()
        keys=[];
        for row in rows:
            #self.log(row);
            keys.append(row[1])

        tableData=[];

        cursor.execute("SELECT * FROM "+tableName);
        rows = cursor.fetchall()
        

        for row in rows:
            #self.log(row);
            tableEntry={};
            for i,key in enumerate(keys):
                tableEntry |= {key : row[i]} 
            #self.log(row);
            #self.log(tableEntry);
            tableData.append(tableEntry);

        return table(tableData,keys);

    def printTable(self,tableName):
        readTable=self.readTable(tableName);
        self.log(f"reading table {tableName}")
        for r in readTable.data:
            self.log(f"{r}")

    def getTableScheme(self,tableName):
        for scheme in self.tableSchemes:
            if scheme["name"] == tableName:
                return scheme;

        return None
           
    def insertVariableIntoTable(self,table,values):
        tableObj=self.readTable(table);
        try:
            for i,key in enumerate(tableObj.keys[1:]):
                if i == 0: QString="?"
                else : QString +=", ?"

            keysString='('+ ', '.join(tableObj.keys[1:]) + ")"#"(id, name, email, joining_date, salary)"
            keysQString="VALUES (" + QString + ");"
            rqst = "INSERT INTO "+ table +" " +keysString +" " + keysQString;

            sqlite_insert_with_param='"""' + rqst +'"""';

            self.cursor.execute(rqst, values)
            self.connection.commit()
            self.log(table  + ' successfully updated')

            #self.cursor.close()
        except Exception as error:
            printErrors(error)