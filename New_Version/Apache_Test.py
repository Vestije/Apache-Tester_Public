import time # for sample
from os import system
import requests
import os
import subprocess
import argparse
#import shutil

apache_parser = argparse.ArgumentParser(prog='Apache Configuration Tester',description='Check if Apache configuration is up to best practices standard.')
apache_parser.add_argument('-c','--change', help='Allows the script to automatically change settings to match best practices.', action='store_true')
apache_parser.add_argument('-p','--printReport', help='Prints a report showing the items meeting industry best practices, followed by those that don\'t.', action='store_true')
apache_parser.add_argument('-s','--silent', help='Turns off confirmation prompts before making each change.', action='store_true')
apache_parser.add_argument('-v','--verbose',help='Enables verbose mode.', action='store_true')

args = apache_parser.parse_args()
correct = []
incorrect = []
settings_dict = {}
current_version = ''
installed_version = ''

def strip_ver(version_string):
    output = ''
    for ch in version_string:
        #print(ch)
        if ch.isdigit():
            output += ch
        elif ch == '.':
            output += ch
    return output

def get_installed_ver():
    global installed_version  
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
    installed_version = strip_ver(version_info) 
def compare_versions():
    global current_version
    global installed_version
    if current_version == installed_version:
        return True
    else:
        return False

def get_current_ver():
    process1 = requests.get('https://ftp.wayne.edu/apache//httpd/')
    webtext = process1.text
    current_version = (webtext.split('IS-'))[1].split('\"')[0]

def print_list(theList):
    for line in theList: #Loop through the list
        print('{: ^100}'.format(line)) #Print each line
def print_header():
    system('clear') #Clear the screen
    print('*'*100)	
    print('{:*^100}'.format(' ╔═╗╔═╗╔═╗╔═╗╦ ╦╔═╗   ╔╦╗╔═╗╔═╗╔╦╗╔═╗╦═╗ '))
    print('{:*^100}'.format(' ╠═╣╠═╝╠═╣║  ╠═╣║╣     ║ ║╣ ╚═╗ ║ ║╣ ╠╦╝ '))
    print('{:*^100}'.format(' ╩ ╩╩  ╩ ╩╚═╝╩ ╩╚═╝    ╩ ╚═╝╚═╝ ╩ ╚═╝╩╚═ '))
  
    #*************************************************************************
    #**** The following 3 lines just print the Apache Tester ASCII art in ****
    #**** the center of the terminal console window.  Remove the # before ****
    #**** each line to print them and comment out the three above instead ****
    #*************************************************************************

    #print('╔═╗╔═╗╔═╗╔═╗╦ ╦╔═╗   ╔╦╗╔═╗╔═╗╔╦╗╔═╗╦═╗'.center(shutil.get_terminal_size().columns))
    #print('╠═╣╠═╝╠═╣║  ╠═╣║╣     ║ ║╣ ╚═╗ ║ ║╣ ╠╦╝'.center(shutil.get_terminal_size().columns))
    #print('╩ ╩╩  ╩ ╩╚═╝╩ ╩╚═╝    ╩ ╚═╝╚═╝ ╩ ╚═╝╩╚═'.center(shutil.get_terminal_size().columns))
    print('*'*100)
    print('\n'* 2)
    
def report():
    print_header()
    global correct
    global incorrect
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

def file_len(in_file):
    count = 0
    with open(in_file, 'r') as f:
        for i, l in enumerate(f):
            pass
    return i+1

def setting_valid(line, setting):
    global correct
    global incorrect
    if setting != 'Serverversion':    
        line = line.split(' ') #If line is a setting split line using on the space
        if line[0] == setting: #Check if 1st element (the Setting) is equal to the setting passed in as the variable to check

            if settings_dict[setting] == line[1].strip(): #If it is the correct setting check if the value matches the recommended
                if args.verbose: #Print the following line if the verbose option was requested
                    print(f'\rFound setting:{setting} set to the recommended setting of: {settings_dict[setting]}'.ljust(100,' '))            
                correct.append(str.format('{0} is set to:{1}',setting.ljust(18),settings_dict[setting].rjust(25))) #If it does append to correct list
            else: #It doesn't match the recommended setting - append to incorrect list.
                if args.verbose: #Print the following line if the verbose option was requested
                    print(f'\rFound setting:{setting} set to: {line[1].strip()}.  The recommended setting is: {settings_dict[setting]}'.ljust(100,' '))
                incorrect.append(str.format('{0} is set to :{1}, the recommended setting is: {2}', setting.ljust(22),line[1].strip().rjust(25),settings_dict[setting].rjust(25)))

    '''The code below is currently bugged.  The function that checks the web for the current version isn't working.'''
    #else:
        #if settings_dict[setting] == line:
            #if args.verbose: #Print the following line if verbose option was requested
                #print(f'\rFound setting:{setting} set to the recommended setting of: {settings_dict[setting]}'.ljust(100,' '))
            #correct.append(str.format('{0} is set to:{1}',setting.ljust(18),settings_dict[setting].rjust(25))) #If it does append to correct list
        #else: #It doesn't match the recommended setting - append to incorrect list.
            #incorrect.append(str.format('{0} is set to :{1}, the recommended setting is: {2}', setting.ljust(22),line[1].strip().rjust(25),settings_dict[setting].rjust(25)))

def get_settings(i, l):
    global settings_dict
    with open('Recommended_Settings.txt','r') as f:
        lines = f.readlines()
    for line in lines:
        i += 1
        if i<=l:
            printProgressBar(i, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
        setting = line.split(':')
        settings_dict[setting[0]] = setting[1].strip()
    time.sleep(0.01)
    return i

def search(i,l):
    global settings_dict
    for setting in settings_dict.keys(): #Loop through each setting in the recomended settings text file
        i+=1 #Increment the iteration variable
        if i <=l: #Check if the iteration variable is less than or equal to the total number of iterations
            printProgressBar(i, l, prefix = 'Progress:', suffix = 'Complete', length = 50) #Print the progress bar with the current iteration
            time.sleep(0.001) #Sleep the timer fo a hundredth of a second
        with open('/etc/apache2/apache2.conf','r') as conf_file: #Open the file to search for settings
            for line in conf_file.readlines(): #Loop through each line in the file looking for the current setting being searched for
                i += 1 #Increment the iteration variable
                if i<=l: #Check if the iteration variable is less than or equal to the total number of iterations
                    printProgressBar(i, l, prefix = 'Progress:', suffix = 'Complete', length = 50) #Print the progress bar with the current iteration
                    time.sleep(0.001) #Sleep the timer fo a hundredth of a second
                    if line[0] != '#' and line[0] != '\n':
                        setting_valid(line, setting) 
        with open('/etc/apache2/conf-enabled/security.conf','r') as conf_file: #Open the file to search for settings
            for line in conf_file.readlines(): #Loop through each line in the file looking for the current setting being searched for
                i += 1 #Increment the iteration variable
                if i<=l: #Check if the iteration variable is less than or equal to the total number of iterations
                    printProgressBar(i, l, prefix = 'Progress:', suffix = 'Complete', length = 50) #Print the progress bar with the current iteration
                    time.sleep(0.001) #Sleep the timer fo a hundredth of a second
                    if line[0] != '#' and line[0] != '\n':
                        setting_valid(line, setting)                           
    return i #Return the iteration variable (with changes)     
    

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
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
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total))) #Set the current completion percentage
    filledLength = int(length * iteration // total) #Get the ammount the bar should be filled
    bar = fill * filledLength + '-' * (length - filledLength) # Fill the bar with the completed blocks and - for uncompleted blocks
    print(f'{prefix} |{bar}| {percent}% {suffix}', end = printEnd) #Print the formatted progress bar

    if iteration == total: #Check if job is complete
        print() #Print a new line if job is complete
        
def main_program():
    system('clear') #Clear the screen
    
    #Get the length of the Settings file, and both configuration files and set to the length for the progress bar
    l = file_len('Recommended_Settings.txt',) * file_len('/etc/apache2/apache2.conf') + file_len('Recommended_Settings.txt') * file_len('/etc/apache2/conf-enabled/security.conf')
    
    i = 0 #Set iteration counter for the progress bar to 0 
    printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50) # Initial call to print 0% progress
    get_installed_ver() # Gets the currently installed Apache version.
    
    '''Code below commented out because it is currently bugged'''
    #current_version = current_ver()
    #settings_dict['Serverversion'] = current_version
    #setting_valid(current_version,'Serverversion')
    
    i = get_settings(i, l) #Get the recommended settings from the Recommended settings text file
    i = search(i, l) #Search the Configuration files
    
    if args.printReport: #Check if user requested a report
        report() #Print the report if requested

if __name__ == "__main__":
    main_program()
    #print(installed_version) #This was just for testing purposes
