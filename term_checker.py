#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Script to check whether project-specific terminology is being used 
in a translation (tmx file).

Terminology is assumed to be listed in a tab-delimited file (txt file)
with the following format: Source<tab>Target

To execute:
python3 term_checker.py glossary.txt translation.tmx
'''


import sys
from translate.storage.tmx import tmxfile


class Segment():
    '''
    Used to create objects for each source-target segment extracted
    from a tmx file.
    '''
    def __init__(self, source_text, target_text, missing_terms):
        self.source_text = source_text
        self.target_text = target_text
        self.missing_terms = missing_terms


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
            # Remove surrounding whitespace chars from each line including '\n'
            terminology = [line.strip() for line in terminology]
            # Remove possible '*' chars from the start of each line
            # (I have these in some of my client glossaries)
            terminology = [line.lstrip('*') for line in terminology]
    except FileNotFoundError as fnf_error:
        print(fnf_error)
    else:
        return terminology


def get_translation(translation_file):
    '''
    Function for extracting translation from a user-specified tmx file.
    '''
    try:
        with open(translation_file, 'rb') as file:
            tmx_file = tmxfile(file)
    except FileNotFoundError as fnf_error:
        print(fnf_error)
    else:
        translation = []  # List of Segment objects

        for node in tmx_file.unit_iter():
            source_text = node.source
            target_text = node.target
            segment = Segment(source_text, target_text, {})
            translation.append(segment)

        return translation


def check_translation(terminology, translation):
    '''
    Function for checking terminology against the translation.
    Note that it should be possible to translate a given source term 
    in more than one way; therefore, from the source term to the target term, 
    a one-to-many relationship is permitted, i.e. a one-to-one relationship
    would be too strict.
    '''
    
    for segment in translation:

        # Only proceed if there is actual source and target text.
        if segment.source_text and segment.target_text:
            if (not segment.source_text.isspace() and 
                not segment.target_text.isspace()):
        
                # Check if any source terminology is in the source text
                for entry in terminology:
                    
                    # Extract source and target terms
                    both_terms = entry.split('\t')
                    if len(both_terms) == 2:
                        source_term = both_terms[0]
                        target_term = both_terms[1]

                    # Convert all to lower case for case-insensitive comparison
                    source_term = source_term.lower()
                    target_term = target_term.lower()
                    source_text = segment.source_text.lower()
                    target_text = segment.target_text.lower()

                    # Get number of instances of each term in present segment
                    source_instances = source_text.count(source_term)
                    target_instances = target_text.count(target_term)

                    if source_instances > 0:
                        # Error condition: if the target term does not appear
                        if target_instances == 0:
                            # Error found: add as missing term
                            segment.missing_terms[source_term] = target_term

    return translation


def output_results(translation):
    '''
    Function for outputting results to the terminal.
    '''
    for segment in translation:
        if segment.missing_terms:
            print('\nPlease check the following terms.')
            for entry in segment.missing_terms:
                print('\'' + entry + '\' should be translated as \'' + 
                      segment.missing_terms[entry] + '\'.')
            print(segment.source_text)
            print(segment.target_text)


def main():
    user_input = sys.argv
    if user_input_check(user_input):
        terminology = get_terminology(user_input[1])
        translation = get_translation(user_input[2])
        translation = check_translation(terminology, translation)
        output_results(translation)
        
        
if __name__ == "__main__":
    main()
