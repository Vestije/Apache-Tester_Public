#!/usr/bin/env python3

import requests


def current_ver():
    process1 = requests.get('https://mirror.jframeworks.com/apache//httpd/')
    webtext = process1.text

    return((webtext.split('IS-'))[1].split('\"')[0])

if __name__ == "__main__":
    print(current_ver())
