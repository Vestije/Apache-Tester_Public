!/usr/bin/env python3
import os
from shutil import copyfile
from dir_locate import find_dir

def conf_backup():
    current_dir = os.path.dirname(os.path.realpath(__file__)) #current directory path of backup.py
    dirlist = find_dir().splitlines() #stores output from dir_locate.py to a list
    if dirlist[0].endswith('apache2.conf'):
        copyfile(dirlist[0],current_dir + '/apache2_backup.conf') #copy of apache2.conf
    elif dirlist[0].endswith('httpd.conf'):
        copyfile(dirlist[0],current_dir + '/httpd_backup.conf') #copy of httpd.conf
    for item in dirlist:
        if item.endswith('/conf-enabled/security.conf'):
            copyfile(item,current_dir + '/security_backup.conf') #copy of security.conf

if __name__ == "__main__":
    conf_backup()
