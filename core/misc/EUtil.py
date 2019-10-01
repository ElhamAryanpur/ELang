'''
    COPYRIGHT 2019 Elham Aryanpur

    This is utilities needed for different projects that
    would otherwise take lot of repitation and code size.

    For license, Please refer to LICENSE file in the master branch.
'''

from platform import system
import os

def clearScreen():
    if system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')