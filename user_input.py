#!/usr/bin/env python3

def user_input():
    answer_yes = ['yes','Yes','YES','y','Y'] #list all possible inputs for yes
    answer_no = ['no','No','NO','n','N'] #list all possible inputs for no
    choice = input('Would you like to set this option for optimal security? <y/n>\n') #statement placed in choice variable

    if choice in answer_yes:
        #return({1}) # ----> return int 1 for yes
        return('awesome!')
    elif choice in answer_no:
        #return({0}) # ----> return int 0 for no
        return('maybe next time...')
    else:
        #return({0}) # ----> return int 0 for no
        return('incorrect action, we will skip this for now.')

if __name__ == '__main__':
    print(user_input())
