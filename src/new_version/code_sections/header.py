from os import system
import sys

def print_header():
    class colors:
        RED = '\033[31m'
        ENDC = '\033[m'
        GREEN = '\033[32m'
        YELLOW = '\033[33m'
        BLUE = '\033[34m'
    
    system('clear')
    print (colors.GREEN + '-'*100 + colors.ENDC)
    print (colors.GREEN + '-'*100 + colors.ENDC)

    print(colors.GREEN +'{:/^113}'.format(colors.BLUE +' ╔═╗╔═╗╔═╗╔═╗╦ ╦╔═╗   ╔╦╗╔═╗╔═╗╔╦╗╔═╗╦═╗ ' + colors.ENDC + colors.GREEN))
    print(colors.GREEN +'{:\^113}'.format(colors.BLUE +' ╠═╣╠═╝╠═╣║  ╠═╣║╣     ║ ║╣ ╚═╗ ║ ║╣ ╠╦╝ '+ colors.ENDC + colors.GREEN))
    print(colors.GREEN +'{:/^113}'.format(colors.BLUE +' ╩ ╩╩  ╩ ╩╚═╝╩ ╩╚═╝    ╩ ╚═╝╚═╝ ╩ ╚═╝╩╚═ '+ colors.ENDC + colors.GREEN))
    
    print (colors.GREEN + '-'*100 + colors.ENDC)
    print (colors.GREEN + '-'*100 + colors.ENDC)

    sys.stdout.write('\033[1;34m') #make all following text blue

if __name__ == "__main__":
    print_header()

    print('Hello, World')
    print("It's all blue...")
