#!/usr/bin/env python3

import os
import re
from dir_locate import find_dir



def search():
    directories = find_dir().split('\n') # ----> run find_dir() to get a list of active directories, split them into a list at each new line
    
    for each_dir in directories:       
        searched_terms = '' # ----> blank variable to add searched lines 
        if 'apache2.conf' in each_dir: # ----> if the string is part of the directory name: run
            conf_file = open(each_dir, "r") # ----> opens the directory and reads ("r") the file
            for line in conf_file: # ----> read each line in the file
                if re.search("main Apache", line):# ----> if searched term (ex. 'main Apache') in the line: return the line
                    #searched_terms += line + '\n' # ----> add all searched lines to a list
        #return searched_terms # ----> list of searched data from the file
                    return(line) # ----> for testing, remove for above lines

        elif 'conf-enable/security.conf' in each_dir: # ----> if the string is part of the directory name: run
            conf_file = open(each_dir, "r") # ----> opens the directory and reads ("r") the file
            for line in conf_file: # ----> read each line in the file
                if re.search("main Apache", line): # ----> if searched term (ex. 'main Apache') in the line: return the line
                    #searched_terms += line + '\n' # ----> add all searched lines to a list
        #return searched_terms # ----> list of searched data from the file
                    return(line) # ----> for testing, remove for above lines

#print(search()) # ----> for testing purposes


