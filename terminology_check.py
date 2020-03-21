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


class Segment():
    '''
    Used to create objects for each source-target segment extracted
    from a tmx file.
    '''
    def __init__(self, source_text, target_text):
        self.source_text = source_text
        self.target_text = target_text


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
    Entries are stored as single tab-delimited string and added to
    a list called 'terminology'.
    '''
    try:
        with open(glossary_file) as f:
            terminology = f.readlines()
            # Remove possible '*' chars from the start of each line
            terminology = [line.lstrip('*') for line in terminology]
            # Remove whitespace chars such as '\n' from the end of each line
            terminology = [line.rstrip() for line in terminology]
    except FileNotFoundError as fnf_error:
        print(fnf_error)
    else:
        return terminology


def get_translation(translation_file):
    '''
    Function for extracting translation from user-specified tmx file.
    Sentence pairs are stored as single tab-delimited string and added to
    a list called 'translation'.
    '''
    try:
        with open(translation_file, 'rb') as tmx_file:
            tree = ET.parse(tmx_file)
    except FileNotFoundError as fnf_error:
        print(fnf_error)
    else:
        root = tree.getroot()
        header = root.find('./header')
        source_lang = header.get('srclang')
        translation = []

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
            
            segment = Segment(source_text, target_text)
            translation.append(segment)
   
        return translation


def check_translation(terminology, translation):
    '''
    Function for checking terminology against the translation.
    The check made is case-insensitive.
    '''
    
    for segment in translation:

        # Only proceed if there is actual source and target text.
        if segment.source_text and segment.target_text:
            if not segment.source_text.isspace() and not segment.target_text.isspace():
        
                # Check if any source terminology is in the source text

                for entry in terminology:
                    
                    both_terms = entry.split('\t')
                    source_term = both_terms[0].lower()
                    target_term = both_terms[1].lower()

                    source_instances = segment.source_text.lower().count(source_term)
                    target_instances = segment.target_text.lower().count(target_term)

                    if source_instances > 0:
                        if target_instances < source_instances:

                            # Error found
                            print('\n' + segment.source_text)
                            print(segment.target_text)
                            print(str(both_terms))
                            print(source_term + ' = ' + str(source_instances))
                            print(target_term + ' = ' + str(target_instances))

    results = []
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
