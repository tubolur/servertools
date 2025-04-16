import datetime
import os
import configparser
from print_color import print as printc
import traceback

WORKINGDIR=os.path.join(os.path.join(os.path.join(os.getenv("HOME"),'dev'),'servertools'));

def strtobool (val):
        val = val.lower()
        if val in ('y', 'yes', 't', 'true', 'on', '1'):
            return True
        elif val in ('n', 'no', 'f', 'false', 'off', '0'):
            return False
        else:
            error=True;
            return None;

def logger(msg,source='NONE',severity='INFO',sameline=False,logFilePath=os.path.join(WORKINGDIR,"log.txt")):  
    
    log_to_file=True;
    log_file=logFilePath;
    debug=True;
    maxMessageLength=2000;
    truncateMessages=False;

    dateStr=str(datetime.datetime.now() );
    sourceStr=' [ ' + source + ' ] ' ;
    severityStr='[ ' + severity + ' ] ' ;
    severityStr="";
    messageColor="white";

    if severity == "ERROR":
        messageColor="red";
    elif severity == "SUCCESS":
        messageColor="green";
    elif  severity =="WARNING":
        messageColor='yellow';
    elif severity=="INFO":
        messageColor='white'

    if not isinstance(msg,str):
        msg=str(msg);
  
    message= dateStr + sourceStr + severityStr + msg

    if len(message) > maxMessageLength and truncateMessages:
        message = message[:maxMessageLength] + " (MESSAGE TRUNCATED)";

    if (severity == "INFO" and debug) or severity == "MAJOR" or severity == "ERROR" or severity == "SUCCESS" or severity == "WARNING":
        if sameline:
            printc (message,color=messageColor,end = '',format="bold")
        else:
            printc (message,color=messageColor,format="bold")

    if log_to_file :
            f = open(log_file, "a")  # append mode
            f.write(message + "\n")
            f.close()

def printErrors(error,module="UTILS"):
    logger("EXCEPTION " + str(type(error).__name__) + " " + str(error) ,module,severity="ERROR");
    stack = traceback.extract_stack()[:-3] + traceback.extract_tb(error.__traceback__);  # add limit=?? 
    for i,l in enumerate(stack):
        logger(str(stack[len(stack)-1-i]),module,severity="ERROR") # An error occurred: NameError – name 'x' is not defined

def readConfigFile(path):
    config = configparser.ConfigParser()
    config.read(path)

    return config

def getConfigFileParameter(path,sectionName,parameterName):

    config=readConfigFile(path);
    
    if sectionName in config.sections():
        if parameterName in config[sectionName]:
            return config[sectionName][parameterName];
        else:
            logger("Parameter " + parameterName +  " not in " + path +" in section "  + sectionName,"CONFIGF")

    else:
        logger("Section not in " + path +" : "  + sectionName,"CONFIGF")

    return None
