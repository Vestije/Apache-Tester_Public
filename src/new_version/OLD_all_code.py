#!/usr/bin/env python3

import requests
import re
import time
import fileinput
import subprocess

import os
from os import system
import os.path


def current_ver():
    process1 = requests.get('https://mirror.jframeworks.com/apache//httpd/')
    webtext = process1.text

    return((webtext.split('IS-'))[1].split('\"')[0])


def setting_valid(line, rec_dict, setting,correct, incorrect):
    if setting == 'Serverversion':    
        line = line.replace('Server version', 'Serverversion')    
        line = line.split(':')
    else:
        line = line.split(' ') #If line is a setting split line using on the space
    
    if line[0] == setting: #Check if 1st element (the Setting) is equal to the setting passed in as the variable to check
        if rec_dict[setting] == line[1].strip(): #If it is the correct setting check if the value matches the recommended
            correct.append(str.format('{0} is set to:{1}',setting.ljust(18),rec_dict[setting].rjust(25))) #If it does append to correct list

        else: #It doesn't match the recommended setting - append to incorrect list.
            incorrect.append(str.format('{0} is set to :{1}, the recommended setting is: {2}', setting.ljust(22),line[1].strip().rjust(25),rec_dict[setting].rjust(25)))


def get_settings(): #from Get_recommendation.py
    with open('recommended_settings.txt') as f:
        lines = f.readlines()
    settings_dict = {}
    for line in lines:
        setting = line.split(':')
        settings_dict[setting[0]] = setting[1].strip()
    return settings_dict


def find_dir():
    found_directories = "" # ----> blank variable to add found directories too
    for dirpath, dirnames, filenames in os.walk("/"): # ----> use os.walk to look through each directory
        for filename in [f for f in filenames if f.endswith("apache2.conf" or "httpd.conf")]: # ----> search through directories to find specific file names
            found_directories += os.path.join(dirpath, filename) + '\n' # ----> add found files to a string
        for filename in [f for f in filenames if f.endswith("security.conf")]: # ----> search through directories to find specific file names
            found_directories += os.path.join(dirpath, filename) + '\n' # ----> add found files to a string
    return (found_directories) # ----> return the finalized string with all directories found on the machine that meet the criteria    
         
def get_ver():
    
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
        return(version_info)


def search(rec_dict, correct, incorrect):
    directories = find_dir().split('\n') # ----> run find_dir() to get a list of active directories, split them into a list at each new line
    setting_valid(get_ver(), rec_dict, 'Serverversion', correct, incorrect)
    for each_dir in directories:  
        searched_terms = '' # ----> blank variable to add searched lines 
        if 'apache2.conf' in each_dir: # ----> if the string is part of the directory name: run
            conf_file = open(each_dir, "r") # ----> opens the directory and reads ("r") the file
            for line in conf_file: # ----> read each line in the file
                if line[0] != '#' and line[0] != '\n':
                    for setting in rec_dict.keys():
                        if re.search(setting, line):# ----> if searched term (ex. 'main Apache') in the line: return the line
                            setting_valid(line, rec_dict, setting, correct, incorrect)


        elif 'conf-enabled/security.conf' in each_dir: # ----> if the string is part of the directory name: run
            conf_file = open(each_dir, "r") # ----> opens the directory and reads ("r") the file
            for line in conf_file: # ----> read each line in the file
                if line[0] != '#' and line[0] != '\n':
                    for setting in rec_dict.keys():
                        if re.search(setting, line): # ----> if searched term (ex. 'main Apache') in the line: return the line
                            setting_valid(line, rec_dict, setting, correct, incorrect)

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

#def user_input():
    # answer_yes = ['yes','Yes','YES','y','Y'] #list all possible inputs for yes
    # answer_no = ['no','No','NO','n','N'] #list all possible inputs for no
    # #choice = input('Would you like to set this option for optimal security? <y/n>\n') #statement placed in choice variable 

    # if choice in answer_yes:
    #     #return({1}) # ----> return int 1 for yes
    #     return('awesome!')
    # elif choice in answer_no:
    #     #return({0}) # ----> return int 0 for no
    #     return('maybe next time...')
    # else:
    #     #return({0}) # ----> return int 0 for no
    #     return('incorrect action, we will skip this for now.')

def print_list(theList):
    for line in theList: #Loop through the list
        print('{: ^100}'.format(line)) #Print each line

def report(correct, incorrect):
    #Print the settings that are set to recommended settings
    print('{: ^100}'.format('The following settings are set to the recommended setting:'))
    print('\n')
    if not correct: #if the list is empty
        print('{: ^100}'.format('--NONE--\n')) #Print no settings are set to recommended settings

    else: #Print the list
        print_list(correct) #Print Correct list
        print('\n'*2) #Print a new line after all the lines in the list

    #Print the settings that are not set to the recommended setting
    print('{: ^100}'.format('The following settings are not set to the recommended setting:'))
    print('\n')
    if not incorrect: #If the list is empty
        print('{: ^100}'.format('--NONE--\n')) #Print no settings are set incorrectly.
    else: #Print the list
        print_list(incorrect) #Print Incorrect list
        print('\n'*5)

def final_output():
    system('clear') #Clear the screen
    l=6 # length for progress_bar

    print('*'*100)	
    print('{:*^100}'.format(' ╔═╗╔═╗╔═╗╔═╗╦ ╦╔═╗   ╔╦╗╔═╗╔═╗╔╦╗╔═╗╦═╗ '))
    print('{:*^100}'.format(' ╠═╣╠═╝╠═╣║  ╠═╣║╣     ║ ║╣ ╚═╗ ║ ║╣ ╠╦╝ '))
    print('{:*^100}'.format(' ╩ ╩╩  ╩ ╩╚═╝╩ ╩╚═╝    ╩ ╚═╝╚═╝ ╩ ╚═╝╩╚═ '))
  
    #*************************************************************************
    #**** The following 3 lines just print the Apache Tester ASCII art in ****
    #**** the center of the terminal console window.  Remove the # before ****
    #**** each line to print them and comment out the three above instead ****
    #*************************************************************************
    print('*'*100)
    print('\n'* 2)
    
    #Declare variables 
    settings = get_settings() #Gets the recommended settings from the Recommended_Settings.txt file
    correct_settings = [] #List to hold all the settings that are set to the recommended setting
    incorrect_settings = [] #List to hold all the settings that are not set to the recommended setting
    #Check Settings and add to appropiate list
    search(settings, correct_settings, incorrect_settings)
    #Print a report
    report(correct_settings, incorrect_settings)
    
    #print(f'\n{get_ver()}')
    #print(f'\nYour files are located in:\n{find_dir()}')
    ### no code yet for search() ###

#def replace_text():
    # replace_texts = {'javascript': 'Java', 'php': 'python'}
    # # makes a dictionary 'replace_texts'= {'search_text': 'replace_text'}

    # for line in fileinput.input('test.txt', inplace = True):
    #     #test.txt is the file i tried this on, placed the words "javascript" and "php" randomly in file
    #     for search_text in replace_texts:
    #         replace_text = replace_texts[search_text]
    #         line = line.replace(search_text,replace_text)
    #     print(line, end='')

if __name__ == "__main__":
   final_output()
