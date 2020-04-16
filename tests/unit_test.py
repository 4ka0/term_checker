#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from .. import term_checker
from ..term_checker import Segment


GLOSSARY_FILE = 'tests/test_glossary.txt'
TRANSLATION_FILE = 'tests/test_translation.tmx'


def test_constructor():
    s = Segment('なお、正孔輸送層12は、NiO、（またはMoO3）等の無機材料を...',
                'Moreover, the positive  hole transport layers 12 may...',
                {})
    assert isinstance(s, Segment)


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


def test_get_terminology():
    expected = ['*技術分野	Technical Field\n',
                '*背景技術	Related Art\n', 
                '*発明の概要	Summary\n', 
                '*発明の概要	Summary\n', 
                '*発明が解決しようとする課題	Problem to be Solved by the Invention\n',
                '*課題を解決するための手段	Means for Solving the Problem\n',
                '*図面の簡単な説明	Brief Description of the Drawings\n',
                '*発明を実施するための形態	Detailed Description\n',
                '*特許請求の範囲	What is Claimed is:\n',
                '*特許請求の範囲	patent claims\n',
                '*要約書	Abstract\n',
                '*要約書	Abstract\n',
                '*要約書	Abstract\n',
                '*実施形態	exemplary embodiment\n',
                '*実施の形態	exemplary embodiment\n',
                '*実施例	example\n',
                '*従来技術	related art\n',
                '*解決	address\n',
                '*解決	solve\n',
                '*解決	solution\n',
                '*装置	device	apparatus\n',
                '*特許	patent	patent']
    terminology = term_checker.get_terminology(GLOSSARY_FILE)
    assert terminology == expected


def test_clean_lines():
    expected = ['技術分野	Technical Field',
                '背景技術	Related Art', 
                '発明の概要	Summary', 
                '発明の概要	Summary', 
                '発明が解決しようとする課題	Problem to be Solved by the Invention',
                '課題を解決するための手段	Means for Solving the Problem',
                '図面の簡単な説明	Brief Description of the Drawings',
                '発明を実施するための形態	Detailed Description',
                '特許請求の範囲	What is Claimed is:',
                '特許請求の範囲	patent claims',
                '要約書	Abstract',
                '要約書	Abstract',
                '要約書	Abstract',
                '実施形態	exemplary embodiment',
                '実施の形態	exemplary embodiment',
                '実施例	example',
                '従来技術	related art',
                '解決	address',
                '解決	solve',
                '解決	solution',
                '装置	device	apparatus',
                '特許	patent	patent']
    terminology = term_checker.get_terminology(GLOSSARY_FILE)
    terminology = term_checker.clean_lines(terminology)
    assert terminology == expected


def test_format_check():
    expected = ['技術分野	Technical Field',
                '背景技術	Related Art', 
                '発明の概要	Summary', 
                '発明の概要	Summary', 
                '発明が解決しようとする課題	Problem to be Solved by the Invention',
                '課題を解決するための手段	Means for Solving the Problem',
                '図面の簡単な説明	Brief Description of the Drawings',
                '発明を実施するための形態	Detailed Description',
                '特許請求の範囲	What is Claimed is:',
                '特許請求の範囲	patent claims',
                '要約書	Abstract',
                '要約書	Abstract',
                '要約書	Abstract',
                '実施形態	exemplary embodiment',
                '実施の形態	exemplary embodiment',
                '実施例	example',
                '従来技術	related art',
                '解決	address',
                '解決	solve',
                '解決	solution']
    terminology = term_checker.get_terminology(GLOSSARY_FILE)
    terminology = term_checker.clean_lines(terminology)
    terminology = term_checker.format_check(terminology)
    assert terminology == expected


def test_remove_duplicates():
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
    terminology = term_checker.get_terminology(GLOSSARY_FILE)
    terminology = term_checker.clean_lines(terminology)
    terminology = term_checker.format_check(terminology)
    terminology = term_checker.remove_duplicates(terminology)
    assert terminology == expected


def test_group_terminology():
    pass


def test_get_translation():
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
    segments = term_checker.get_translation(TRANSLATION_FILE)
    translation = []
    for segment in segments:
        translation.append((segment.source_text, segment.target_text))
    assert translation == expected


def test_check_translation():
    pass
