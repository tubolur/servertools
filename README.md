# Servertools

This repo includes few programs to be ran on servers

## Install

run `python3 -m venv venv && source venv/bin/activate && pip install -r utils/requirements.txt`

## HTTPS Server

use  `source venv/bin/activate && python runHTTPSServer.py` . 
It will share the current directory over HTTPS. 
You can share any current dir but you'll have to use absolute path to venv and python file.

Note that the certificate is self signed but has to include the domain name innit. 

To add the certificate to the trusted ones:
 - With Firefox load the page using https://yourdomain:4443, accept exception, click on the lock next to the url and display certificate
 - a webpage should open, look for **Download** and click PEM(cert). It should download the certificate
 - add the certificate to trusted, on archlinux using `sudo trust anchor --store certificateFile.pem`

## MessageBoard

use  `source venv/bin/activate && python runMessageBoard.py` 
the url will be on URL/mb
