#!/usr/bin/env python3

import os
from dir_locate import find_dir



def search():
    directories = find_dir().split('\n')
    
    for each_dir in directories:
        if 'apache2.conf' in each_dir:
            return(f'{each_dir} has apache2.conf')

print(search())


