#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Script to check whether project-specific terminology is being used
in a translation (tmx file).

Terminology is assumed to be listed in a tab-delimited file (txt file)
with the following format:
    source_term<tab>target_term

If multiple target terms exist for a given source term, it is assumed that
these are entered on separate lines rather than all on the same line, e.g.:
    source_term<tab>target_term_1
    source_term<tab>target_term_2
    source_term<tab>target_term_3

To execute:
    python3 term_checker.py translation.tmx glossary.txt
'''


import sys

import spacy
from spacy.tokenizer import Tokenizer
from spacy.util import compile_infix_regex
from colorama import Fore
from translate.storage.tmx import tmxfile


class Segment():
    '''
    Used to create objects for each source-target segment extracted
    from a tmx file.
    '''
    def __init__(self,
                 source_text,  # string
                 target_text,  # string
                 missing_terms,  # dict {string: list of strings}
                 hyphenated_forms):  # dict {string: string}
        self.source_text = source_text
        self.target_text = target_text
        self.missing_terms = missing_terms
        self.hyphenated_forms = hyphenated_forms


def user_input_check(user_input):
    '''
    Function to validate user input entered at the command line.
    Expected input:
        python3 terminology_check.py translation.tmx glossary.txt
    Aspects checked:
        3 arguments should have been entered
        (1st argument is the name of this script)
        2nd argument should be a tmx file (translation)
        3rd argument should be a txt file (glossary)
    '''
    input_verified = True

    # Check if 3 arguments have been input
    if len(user_input) != 3:
        input_verified = False

    else:
        translation_file = user_input[1]
        glossary_file = user_input[2]

        # Check if 2nd argument is a tmx file
        if not translation_file.lower().endswith('.tmx'):
            input_verified = False

        # Check if 3rd argument is a txt file
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
    Function to extract translation from a user-specified tmx file.
    '''
    try:
        with open(translation_file, 'rb') as file:
            tmx_file = tmxfile(file)
    except FileNotFoundError as fnf_error:
        print(fnf_error)
        sys.exit()
    else:
        translation = []  # List of Segment objects

        for node in tmx_file.unit_iter():
            source_text = node.source
            target_text = node.target
            segment = Segment(source_text, target_text, {}, {})
            translation.append(segment)

        return translation


def get_terminology(glossary_file):
    '''
    Function to read in terminology from a user-specified txt file.
    '''
    try:
        with open(glossary_file) as f:
            terminology = f.readlines()
    except FileNotFoundError as fnf_error:
        print(fnf_error)
        sys.exit()
    else:
        return terminology


def clean_lines(terminology):
    '''
    Function to clean entries in a terminology list, specifically:
    (1) Removes surrounding whitespace chars from each line (including '\n')
    (2) Removes '*' chars from the start of each line
        (I have these in some of my client glossaries).
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

    '''
    unique_terminology = []
    for entry in terminology:
        if entry not in unique_terminology:
            unique_terminology.append(entry)
    '''

    unique_terminology = list(dict.fromkeys(terminology))

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

        # If source term already appears as a key
        if source_term in grouped_terminology:
            target_terms = grouped_terminology[source_term]
            target_terms.append(target_term)
            grouped_terminology[source_term] = target_terms

        else:
            # Add new entry with the source term as the key and
            # a list containing the single target term as the value
            grouped_terminology[source_term] = [target_term]

    return grouped_terminology


def basic_check(terminology, translation):
    '''
    Function for running a basic check to see whether the target text in a
    translation segment contains correct terminology. A basic check here means
    simply using "in" to see whether correct terminology is included in the
    target text.
    '''

    missing = False

    for segment in translation:

        # Only proceed if there is actual source and target text
        if contains_content(segment):

            # Check if any source terminology is in the source text
            for entry in terminology:
                if entry in segment.source_text:

                    # Case-insensitive comparison to find target terms
                    text = segment.target_text.lower()
                    terms = [x.lower() for x in terminology[entry]]

                    # Check if any of the corresponding target terms
                    # appear in the target text
                    found = any(elem in text for elem in terms)

                    if not found:
                        segment.missing_terms[entry] = terminology[entry]
                        missing = True

    return translation, missing


def setup_tokenizer():
    '''
    Function to set up a tokenizer with specific rules to not split words or
    numbers that include hyphens.
    '''

    nlp = spacy.load('en_core_web_sm')

    # Default infixes
    inf = list(nlp.Defaults.infixes)

    # Remove the generic op between numbers or between a number and a hyphen
    inf.remove(r"(?<=[0-9])[+\-\*^](?=[0-9-])")

    # Convert inf to tuple
    inf = tuple(inf)

    # Add the removed rule after subtracting (?<=[0-9])-(?=[0-9]) pattern
    infixes = inf + tuple([r"(?<=[0-9])[+*^](?=[0-9-])", r"(?<=[0-9])-(?=-)"])

    # Remove hyphen between letters rule
    infixes = [x for x in infixes if '-|–|—|--|---|——|~' not in x]
    infix_re = compile_infix_regex(infixes)

    nlp.tokenizer = Tokenizer(nlp.vocab,
                              prefix_search=nlp.tokenizer.prefix_search,
                              suffix_search=nlp.tokenizer.suffix_search,
                              infix_finditer=infix_re.finditer,
                              token_match=nlp.tokenizer.token_match,
                              rules=nlp.Defaults.tokenizer_exceptions)

    return nlp


def lemma_check(nlp, terminology, translation):
    '''
    Function for checking whether the target text in a translation segment
    contains a correct target term in its lemma form.
    '''

    for segment in translation:

        # Only proceed if missing terminology has been found
        if segment.missing_terms:

            # List of entries to remove from missing_terms if found
            to_remove = []

            # Only look at terminolgy registered as missing
            for source_term in segment.missing_terms:
                for target_term in segment.missing_terms[source_term]:

                    # Get the lemma form of the target term
                    target_term_lemma = get_lemma(target_term, nlp)

                    # Check if target_term_lemma appears in target text
                    found = target_search(target_term_lemma,
                                          segment.target_text,
                                          nlp)

                    if found:
                        to_remove.append(source_term)

            # Remove found terms from the missing terms dict
            if to_remove:
                for entry in to_remove:
                    if entry in segment.missing_terms:
                        del segment.missing_terms[entry]

    return translation


def get_lemma(input_string, nlp):
    '''
    Function to return the lemma version of an input string.
    A lemma version being:
       - for a single-word string, the lemma of that single word
       - for a multi-word string, the same string except that the end word
            is replaced with its lemma form
    '''

    # Get end word lemma, regardless of the number of words
    subwords = input_string.split()
    doc = nlp(input_string)
    end_word_lemma = doc[-1].lemma_

    # If the input string contains more than one word, rebuild the input
    # string with the end word being replaced with its lemma form
    if len(subwords) > 1:
        split_words = input_string.rsplit(' ', 1)
        lemma_form = split_words[0] + ' ' + end_word_lemma
    else:
        lemma_form = end_word_lemma

    return lemma_form


def target_search(target_term_lemma, target_text, nlp):
    '''
    Function to check whether the lemma version of a target term appears in
    the target text of a given translation segment.
    '''

    found = False
    doc = nlp(target_text)
    subwords = target_term_lemma.split()
    subword_no = len(subwords)
    target_end_lemma = subwords[-1]

    for i in range(len(doc)):

        # Look for a lemma that matches the end target term lemma
        if doc[i].lemma_.lower() == target_end_lemma.lower():

            found_term = doc[i].lemma_

            # If necessary, get the preceding words to build the whole term
            if subword_no > 1:
                for j in range(1, subword_no):
                    found_term = doc[i - j].text + ' ' + found_term

            # Compare found term with target term
            if found_term.lower() == target_term_lemma.lower():
                found = True

    return found


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


def hyphen_check(terminology, translation):
    '''
    Function to check if hyphenated forms of missing terms appear in the
    target text. If the hyphenated form is found in the target text, this
    is not treated as an error, but rather a message indicating this is output.
    '''
    for segment in translation:
        if segment.missing_terms:
            for source_term in segment.missing_terms:
                for target_term in segment.missing_terms[source_term]:

                    # If the target_term consists of 2 or more words
                    if len(target_term.split()) > 1:
                        hyphenated = target_term.replace(' ', '-')

                        # If the hyphenated form appears in the target text
                        if hyphenated in segment.target_text:
                            segment.hyphenated_forms[source_term] = hyphenated

    return translation


def output_results(translation):
    '''
    Function to output results to the terminal.
    '''
    errors_found = False

    for segment in translation:
        if segment.missing_terms:

            errors_found = True

            for source_term in segment.missing_terms:
                print(Fore.RED + '\n\'' + source_term +
                      '\' should be translated as', end=' ')

                # Get the number of target terms
                target_num = len(segment.missing_terms[source_term])
                counter = 0

                for target_term in segment.missing_terms[source_term]:
                    counter += 1
                    # Second to last element
                    if counter == target_num - 1:
                        print('\'' + target_term + '\'', end=', or ')
                    # Last element
                    elif counter == target_num:
                        print('\'' + target_term + '\'', end=' ')
                    # Any other element
                    else:
                        print('\'' + target_term + '\'', end=', ')

                # Print hyphenated form if present

                if segment.hyphenated_forms:
                    print(Fore.RED + '(although \'' +
                          segment.hyphenated_forms[source_term] +
                          '\' appears in the target text)', end=' ')

            print(Fore.CYAN + '\nSource text:')
            print(Fore.RESET + segment.source_text)
            print(Fore.CYAN + 'Target text:')
            print(Fore.RESET + segment.target_text)

    if errors_found is False:
        print(Fore.CYAN + '\nNo terminology errors found.\n')


def main():
    # Check user input
    user_input = sys.argv
    if user_input_check(user_input):

        # Obtain translation
        translation = get_translation(user_input[1])

        # Obtain and organize terminology
        terminology = get_terminology(user_input[2])
        terminology = clean_lines(terminology)
        terminology = format_check(terminology)
        terminology = remove_duplicates(terminology)
        terminology = group_terminology(terminology)

        # Run basic check
        translation, missing = basic_check(terminology, translation)

        # Run more advanced checks if necessary
        if missing:
            nlp = setup_tokenizer()
            translation = hyphen_check(terminology, translation)
            translation = lemma_check(nlp, terminology, translation)

        # Display results
        output_results(translation)


if __name__ == "__main__":
    main()
