#!/usr/bin/env python3

import os
import os.path

def find_dir():
    found_directories = "" # ----> blank variable to add found directories too
    for dirpath, dirnames, filenames in os.walk("/"): # ----> use os.walk to look through each directory
        for filename in [f for f in filenames if f.endswith("apache2.conf" or "httpd.conf")]: # ----> search through directories to find specific file names
            found_directories += os.path.join(dirpath, filename) + '\n' # ----> add found files to a string
        for filename in [f for f in filenames if f.endswith("security.conf")]: # ----> search through directories to find specific file names
            found_directories += os.path.join(dirpath, filename) + '\n' # ----> add found files to a string
    return (found_directories) # ----> return the finalized string with all directories found on the machine that meet the criteria


if __name__ == "__main__":
    print(find_dir())

