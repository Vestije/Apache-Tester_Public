#!/usr/bin/env python3

import time 
import sys
from os import system, path
import requests
import os
import os.path
import subprocess
import argparse
from shutil import copyfile

class ProgressBar: # Print progress bar while files are being searched through
    """
    @Properties:
    iteration       - Required  : current iteration (Int)
    total           - Required  : total iterations (Int)
    prefix          - Optional  : prefix string (Str)
    suffix          - Optional  : suffix string (Str)
    decimals        - Optional  : positive number of decimals in percent complete (Int)
    length          - Optional  : character length of bar (Int)
    fill            - Optional  : bar fill character (Str)
    printEnd        - Optional  : end character (e.g. "\r", "\r\n") (Str) 
    sleep           - Optional  : amount to sleep on each iteration          
    """

    def __init__(self):
        self.iteration = 0
        self.total = 0
        self.prefix = 'Progress:'
        self.suffix = 'Complete'
        self.decimals = 1
        self.length = 50
        self.fill = '█'
        self.printEnd = '\r'
        self.sleeping = 0.0
        

    def PrintMe(self):
        self.iteration += 1
        if self.iteration < self.total:
            percent = ("{0:." + str(self.decimals) + "f}").format(100 * (self.iteration / float(self.total))) # Set the current completion percentage
            filledLength = int(self.length * self.iteration // self.total) # Get the ammount the bar should be filled
            bar = self.fill * filledLength + '-' * ((self.length - filledLength)-1) # Fill the bar with the completed blocks and - for uncompleted blocks
            print(f'{self.prefix} |{bar}| {percent}% {self.suffix}', end = self.printEnd) # Print the formatted progress bar
        elif self.iteration > self.total:
            self.iteration = self.total - 1 
        else:
            self.iteration = self.total
        time.sleep(self.sleeping)
        

# Program arguments and descriptions
apache_parser = argparse.ArgumentParser(prog='Apache Configuration Tester',description='Check if Apache configuration is up to best practices standard.')
apache_parser.add_argument('-c','--change', help='Allows the script to automatically change settings to match best practices.', action='store_true')
apache_parser.add_argument('-p','--printReport', help='Prints a report showing the items meeting industry best practices, followed by those that don\'t.', action='store_true')
apache_parser.add_argument('-s','--silent', help='Turns off confirmation prompts before making each change.', action='store_true')
apache_parser.add_argument('-v','--verbose',help='Enables verbose mode.', action='store_true')

args = apache_parser.parse_args()

prog_bar = ProgressBar()
correct = []
incorrect = []
settings_dict = {}
current_version = '' # store newest version of apache avaliable online
installed_version = '' # store current version of apache on the host machine
modified_list = [] # store copy of configuration files that includes edited options if change argument is used
found_directories = [] # store all found directories 
apache_conf = [] # store apache.conf or http.conf files after modified_list is split
security_conf = [] # store security.conf files after modified_list is split


def find_dir(): # locates directories which store apache server files and stores them in a list
    global found_directories 
    global prog_bar
    for dirpath, dirnames, filenames in os.walk("/"): # ----> use os.walk to look through each directory
        prog_bar.PrintMe()
        for filename in [f for f in filenames if f.endswith("apache2.conf" or "httpd.conf")]: # ----> search through directories to find specific file names
            prog_bar.PrintMe()
            found_directories.append(os.path.join(dirpath, filename)) # ----> add found files to the list
        for filename in [f for f in filenames if f.endswith("security.conf")]: # ----> search through directories to find specific file names
            prog_bar.PrintMe()
            if 'enabled' not in dirpath: # only look at conf-avaliable for security files, conf-enabled only contains links to the actual files
                found_directories.append(os.path.join(dirpath, filename)) # add found files to the list 


def strip_ver(version_string): # strips string so only version number is left
    output = ''
    for ch in version_string:
        if ch.isdigit():
            output += ch
        elif ch == '.':
            output += ch
    return output


def get_installed_ver(): # uses subprocess to find the current installed version of apache
    global installed_version
    global found_directories
    version_info = ''

    for each_dir in found_directories:
        if 'apache2.conf' in each_dir:
            process1 = subprocess.run(['apache2', '-v'], capture_output=True) # run the subprocess, capture output
            apache_output = process1.stdout.decode()
            list_apache_output = apache_output.split('\n')    
            for line in list_apache_output:
                if 'version' in line:
                    version_info += line
            installed_version = strip_ver(version_info)
            break
        elif 'httpd.conf' in each_dir:
            process2 = subprocess.run(['httpd', '-v'], capture_output=True) # run the subprocess, capture output
            httpd_output = process2.stdout.decode() # print standard output and decode from bytes
            list_httpd_output = httpd_output.split('\n')
            for line in list_httpd_output:
                if 'version' in line:
                    version_info += line
            installed_version = strip_ver(version_info)
            break


def compare_versions(): # compare the installed version of apache on the host server to the newest update version
    global current_version
    global installed_version
    if current_version == installed_version:
        return True
    else:
        return False


def get_current_ver(): # get the version number of the newest apache version from apache website
    global current_version
    process1 = requests.get('https://downloads.apache.org/httpd/')
    webtext = process1.text
    current_version = (webtext.split('IS-'))[1].split('\"')[0]


def print_list(theList): # formatting
    for line in theList: 
        print('{: ^100}'.format(line)) 


def conf_backup():
    global found_directories
    current_dir = os.path.dirname(os.path.realpath(__file__)) # current directory path of backup.py    
    if os.path.isdir(current_dir + '/backup') == False: # checks if there is a backup folder
        os.mkdir(current_dir + '/backup') # makes a backup folder
    for item in found_directories:
        if item.endswith('security.conf'):
            if path.exists( current_dir + '/backup/security.original.back') == False: # checks if security.original.back exists
                copyfile(item,current_dir + '/backup/security.original.back') # copy of security.conf
            elif path.exists( current_dir + '/backup/security.original.back') == True: # checks if security.original.back exists
                copyfile(item,current_dir + '/backup/security.updated.back') # copy of security.conf
        if item.endswith('apache2.conf'):
            if path.exists( current_dir + '/backup/apache2.original.back') == False: # checks if security.original.back exists
                copyfile(item,current_dir + '/backup/apache2.original.back') # copy of security.conf
            elif path.exists( current_dir + '/backup/apache2.original.back') == True: # checks if security.original.back exists
                copyfile(item,current_dir + '/backup/apache2.updated.back') # copy of security.conf
        if item.endswith('httpd.conf'):
            if path.exists( current_dir + '/backup/httpd.original.back') == False: # checks if security.original.back exists
                copyfile(item,current_dir + '/backup/httpd.original.back') # copy of security.conf
            elif path.exists( current_dir + '/backup/httpd.original.back') == True: # checks if security.original.back exists
                copyfile(item,current_dir + '/backup/httpd.updated.back') # copy of security.conf

def print_header(): # print report header image and modify text color 
    class colors:
        #RED = '\033[31m'
        ENDC = '\033[m'
        GREEN = '\033[32m'
        #YELLOW = '\033[33m'
        BLUE = '\033[34m'
    
    system('clear')
    print (colors.GREEN + '-'*100 + colors.ENDC)
    print (colors.GREEN + '-'*100 + colors.ENDC)

    print(colors.GREEN +'{:/^113}'.format(colors.BLUE +' ╔═╗╔═╗╔═╗╔═╗╦ ╦╔═╗   ╔╦╗╔═╗╔═╗╔╦╗╔═╗╦═╗ ' + colors.ENDC + colors.GREEN))
    print(colors.GREEN +'{:\^113}'.format(colors.BLUE +' ╠═╣╠═╝╠═╣║  ╠═╣║╣     ║ ║╣ ╚═╗ ║ ║╣ ╠╦╝ '+ colors.ENDC + colors.GREEN))
    print(colors.GREEN +'{:/^113}'.format(colors.BLUE +' ╩ ╩╩  ╩ ╩╚═╝╩ ╩╚═╝    ╩ ╚═╝╚═╝ ╩ ╚═╝╩╚═ '+ colors.ENDC + colors.GREEN))
    
    print (colors.GREEN + '-'*100 + colors.ENDC)
    print (colors.GREEN + '-'*100 + colors.ENDC)

    sys.stdout.write('\033[1;34m') # make all following text blue


def report(): 
    print_header()
    global correct
    global incorrect
    # print the settings that are set to recommended settings
    print('{: ^100}'.format('The following settings are set to the recommended setting:'))
    print('\n')
    if not correct: #if the list is empty
        print('{: ^100}'.format('--NONE--\n')) # print no settings are set to recommended settings

    else: # print the list
        print_list(correct) # print Correct list
        print('\n'*2) # print a new line after all the lines in the list

    # print the settings that are not set to the recommended setting
    print('{: ^100}'.format('The following settings are not set to the recommended setting:'))
    print('\n')
    if not incorrect: # if the list is empty
        print('{: ^100}'.format('--NONE--\n')) # print no settings are set incorrectly.
    else: # print the list
        print_list(incorrect) # print incorrect list
        print('\n'*5)


def user_input(option, rec_setting, old_setting):
    answer_yes = ['yes','y'] # list all possible inputs for yes
    answer_no = ['no','n'] # list all possible inputs for no
    choice = input(f'\n\nWould you like to change {option} from {old_setting.strip()} to the recommended setting of: {rec_setting}? <y/n>: ') #statement placed in choice variable

    if choice.lower() in answer_yes:
        return 'True'
    elif choice.lower() in answer_no:
        return 'False'
    else:
        system('clear')
        print('Incorrect action. ', end='')
        return 'Error'


def file_len(in_file): # count number of lines that will be read from configuration files, used to set the end length of the progress bar
    count = 0
    with open(in_file, 'r') as f:
        count = len(f.readlines())
    return count + 1


def setting_valid(line, setting): # check lines from search function that meet recommended settings criteria. 
    global correct
    global incorrect
    global modified_list
    if setting != 'Serverversion':    
        line = line.split(' ') # if line is a setting split line using on the space
        if settings_dict[setting] == line[1].strip(): # if it is the correct setting check if the value matches the recommended
            if args.verbose: # print the following line if the verbose option was requested
                print(f'\rFound setting:{setting} set to the recommended setting of: {settings_dict[setting]}'.ljust(100,' '))            
            correct.append(str.format('{0} is set to:{1}',setting.ljust(22),settings_dict[setting].rjust(10))) #If it does append to correct list
            line = ' '.join(line)
            modified_list.append(line)
        else: # it doesn't match the recommended setting - append to incorrect list.
            incorrect.append(str.format('{0} is set to :{1}, the recommended setting is: {2}', setting.ljust(22),line[1].strip().rjust(10),settings_dict[setting].rjust(10)))
            if args.verbose: # print the following line if the verbose option was requested
                print(f'\rFound setting:{setting} set to: {line[1].strip()}.  The recommended setting is: {settings_dict[setting]}'.ljust(100,' '))
            if args.change: # user input requests to change settings if change arument used without silent argument
                if not args.silent: 
                    user_choice = user_input(line[0],settings_dict[setting], line[1])
                    if  user_choice == 'True':
                        system('clear') # clear the screen
                        line[1] = settings_dict[setting]
                        line = ' '.join(line)
                        modified_list.append(line+'\n')
                    elif user_choice == 'False':
                        system('clear')
                        print(f'We will skip {line[0]} for now.')
                        time.sleep(1.5)
                        line = ' '.join(line)
                        modified_list.append(line+'\n')
                        system('clear')
                    elif user_choice == 'Error':
                        print(f'We will skip {line[0]} for now.')
                        time.sleep(1.5)
                        line = ' '.join(line)
                        modified_list.append(line+'\n')
                        system('clear')
            else:
                line = ' '.join(line)
                modified_list.append(line+'\n')


def get_settings(): # pull recommended settings from txt file
    global settings_dict
    global iteration
    global prog_bar
    with open('Recommended_Settings.txt','r') as f:
        lines = f.readlines()
    for line in lines:
        prog_bar.PrintMe()
        setting = line.split(':')
        settings_dict[setting[0]] = setting[1].strip()


def search(): # check lines of configuration files, add to new modifed list
    global settings_dict
    global modified_list

    if prog_bar.iteration < prog_bar.total: # check if the iteration variable is less than or equal to the total number of iterations
        prog_bar.PrintMe()
    with open(found_directories[0],'r') as conf_file: # open the file to search for settings
        for line in conf_file.readlines(): # loop through each line in the file looking for the current setting being searched for
            if prog_bar.iteration < prog_bar.total: # check if the iteration variable is less than or equal to the total number of iterations
                prog_bar.PrintMe()
            if line[0] != '#' and line[0] != '\n' and line[0] != '<' and not line.startswith('	'):
                if line.split(' ')[0] in settings_dict.keys():
                    setting_valid(line, line.split(' ')[0])
                else:
                    modified_list.append(line)
            else:
                    modified_list.append(line) 
        modified_list.append('~~~~~~~~~~')  # separator between apache2/httpd and security.conf files.              
        with open(found_directories[1],'r') as conf_file: # open the file to search for settings
            for line in conf_file.readlines(): # ;oop through each line in the file looking for the current setting being searched for
                if prog_bar.iteration < prog_bar.total: # check if the iteration variable is less than or equal to the total number of iterations
                    prog_bar.PrintMe()
                if line[0] != '#' and line[0] != '\n' and line[0] != '<' and line.startswith:
                    setting_valid(line, line.split(' ')[0])
                else:
                    modified_list.append(line)                              


def write_file(in_list, filename): # 
    global found_directories
    for each_dir in found_directories:
        if filename in each_dir:
            with open(each_dir, "w") as copy: # note that the copy file location does not need to exist before running
                for line in in_list: # reads each line in the file
                    copy.write(line) 


def split_list(): # splits modified list into apache_conf and security_conf files
    global modified_list
    global apache_conf
    global security_conf
    new_starter = 0
    for index,line in enumerate(modified_list):
        if '~~~~~~~~~~' in line:
            new_starter += index + 1
            break
        else:
            apache_conf.append(line)
    for index,line in enumerate(modified_list):
        if index > new_starter:
            security_conf.append(line)


def main_program(): # main program ran if __name__ == "__main__"
    global current_version
    global found_directories
    global apache_conf
    global security_conf
    if args.change:
        prog_bar.total = 43003
    else:
        prog_bar.total = 38779
    system('clear') # clear the screen
    sys.stdout.write('\033[1;34m')
    
    find_dir()
    if args.change:
        try: # checks if write privilages are avaliable with current permissions, error message if we need additional permissions to run change arugment
            filehandle = open(found_directories[0], 'a')
            filehandle.close()
        except IOError:
            system('clear') #Clear the screen
            sys.exit( 'Change option requires elevated priveledges.\nPlease run as root to use this option.') 

    prog_bar.PrintMe()
    get_installed_ver()
    get_current_ver()

    if current_version == installed_version:
        correct.append(str.format('{0} installed:{1}','Apache Version'.ljust(22),current_version.rjust(10))) # if it does append to correct list
    else:
        incorrect.append(str.format('{0}installed :{1}, the current version is: {2}', 'Apache Version'.ljust(23),installed_version.rjust(10),current_version.rjust(14)))
    
    get_settings() # get the recommended settings from the Recommended settings text file
    search() # search the Configuration files
    
    if args.printReport: # check if user requested a report
        report() # print the report if requested
    
    if args.change:
        conf_backup()
        split_list()
        write_file(security_conf,'security.conf')
        write_file(apache_conf,'apache2.conf')

        
        
if __name__ == "__main__":
    main_program() 
