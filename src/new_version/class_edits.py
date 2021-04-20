import time 
from os import system, path
import requests
import os
import os.path
import subprocess
import argparse
from shutil import copyfile

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
modified_list = []
found_directories = ''


def find_dir(): ##############################
    global found_directories # ----> blank variable to add found directories too
    for dirpath, dirnames, filenames in os.walk("/"): # ----> use os.walk to look through each directory
        for filename in [f for f in filenames if f.endswith("apache2.conf" or "httpd.conf")]: # ----> search through directories to find specific file names
            found_directories += os.path.join(dirpath, filename) + '\n' # ----> add found files to a string
        for filename in [f for f in filenames if f.endswith("security.conf")]: # ----> search through directories to find specific file names
            found_directories += os.path.join(dirpath, filename) + '\n' # ----> add found files to a string
    #return (found_directories) # ----> return the finalized string with all directories found on the machine that meet the criteria   


def strip_ver(version_string):
    output = ''
    for ch in version_string:
        if ch.isdigit():
            output += ch
        elif ch == '.':
            output += ch
    return output


def get_installed_ver(): ##############################
    global installed_version
    global found_directories
    version_info = ''
    #process1 = os.popen('apache2 -v') # ----> os version; run the terminal command and print 
    #process2 = os.popen('httpd -v') # ----> os version; run the terminal command and print 
    #apache_output = process1.readlines() # ----> os version; read output from process1, return lines
    #httpd_output = process2.readlines() # ----> os version; read output from process1, return lines
    if 'apache2.conf' in found_directories:
        process1 = subprocess.run(['apache2', '-v'], capture_output=True) # ----> subprocess version; run the subprocess, capture output
        apache_output = process1.stdout.decode()
        list_apache_output = apache_output.split('\n')    
        for line in list_apache_output:
            if 'version' in line:
                version_info += line
        installed_version = strip_ver(version_info) ##############################
    elif 'httpd.conf' in found_directories:
        process2 = subprocess.run(['httpd', '-v'], capture_output=True) # ----> subprocess version; run the subprocess, capture output
        httpd_output = process2.stdout.decode() # ----> subprocess version; print standard output and decode from bytes
        list_httpd_output = httpd_output.split('\n')
        for line in list_httpd_output:
            if 'version' in line:
                version_info += line
        installed_version = strip_ver(version_info) ##############################


def compare_versions():
    global current_version
    global installed_version
    if current_version == installed_version:
        return True
    else:
        return False


def get_current_ver():
    global current_version
    process1 = requests.get('https://downloads.apache.org/httpd/')
    webtext = process1.text
    current_version = (webtext.split('IS-'))[1].split('\"')[0]


def print_list(theList):
    for line in theList: #Loop through the list
        print('{: ^100}'.format(line)) #Print each line


def conf_backup(): ##############################
    global found_directories
    current_dir = os.path.dirname(os.path.realpath(__file__)) #current directory path of backup.py    
    dirlist = found_directories.splitlines() #stores output from dir_locate.py to a list
    if os.path.isdir(current_dir + '/backup') == False: #checks if there is a backup folder
        os.mkdir(current_dir + '/backup') #makes a backup folder
    if dirlist[0].endswith('apache2.conf'):
        if path.exists( current_dir + '/backup/apache2.original.back') == False: #checks if apache2.original.back exists
            copyfile(dirlist[0],current_dir + '/backup/apache2.original.back') #copy of apache2.conf
        elif path.exists( current_dir + '/backup/apache2.original.back') == True: #checks if apache2.original.back exists
            copyfile(dirlist[0],current_dir + '/backup/apache2.updated.back') #copy of apache2.conf
    elif dirlist[0].endswith('httpd.conf'):
        if path.exists( current_dir + '/backup/httpd.original.back') == False: #checks if httpd.original.back exists
            copyfile(dirlist[0],current_dir + '/backup/httpd.original.back') #copy of httpd.conf
        elif path.exists( current_dir + '/backup/httpd.original.back') == True: #checks if httpd.original.back exists
            copyfile(dirlist[0],current_dir + '/backup/httpd.updated.back') #copy of httpd.conf
    for item in dirlist:
        if item.endswith('/conf-enabled/security.conf'):
            if path.exists( current_dir + '/backup/security.original.back') == False:  #checks if security.original.back exists
                copyfile(item,current_dir + '/backup/security.original.back') #copy of security.conf
            elif path.exists( current_dir + '/backup/security.original.back') == True:  #checks if security.original.back exists
                copyfile(item,current_dir + '/backup/security.updated.back') #copy of security.conf


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


def user_input(option, rec_setting, old_setting):
    answer_yes = ['yes','y'] #list all possible inputs for yes
    answer_no = ['no','n'] #list all possible inputs for no
    choice = input(f'\n\nWould you like to change {option} from {old_setting.strip()} to the recommended setting of: {rec_setting}? <y/n>: ') #statement placed in choice variable

    if choice.lower() in answer_yes:
        return 'True'
    elif choice.lower() in answer_no:
        return 'False'
    else:
        system('clear')
        print('Incorrect action. ', end='')
        return 'Error'


def file_len(in_file):
    count = 0
    with open(in_file, 'r') as f:
        for i, l in enumerate(f):
            pass
    return i+1


def setting_valid(line, setting):
    global correct
    global incorrect
    global modified_list
    if setting != 'Serverversion':    
        line = line.split(' ') #If line is a setting split line using on the space
        if line[0] == setting: #Check if 1st element (the Setting) is equal to the setting passed in as the variable to check
            if settings_dict[setting] == line[1].strip(): #If it is the correct setting check if the value matches the recommended
                if args.verbose: #Print the following line if the verbose option was requested
                    print(f'\rFound setting:{setting} set to the recommended setting of: {settings_dict[setting]}'.ljust(100,' '))            
                correct.append(str.format('{0} is set to:{1}',setting.ljust(22),settings_dict[setting].rjust(10))) #If it does append to correct list
                line = ' '.join(line)
                modified_list.append(line)
            else: #It doesn't match the recommended setting - append to incorrect list.
                incorrect.append(str.format('{0} is set to :{1}, the recommended setting is: {2}', setting.ljust(22),line[1].strip().rjust(10),settings_dict[setting].rjust(10)))
                if args.verbose: #Print the following line if the verbose option was requested
                    print(f'\rFound setting:{setting} set to: {line[1].strip()}.  The recommended setting is: {settings_dict[setting]}'.ljust(100,' '))
                if args.change:
                    #print('\nChange mode is on')
                    if not args.silent:
                        #print('Silent mode is off')
                        #ask for user_input()
                        user_choice = user_input(line[0],settings_dict[setting], line[1])
                        if  user_choice == 'True':
                            system('clear') #Clear the screen
                            line[1] = settings_dict[setting]
                            line = ' '.join(line)
                            modified_list.append(line)
                            #print(f'New line is: {line}')
                            #Write new setting to file
                        elif user_choice == 'False':
                            system('clear')
                            print(f'We will skip {line[0]} for now.')
                            time.sleep(1.5)
                            line = ' '.join(line)
                            modified_list.append(line)
                            system('clear')
                        elif user_choice == 'Error':
                            print(f'We will skip {line[0]} for now.')
                            time.sleep(1.5)
                            line = ' '.join(line)
                            modified_list.append(line)
                            system('clear')
                    #print('Silent mode is on')
                        #Write original setting to file
        else:
            line = ' '.join(line)
            modified_list.append(line)
                        


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
    global modified_list
    for setting in settings_dict.keys(): #Loop through each setting in the recomended settings text file
        i+=1 #Increment the iteration variable
        if i <=l: #Check if the iteration variable is less than or equal to the total number of iterations
            printProgressBar(i, l, prefix = 'Progress:', suffix = 'Complete', length = 50) #Print the progress bar with the current iteration
            time.sleep(0.001) #Sleep the timer fo a hundredth of a second
        with open('/etc/apache2/apache2.conf','r') as conf_file: #Open the file to search for settings
            modified_list = []
            for line in conf_file.readlines(): #Loop through each line in the file looking for the current setting being searched for
                i += 1 #Increment the iteration variable
                if i<=l: #Check if the iteration variable is less than or equal to the total number of iterations
                    printProgressBar(i, l, prefix = 'Progress:', suffix = 'Complete', length = 50) #Print the progress bar with the current iteration
                    time.sleep(0.001) #Sleep the timer for a hundredth of a second
                    if line[0] != '#' and line[0] != '\n' and line[0] != '<' and not line.startswith('	'):
                        setting_valid(line, setting)
                    else:
                        modified_list.append(line) 
        modified_list.append('~~~~~~~~~~')  # ----> separator between apache2/httpd and security.conf files.              
        with open('/etc/apache2/conf-enabled/security.conf','r') as conf_file: #Open the file to search for settings
            for line in conf_file.readlines(): #Loop through each line in the file looking for the current setting being searched for
                i += 1 #Increment the iteration variable
                if i<=l: #Check if the iteration variable is less than or equal to the total number of iterations
                    printProgressBar(i, l, prefix = 'Progress:', suffix = 'Complete', length = 50) #Print the progress bar with the current iteration
                    time.sleep(0.001) #Sleep the timer fo a hundredth of a second
                    if line[0] != '#' and line[0] != '\n' and line[0] != '<' and line.startswith:
                        setting_valid(line, setting)
                    else:
                        modified_list.append(line)                           
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
    global current_version
    system('clear') #Clear the screen
    find_dir() ##############################
    get_installed_ver() # Gets the currently installed Apache version.    
    get_current_ver()
    #Get the length of the Settings file, and both configuration files and set to the length for the progress bar
    l = file_len('Recommended_Settings.txt',) * file_len('/etc/apache2/apache2.conf') + file_len('Recommended_Settings.txt') * file_len('/etc/apache2/conf-enabled/security.conf')
    
    i = 0 #Set iteration counter for the progress bar to 0 
    printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50) # Initial call to print 0% progress

    if current_version == installed_version:
        correct.append(str.format('{0} installed:{1}','Apache Version'.ljust(22),current_version.rjust(10))) #If it does append to correct list
    else:
        incorrect.append(str.format('{0}installed :{1}, the current version is: {2}', 'Apache Version'.ljust(23),installed_version.rjust(10),current_version.rjust(14)))
    
    i = get_settings(i, l) #Get the recommended settings from the Recommended settings text file
    i = search(i, l) #Search the Configuration files
    
    if args.printReport: #Check if user requested a report
        report() #Print the report if requested


if __name__ == "__main__":
    main_program()    
    apache_conf = []
    security_conf = []
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
    print(apache_conf)
    print('\n\nXXXXXXXXXXXXXXX\n\n')
    print(security_conf)
    #print(new_starter)
