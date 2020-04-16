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
    def __init__(self, source_text, target_text, missing):
        self.source_text = source_text
        self.target_text = target_text
        self.missing = missing  # Missing terms, if found


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
    Function for reading in terminology from user-specified txt file.
    '''
    try:
        with open(glossary_file) as f:
            terminology = f.readlines()
    except FileNotFoundError as fnf_error:
        print(fnf_error)
    else:
        return terminology


def clean_lines(terminology):
    '''
    Function to clean enties in terminology list and also to remove duplicate 
    entries. 
    (1) Removes surrounding whitespace chars from each line (including '\n')
    (2) Removes '*' chars from the start of each line (I have these in some of 
        my client glossaries).
    '''
    terminology = [line.strip() for line in terminology]
    terminology = [line.lstrip('*') for line in terminology]
    return terminology


def entry_check(terminology):
    '''
    Function to check whether there are two entries on each line. In other
    words, whether each line contains two substrings (source and target text)
    delimited by a single tab character. Lines not formatted this way are
    passed over.
    '''
    formatted_terminology = []
    for entry in terminology:
        split_terms = entry.split('\t')
        if len(split_terms) == 2:
            formatted_terminology.append(entry)
    return formatted_terminology


def remove_duplicates(terminology):
    '''
    Function to remove duplicate entries.
    '''
    unique_terminology = []
    for entry in terminology:
        if entry not in unique_terminology:
            unique_terminology.append(entry)
    return unique_terminology


def group_terminology(terminology):
    '''
    Function to group entries together if there is more than one target term
    for a source term, i.e if a source term can be translated in more than one
    way. These are grouped into a dictionary in which the key is the source
    term and the value is a list containing target terms, i.e.:
    {source: [target1, target2, ...]}
    '''
    grouped_terminology = {}
    
    for entry in terminology:
        split_terms = entry.split('\t')
        source_term = split_terms[0].lower()
        target_term = split_terms[1].lower()

        # Check if source term already appears as a key
        if source_term in grouped_terminology:
            
            # Add the target term to the list corresponding to the source term
            # Get the current list of target terms for the source term
            translations = grouped_terminology[source_term]
            # Append the new target term to the list
            translations.append(target_term)
            # Assign the new larger list to the source term
            grouped_terminology[source_term] = translations

        else:            
            # Add new entry with the key being the source term and 
            # the value being a list containing the single target term
            grouped_terminology[source_term] = [target_term]
            
    return grouped_terminology


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
    Function for checking that terminology has been translated in the correct
    way in the translation according to the user-specified terminology.
    '''
    
    for segment in translation:

        # Only proceed if there is actual source and target text.
        if segment.source_text and segment.target_text:
            if (not segment.source_text.isspace() and 
                not segment.target_text.isspace()):
        
                # Check if any source terminology is in the source text
                # term here is the keys in the termonology dict
                for term in terminology:
                    if term in segment.source_text:

                        # Check if any corresponding target term appears 
                        # in the target text.
                        found = any(elem in segment.target_text.lower()
                                     for elem in terminology[term])    
                        
                        if found == False:
                            segment.missing[term] = terminology[term]

    return translation


def output_results(translation):
    '''
    Function for outputting results to the terminal.
    '''
    errors_found = False

    for segment in translation:
        if segment.missing:
            
            errors_found = True
            print('\n')

            for source_term in segment.missing:
                print('\'' + source_term + '\' should be translated as', end=' ')

                # Get number of target terms.
                target_num = len(segment.missing[source_term])
                counter = 0

                for target_term in segment.missing[source_term]:
                    counter += 1
                    # Second to last element.
                    if counter == target_num - 1:
                        print('\'' + target_term + '\'', end=', or ')
                    # Last element.
                    elif counter == target_num:  
                        print('\'' + target_term + '\'', end=' ')
                    # Any other element.
                    else:
                        print('\'' + target_term + '\'', end=', ')
            
            print('\nSource text:')
            print(segment.source_text)
            print('Target text:')
            print(segment.target_text)
    
    if errors_found == False:
        print('\nNo terminology errors found.\n')


def main():
    user_input = sys.argv
    if user_input_check(user_input):
        terminology = get_terminology(user_input[1])
        terminology = clean_lines(terminology)
        terminology = entry_check(terminology)
        terminology = remove_duplicates(terminology)
        terminology = group_terminology(terminology)
        translation = get_translation(user_input[2])
        translation = check_translation(terminology, translation)
        output_results(translation)
        
        
if __name__ == "__main__":
    main()
