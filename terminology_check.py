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
        (1st argument is the name of this script)
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


def get_terminology(glossary_file):
    '''
    Function for extracting terminology from user-specified txt file.
    '''
    
    terminology = []

    # Read in terminology data file
    with open(glossary_file) as f:
        terminology = f.readlines()
        # Remove possible '*' chars from the start of each line
        terminology = [line.lstrip('*') for line in terminology]
        # Remove whitespace chars such as '\n' from the end of each line
        terminology = [line.rstrip() for line in terminology]

    return terminology


def get_translation(translation_file):
    '''
    Function for extracting translation from user-specified tmx file.
    '''

    '''
    NEXT
    Save segment pairs as a Segment object as per gather.py
    '''

    translation = []

    root = tree.getroot()
    header = root.find('./header')
    source_lang = header.get('srclang')
    segments = []

    # Look at each 'tu' node
    for tu in root.iter('tu'):

        target_lang = ''
        source_text = ''
        target_text = ''

        # Any children present? Should be 2 'tuv' nodes
        if len(tu) > 0:

            for child in tu:

                # Only look at 'tuv' children
                if child.tag == 'tuv':

                    # Get language
                    lang = child.get('lang')

                    # Set target language if appropriate
                    if lang != source_lang:
                        target_lang = lang

                    # Any children present? Should be 1 'seg' node
                    if len(child) > 0:

                        for subchild in child:

                            # Only look at 'seg' child nodes
                            if subchild.tag == 'seg':

                                '''
                                Source or target text?
                                Check if text exists.
                                If not, assign empty string
                                to avoid 'None' being assigned.
                                '''
                                if target_lang == '':
                                    if subchild.text:
                                        source_text = subchild.text
                                    else:
                                        source_text = ''
                                else:
                                    if subchild.text:
                                        target_text = subchild.text
                                    else:
                                        target_text = ''


    
    return translation


def check_translation(terminology, translation):
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


def output_results(results):
    '''
    Function for outputting results to the terminal.
    '''
    pass


def main():
    user_input = sys.argv
    if user_input_check(user_input):
        terminology = get_terminology(user_input[1])
        translation = get_translation(user_input[2])
        results = check_translation(terminology, translation)
        output_results(results)
        
        
if __name__ == "__main__":
    main()
