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
        print('\n'*5
