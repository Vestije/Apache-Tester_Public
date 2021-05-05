#!/usr/bin/env python3

import requests
import os
import subprocess

def strip_ver(version_string):
    output = ''
    for ch in version_string:
        if ch.isdigit():
            output += ch
        elif ch == '.':
            output += ch
    return ch

def get_installed_ver():
    
### ADD IF STATEMENT THAT PULLS HTTP OR APACHE2 .CONF FILE TO TELL TO RUN PROCESS1 OR PROCESS2 ###
    
    version_info = ''

    #process1 = os.popen('apache2 -v') # ----> os version; run the terminal command and print 
    #process2 = os.popen('httpd -v') # ----> os version; run the terminal command and print 

    #apache_output = process1.readlines() # ----> os version; read output from process1, return lines
    #httpd_output = process2.readlines() # ----> os version; read output from process1, return lines

    process1 = subprocess.run(['apache2', '-v'], capture_output=True) # ----> subprocess version; run the subprocess, capture output
    #process2 = subprocess.run(['httpd', '-v'], capture_output=True) # ----> subprocess version; run the subprocess, capture output

    apache_output = process1.stdout.decode() # ----> subprocess version; print standard output and decode from bytes
    #httpd_output = process2.stdout.decode() # ----> subprocess version; print standard output and decode from bytes
    
    list_apache_output = apache_output.split('\n')

    for line in list_apache_output:
        if 'version' in line:
            version_info += line
        return(strip_version(version_info))
    
def compare_versions():
    if current_ver() == get_installed_ver():
        return True
    else:
        return False

def current_ver():
    process1 = requests.get('https://downloads.apache.org/httpd/')
    webtext = process1.text

    return((webtext.split('IS-'))[1].split('\"')[0])

if __name__ == "__main__":
    print(current_ver())
