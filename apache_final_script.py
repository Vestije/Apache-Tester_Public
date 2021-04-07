#!/usr/bin/env python3

from apache_version import get_ver
from dir_locate import find_dir
from dir_search import search

def final_output():
    print('╔═╗╔═╗╔═╗╔═╗╦ ╦╔═╗   ╔╦╗╔═╗╔═╗╔╦╗╔═╗╦═╗\n╠═╣╠═╝╠═╣║  ╠═╣║╣     ║ ║╣ ╚═╗ ║ ║╣ ╠╦╝\n╩ ╩╩  ╩ ╩╚═╝╩ ╩╚═╝────╩ ╚═╝╚═╝ ╩ ╚═╝╩╚═')
    print(f'\n{get_ver()}')
    print(f'\nYour files are located in:\n{find_dir()}')
    ### no code yet for search() ###



if __name__ == "__main__":
   final_output()
