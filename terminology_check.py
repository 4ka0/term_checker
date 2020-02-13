#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Script to check whether project-specific terminology is being used 
in a Japanese to English translation (tmx file).

Terminology is listed in a tab-delimited file (txt file) with
the following format: Japanese<tab>English.

Features:
	Obtaining command line arguments
	Reading txt file
	Parsing tmx file
	String comparisons

To execute:
	python3 terminology_check.py tmxfile txtfile
'''

import sys
import xml.etree.ElementTree as ET

if verify.user_input_check(sys.argv):
        segments = gather.gather_segments(sys.argv[1])


def user_input_check(argv):
    '''
    Function for validating user input entered at the command line.
    Aspects checked:
        Two arguments should have been entered.
        The second argument should be a tmx file.
        The existence of the actual tmx file is checked in gather.py
            (The “easier to ask for forgiveness than permission” (EAFP)
            approach is used to avoid a race condition.)
    '''
    input_verified = True

    # If two arguments have not been entered
    if len(argv) != 2:
        input_verified = False
        print(Fore.RED + 'Incorrect number of arguments entered.')

    # If two arguments have been entered
    else:
        file = argv[1]

        # If the second argument is not a tmx file
        if not file.lower().endswith('.tmx'):
            input_verified = False
            print(Fore.RED + 'Incorrect file type. Only tmx files accepted.')

    if not input_verified:
        print(Fore.RED + 'Please try again using the following format.')
        print(Fore.CYAN + 'python3 checker.py yourfile.tmx')

    return input_verified


def get_terminology():
	'''
	Function for extracting terminology from user-specified txt file.
	'''
	pass


def get_translation():
	'''
	Function for extracting translation from user-specified tmx file.
	'''
	pass


def check_translation():
	'''
	Function for checking terminology against the translation.
	'''
	
	'''
	Parse through tmx file segment by segment
		In each segment, check if Jap text contains word in Jap list
			If yes, count number of instances in Jap text
					check corresponding Eng word is in Eng text same number of instances
						If yes, no problem
						If not, report error
			If not, no problem
	'''
	pass


def output_results():
	'''
	Function for outputting results to the terminal.
	'''
	pass


def main():
	if user_input_check(sys.argv):
		get_terminology()
		get_translation()
		check_translation()
		
		
if __name__ == "__main__":
    main()
