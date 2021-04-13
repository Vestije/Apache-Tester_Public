#!/usr/bin/env python3
import os
from shutil import copyfile
from dir_locate import find_dir

def conf_backup():
    current_dir = os.path.dirname(os.path.realpath(__file__)) #current directory path
    dirlist = find_dir().splitlines() #list from output of dir_locate
    copyfile(dirlist[0],current_dir + '/apache2_backup.conf') #copy of apache2.conf
    copyfile(dirlist[1],current_dir + '/security_backup.conf') #copy of security.conf

if __name__ == "__main__":
    conf_backup()
