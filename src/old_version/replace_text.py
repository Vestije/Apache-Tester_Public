#!/usr/bin/env python3
# replace text

import fileinput

replace_texts = {'javascript': 'Java', 'php': 'python'}
# makes a dictionary 'replace_texts'= {'search_text': 'replace_text'}

for line in fileinput.input('test.txt', inplace = True):
    #test.txt is the file i tried this on, placed the words "javascript" and "php" randomly in file
    for search_text in replace_texts:
        replace_text = replace_texts[search_text]
        line = line.replace(search_text,replace_text)
    print(line, end='')

####Be careful with this! If there error here, it can make the text file blank###
