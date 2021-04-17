#!/usr/bin/env python3

import time # needed for delay

# Print iterations progress
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
    #code provided by Greenstick from https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console#

if __name__ == "__main__":
#### test argument ####
    # A List of Items
    
    
    #items = list(range(0, 57)) #bar starts at 0; 57 is number of seconds to complete bar as below we have time.sleep(0.1) i.e., bar sleeps for .1 seconds before ticking up again
    l = 6
    i = 0
    # Initial call to print 0% progress
    
    printProgressBar(0, l, prefix = 'Progress:', suffix = '  Complete  -  Checking Apache version....', length = 50)
    
    time.sleep(1)
    
    printProgressBar(1, l, prefix = 'Progress:', suffix = ' Complete  -  Searching for directories...', length = 50)

    time.sleep(1)
    
    printProgressBar(2, l, prefix = 'Progress:', suffix = ' Complete  -  Searching for directories...', length = 50)

    time.sleep(1)

    printProgressBar(3, l, prefix = 'Progress:', suffix = ' Complete  -  Checking current settings...', length = 50)

    time.sleep(1)

    printProgressBar(4, l, prefix = 'Progress:', suffix = ' Complete  -  Checking current settings...', length = 50)

    time.sleep(1)

    printProgressBar(5, l, prefix = 'Progress:', suffix = ' Complete  -  Comparing current settings...', length = 50)

    time.sleep(1)

    printProgressBar(6, l, prefix = 'Progress:', suffix = 'Complete  -  Finalizing settings report...', length = 50)
#### test argument ####


#~~~~~~~~~~~~~~ need different bar for verbose mode, as we will only use the progress bar for checking version, checking directories, and starting search for directories ~~~~~~~~~~~~~#
