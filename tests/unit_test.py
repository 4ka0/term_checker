#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pytest
from .. import term_checker
from ..term_checker import Segment


'''
Test class instantiation.
'''
def test_constructor():
    s = Segment('なお、正孔輸送層12は、NiO、（またはMoO3）等の無機材料を...',
                'Moreover, the positive  hole transport layers 12 may...',
                {})
    assert isinstance(s, Segment)


'''
Test user input verification.
'''
@pytest.mark.parametrize('user_input,expected', [
                          (['term_checker.py', 'file.txt', 'file.tmx'], True),
                          (['term_checker.py'], False),
                          (['term_checker.py', 'file.txt'], False),
                          (['term_checker.py', 'file.tmx'], False),
                          (['term_checker.py', 'file.tmx', 'file.txt'], False),
                          (['term_checker.py', 'file.txt', 'file.tmx', 'file.tmx'], False)
                          ])
def test_user_input_check(user_input, expected):
    assert term_checker.user_input_check(user_input) == expected


'''
Test extraction of glossary terms from txt file.
'''
def test_get_terminology():
    glossary_file = 'tests/test_glossary.txt'
    expected = ['技術分野	Technical Field',
                '背景技術	Related Art', 
                '発明の概要	Summary', 
                '発明が解決しようとする課題	Problem to be Solved by the Invention',
                '課題を解決するための手段	Means for Solving the Problem',
                '図面の簡単な説明	Brief Description of the Drawings',
                '発明を実施するための形態	Detailed Description',
                '特許請求の範囲	What is Claimed is:',
                '特許請求の範囲	patent claims',
                '要約書	Abstract',
                '実施形態	exemplary embodiment',
                '実施の形態	exemplary embodiment',
                '実施例	example',
                '従来技術	related art',
                '解決	address',
                '解決	solve',
                '解決	solution']
    terminology = term_checker.get_terminology(glossary_file)
    assert terminology == expected


'''
Test extraction of translation from tmx file.
'''
def test_get_translation():
    translation_file = 'tests/test_translation.tmx'
    expected = [('[図1]...を示す断面模式図である。', 
                 'Fig. 1 is a cross-sectional schematic view depicting ...'),
                ('[図2]...を説明する図である。', 
                 'Fig. 2 is a drawing illustrating ...'),
                ('[図3]...を示す断面模式図である。', 
                 'Fig. 3 is a cross-sectional schematic view depicting ...'),
                ('[図4]...を説明する図である。', 
                 'Fig. 4 is a drawing illustrating ...'),
                ('[図5]...を示す図である。', 
                 'Fig. 5 is a drawing depicting ...'),
                ('[図6]...を示す図である。', 
                 'Fig. 6 is a drawing depicting ...'),
                ('[図7]...を示す平面模式図である。', 
                 'Fig. 7 is a plan schematic view depicting ...')]
    segments = term_checker.get_translation(translation_file)
    translation = []
    for segment in segments:
        translation.append((segment.source_text, segment.target_text))
    assert translation == expected


'''
Test terminology checking funcionality.
'''
def test_check_translation():
    pass
