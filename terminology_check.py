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
	python3 terminology_check.py glossary.txt translation.tmx
'''


import sys
import xml.etree.ElementTree as ET


def user_input_check(user_input):
    '''
    Function for validating user input entered at the command line.
    Expected input:
    	python3 terminology_check.py glossary.txt translation.tmx
    Aspects checked:
        3 arguments should have been entered
        1st argument should be a python script
        2nd argument should be a txt file (glossary)
        3rd argument should be a tmx file (translation)
    '''
    input_verified = True

    # Check if 3 arguments have been input
    if len(user_input) != 3:
        input_verified = False

    else:
        glossary_file = user_input[1]
        translation_file = user_input[2]

        # Check if 2nd argument is a txt file
        if not glossary_file.lower().endswith('.txt'):
            input_verified = False

        # Check if 3rd argument is a tmx file
        if not translation_file.lower().endswith('.tmx'):
            input_verified = False

    # Error message   
    if not input_verified:
        print(' Incorrect input.\n'
        	  ' Please try again using the following format.\n'
        	  ' python3 terminology_check.py glossary.txt translation.tmx')

    return input_verified


def get_terminology():
	'''
	Function for extracting terminology from user-specified txt file.
	'''
	
	terminology = []

	# Get data from file, populate list
	# line by line or all at once?

	with open(filename) as f:
    	content = f.readlines()
		# Remove whitespace characters such as \n at the end of each line
		content = [line.rstrip() for line in content]

	return terminology


def get_translation():
	'''
	Function for extracting translation from user-specified tmx file.
	'''
	translation = []
	return translation


def check_translation():
	'''
	Function for checking terminology against the translation.
	'''
	results = []
	'''
	Parse through tmx file segment by segment
		In each segment, check if Jap text contains word in Jap list
			If yes, count number of instances in Jap text
					check corresponding Eng word is in Eng text at 
					the same number of instances
						If yes, no problem
						If not, report error
			If not, no problem
	'''
	return results


def output_results():
	'''
	Function for outputting results to the terminal.
	'''
	pass


def main():
	user_input = sys.argv
	if user_input_check(user_input):
		terminology = get_terminology(user_input[3])
		translation = get_translation(user_input[2])
		results = check_translation(terminology, translation)
		output_results(results)
		
		
if __name__ == "__main__":
    main()
