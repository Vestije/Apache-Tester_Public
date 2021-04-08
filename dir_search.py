#!/usr/bin/env python3

import os
import re
from dir_locate import find_dir

def setting_valid(line, rec_dict, setting,correct, incorrect):
    line = line.split(' ') #If line is a setting split line using on the space
    if line[0] == setting: #Check if 1st element (the Setting) is equal to the setting passed in as the variable to check
        if rec_dict[setting] == line[1].strip(): #If it is the correct setting check if the value matches the recommended
            correct.append(str.format('{0} is set to: {1}',setting.ljust(18),rec_dict[setting].rjust(5))) #If it does append to correct list

        else: #It doesn't match the recommended setting - append to incorrect list.
            incorrect.append(str.format('{0} is set to : {1}, the recommended setting is: {2}', setting.ljust(22),line[1].strip().rjust(3),rec_dict[setting].rjust(5)))

            
def search(rec_dict, correct, incorrect):
    directories = find_dir().split('\n') # ----> run find_dir() to get a list of active directories, split them into a list at each new line
    
    for each_dir in directories:       
        searched_terms = '' # ----> blank variable to add searched lines 
        if 'apache2.conf' in each_dir: # ----> if the string is part of the directory name: run
            conf_file = open(each_dir, "r") # ----> opens the directory and reads ("r") the file
            for line in conf_file: # ----> read each line in the file
                if line[0] != '#' and line[0] != '\n':
                    for setting in rec_dict.keys():
                        if re.search(setting, line):# ----> if searched term (ex. 'main Apache') in the line: return the line
                            setting_valid(line, rec_dict, setting, correct, incorrect)
                    #searched_terms += line + '\n' # ----> add all searched lines to a list
        #return searched_terms # ----> list of searched data from the file

        elif 'conf-enabled/security.conf' in each_dir: # ----> if the string is part of the directory name: run
            conf_file = open(each_dir, "r") # ----> opens the directory and reads ("r") the file
            for line in conf_file: # ----> read each line in the file
                if line[0] != '#' and line[0] != '\n':
                    for setting in rec_dict.keys():
                        if re.search(setting, line): # ----> if searched term (ex. 'main Apache') in the line: return the line
                            setting_valid(line, rec_dict, setting, correct, incorrect)
                    #searched_terms += line + '\n' # ----> add all searched lines to a list
        #return searched_terms # ----> list of searched data from the file

#if __name__ == "__main__":
    #print(search())


