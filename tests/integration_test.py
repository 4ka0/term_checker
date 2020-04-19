#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pytest

from .. import term_checker
from ..term_checker import Segment


GLOSSARY_FILE = 'tests/test_glossary.txt'
TRANSLATION_FILE = 'tests/test_translation.tmx'


def test_all():
    expected = [('[図1]...を示す断面模式図である。',
                 'Fig. 1 is a schematic view depicting ...',
                 {'断面模式図': ['cross-sectional schematic view']}),
                ('[図2]...を説明する図である。',
                 'Fig. 2 is a drawing illustrating ...',
                 {}),
                ('[図3]...を示す断面模式図である。',
                 'Fig. 3 is a cross-sectional schematic view depicting ...',
                 {}),
                ('[図4]...を説明する図である。',
                 'Fig. 4 is a drawing illustrating ...',
                 {}),
                ('[図5]...を示す図である。',
                 'Fig. 5 is a drawing depicting ...',
                 {}),
                ('[図6]...を示す図である。',
                 'Fig. 6 is a drawing depicting ...',
                 {}),
                ('[図7]...を示す平面模式図である。',
                 'Fig. 7 is a plan schematic depicting ...',
                 {'平面模式図': ['plan schematic view']})]

    # Build translation
    translation = term_checker.get_translation(TRANSLATION_FILE)

    # Build terminology
    terminology = term_checker.get_terminology(GLOSSARY_FILE)
    terminology = term_checker.clean_lines(terminology)
    terminology = term_checker.format_check(terminology)
    terminology = term_checker.remove_duplicates(terminology)
    terminology = term_checker.group_terminology(terminology)

    # Check translation
    translation = term_checker.check_translation(terminology, translation)

    # Extract content from Segment objects for assert comparison
    output = []
    for segment in translation:
        output.append((segment.source_text, segment.target_text,
                       segment.missing_terms))

    assert output == expected