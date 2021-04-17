#!/usr/bin/env python3
import os.path
from os import path
from shutil import copyfile
from dir_locate import find_dir

def conf_backup():
    current_dir = os.path.dirname(os.path.realpath(__file__)) #current directory path of backup.py    
    dirlist = find_dir().splitlines() #stores output from dir_locate.py to a list
    if dirlist[0].endswith('apache2.conf'):
        if path.exists( current_dir + '/apache2.original.back') == False: #checks if apache2.original.back exists
            copyfile(dirlist[0],current_dir + '/apache2.original.back') #copy of apache2.conf
        elif path.exists( current_dir + '/apache2.original.back') == True: #checks if apache2.original.back exists
            copyfile(dirlist[0],current_dir + '/apache2.updated.back') #copy of apache2.conf
    elif dirlist[0].endswith('httpd.conf'):
        if path.exists( current_dir + '/httpd.original.back') == False: #checks if httpd.original.back exists
            copyfile(dirlist[0],current_dir + '/httpd.original.back') #copy of httpd.conf
        elif path.exists( current_dir + '/httpd.original.back') == True: #checks if httpd.original.back exists
            copyfile(dirlist[0],current_dir + '/httpd.updated.back') #copy of httpd.conf
    for item in dirlist:
        if item.endswith('/conf-enabled/security.conf'):
            if path.exists( current_dir + '/security.original.back') == False:  #checks if security.original.back exists
                copyfile(item,current_dir + '/security.original.back') #copy of security.conf
            elif path.exists( current_dir + '/security.original.back') == True:  #checks if security.original.back exists
                copyfile(item,current_dir + '/security.updated.back') #copy of security.conf

if __name__ == "__main__":
    conf_backup()
