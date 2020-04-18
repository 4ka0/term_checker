#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Script to check whether project-specific terminology is being used
in a translation (tmx file).

Terminology is assumed to be listed in a tab-delimited file (txt file)
with the following format:
    source_term <tab> target_term

If multiple target terms exist for a given source term, it is assumed that
these are entered on separate lines rather than all on the same line, e.g.:
    source_term <tab> target_term_1
    source_term <tab> target_term_2
    source_term <tab> target_term_3

To execute:
    python3 term_checker.py translation.tmx glossary.txt
'''


import sys

from colorama import Fore
from translate.storage.tmx import tmxfile


class Segment():
    '''
    Used to create objects for each source-target segment extracted
    from a tmx file.
    '''
    def __init__(self, source_text, target_text, missing_terms):
        self.source_text = source_text  # string
        self.target_text = target_text  # string
        self.missing_terms = missing_terms  # dict


def user_input_check(user_input):
    '''
    Function for validating user input entered at the command line.
    Expected input:
        python3 terminology_check.py translation.tmx glossary.txt
    Aspects checked:
        3 arguments should have been entered
        (1st argument is the name of this script)
        2nd argument should be a tmx file (translation)
        3rd argument should be a txt file (glossary)
    '''
    input_verified = True

    # Check if 3 arguments have been input.
    if len(user_input) != 3:
        input_verified = False

    else:
        translation_file = user_input[1]
        glossary_file = user_input[2]

        # Check if 2nd argument is a tmx file.
        if not translation_file.lower().endswith('.tmx'):
            input_verified = False

        # Check if 3rd argument is a txt file.
        if not glossary_file.lower().endswith('.txt'):
            input_verified = False

    # Error message.
    if not input_verified:
        print('\nIncorrect input.\n'
              'Please try again using the following format.\n'
              'python3 terminology_check.py translation.tmx glossary.txt\n')

    return input_verified


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
            # {} below is 'missing_terms'
            segment = Segment(source_text, target_text, {})
            translation.append(segment)

        return translation


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
    Function to clean entries in a terminology list and also to remove
    duplicate entries. Specifically:
    (1) Removes surrounding whitespace chars from each line (including '\n')
    (2) Removes '*' chars from the start of each line (I have these in some of
        my client glossaries).
    '''
    terminology = [line.strip() for line in terminology]
    terminology = [line.lstrip('*') for line in terminology]
    return terminology


def format_check(terminology):
    '''
    Function to check whether there are two entries on each line. In other
    words, whether each line contains two substrings (source and target text)
    delimited by a single tab character. Lines not formatted this way are
    ignored.
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
        source_term = split_terms[0]
        target_term = split_terms[1]

        # If source term already appears as a key.
        if source_term in grouped_terminology:
            target_terms = grouped_terminology[source_term]
            target_terms.append(target_term)
            grouped_terminology[source_term] = target_terms

        else:
            # Add new entry with the source term as the key and
            # a list containing the single target term as the value.
            grouped_terminology[source_term] = [target_term]

    return grouped_terminology


def check_translation(terminology, translation):
    '''
    Function for checking that terminology has been translated in the correct
    way in the translation according to the user-specified terminology.
    '''

    for segment in translation:

        # Only proceed if there is actual source and target text.
        if contains_content(segment):

            # Check if any source terminology is in the source text.
            for entry in terminology:
            # 'source_term' here refers to keys in the terminology dict.
                if entry in segment.source_text:

                    # Case-insensitive comparison to find target terms
                    text = segment.target_text.lower()
                    terms = [x.lower() for x in terminology[entry]]

                    # Check if any corresponding target term appears
                    # in the target text.
                    found = any(elem in text for elem in terms)

                    if not found:
                        segment.missing_terms[entry] = terminology[entry]

    return translation


def contains_content(segment):
    '''
    Function to check if a segment contains actual source and target text
    that is not simply whitespace.
    '''
    if segment.source_text:
        if segment.target_text:
            if not segment.source_text.isspace():
                if not segment.target_text.isspace():
                    return True
    return False


def output_results(translation):
    '''
    Function for outputting results to the terminal.
    '''
    errors_found = False

    for segment in translation:
        if segment.missing_terms:

            errors_found = True
            print('\n')

            for source in segment.missing_terms:
                print(Fore.RED + '\'' + source + '\' should be translated as',
                      end=' ')

                # Get the number of target terms.
                target_num = len(segment.missing_terms[source])
                counter = 0

                for target in segment.missing_terms[source]:
                    counter += 1
                    # Second to last element.
                    if counter == target_num - 1:
                        print('\'' + target + '\'', end=', or ')
                    # Last element.
                    elif counter == target_num:
                        print('\'' + target + '\'', end=' ')
                    # Any other element.
                    else:
                        print('\'' + target + '\'', end=', ')

            print(Fore.CYAN + '\nSource text:')
            print(Fore.RESET + segment.source_text)
            print(Fore.CYAN + 'Target text:')
            print(Fore.RESET + segment.target_text)

    if errors_found == False:
        print(Fore.CYAN + '\nNo terminology errors found.\n')


def main():
    user_input = sys.argv
    if user_input_check(user_input):
        translation = get_translation(user_input[1])
        terminology = get_terminology(user_input[2])
        terminology = clean_lines(terminology)
        terminology = format_check(terminology)
        terminology = remove_duplicates(terminology)
        terminology = group_terminology(terminology)
        translation = check_translation(terminology, translation)
        output_results(translation)


if __name__ == "__main__":
    main()
