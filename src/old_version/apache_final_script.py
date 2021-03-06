#!/usr/bin/env python3

from os import system
from Get_Recommendations import get_settings
from Print_Report import report
from dir_search import search
from apache_version import get_ver
from dir_locate import find_dir
from dir_search import search
import argparse
#import shutil

apache_parser = argparse.ArgumentParser(prog='Apache Configuration Tester',description='Check if Apache configuration is up to best practices standard.')
apache_parser.add_argument('-c','--change', help='Allows the script to automatically change settings to match best practices.', action='store_true')
apache_parser.add_argument('-p','--printReport', help='Prints a report showing the items meeting industry best practices, followed by those that don\'t.', action='store_true')
apache_parser.add_argument('-s','--silent', help='Turns off confirmation prompts before making each change.', action='store_true')
apache_parser.add_argument('-v','--verbose',help='Enables verbose mode.', action='store_true')

args = apache_parser.parse_args()

def final_output():
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
    
    #Declare variables 
    settings = get_settings() #Gets the recommended settings from the Recommended_Settings.txt file
    correct_settings = [] #List to hold all the settings that are set to the recommended setting
    incorrect_settings = [] #List to hold all the settings that are not set to the recommended setting

    #Check Settings and add to appropiate list
    search(settings, correct_settings, incorrect_settings)
    
    #Print a report
    if args.printReport:  
        report(correct_settings, incorrect_settings)
    if args.change:
        print('Change feature not yet implemented')
    if args.verbose:
        print('Verbose feature not yet implemented')
    if args.silent:
        print('Silent feature not yet implemented')
    #print(f'\n{get_ver()}')
    #print(f'\nYour files are located in:\n{find_dir()}')
    ### no code yet for search() ###



if __name__ == "__main__":
   final_output()
