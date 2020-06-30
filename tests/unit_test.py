#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
import spacy

from .. import term_checker
from ..term_checker import Segment


GLOSSARY_FILE_1 = 'tests/test_glossary_1.txt'
GLOSSARY_FILE_2 = 'tests/test_glossary_2.txt'
TRANSLATION_FILE_1 = 'tests/test_translation_1.tmx'
TRANSLATION_FILE_2 = 'tests/test_translation_2.tmx'

nlp = term_checker.setup_tokenizer()


def test_constructor():
    s = Segment('なお、正孔輸送層12は、NiO、（またはMoO3）等の無機材料を...',
                'Moreover, the positive  hole transport layers 12 may...',
                {}, {})
    assert isinstance(s, Segment)


@pytest.mark.parametrize('user_input,expected', [
                          (['term_checker.py', 'file.tmx', 'file.txt'], True),
                          (['term_checker.py'], False),
                          (['term_checker.py', 'file.txt'], False),
                          (['term_checker.py', 'file.tmx'], False),
                          (['term_checker.py', 'file.txt', 'file.tmx'], False),
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
                '*特許	patent	patent\n',
                '*断面模式図	cross-sectional schematic view\n',
                '*平面模式図	plan schematic view']
    terminology = term_checker.get_terminology(GLOSSARY_FILE_1)
    assert terminology == expected


def test_clean_lines():
    input = [' 技術分野	Technical Field  \n',
             '  背景技術	Related Art  \n',
             '   発明の概要	Summary \n',
             '    発明の概要	Summary \n',
             '      課題	Problem  \n',
             ' *手段	Means \n',
             '   *図面の簡単な説明	Brief Description of the Drawings \n',
             '*発明を実施するための形態	Detailed Description   \n',
             '*特許請求の範囲	What is Claimed is:	\n',
             '*特許請求の範囲	patent claims	\n']
    expected = ['技術分野	Technical Field',
                '背景技術	Related Art',
                '発明の概要	Summary',
                '発明の概要	Summary',
                '課題	Problem',
                '手段	Means',
                '図面の簡単な説明	Brief Description of the Drawings',
                '発明を実施するための形態	Detailed Description',
                '特許請求の範囲	What is Claimed is:',
                '特許請求の範囲	patent claims']
    output = term_checker.clean_lines(input)
    assert output == expected


def test_format_check():
    input = ['技術分野	Technical Field',
             '背景技術	Related Art',
             '発明の概要	Summary',
             '発明の概要	Summary',
             '課題	Problem',
             '手段, Means',
             '図面の簡単な説明',
             '発明を実施するための形態,Detailed Description',
             '特許請求の範囲	What is Claimed is:	patent claims',
             '特許請求の範囲/patent claims/claims']
    expected = ['技術分野	Technical Field',
                '背景技術	Related Art',
                '発明の概要	Summary',
                '発明の概要	Summary',
                '課題	Problem']
    ouput = term_checker.format_check(input)
    assert ouput == expected


def test_remove_duplicates():
    input = ['技術分野	Technical Field',
             '背景技術	Related Art',
             '発明の概要	Summary',
             '発明の概要	Summary',
             '発明の概要	Summary',
             '課題	Problem',
             '手段	Means',
             '図面の簡単な説明	Brief Description of the Drawings',
             '図面の簡単な説明	Brief Description of the Drawings',
             '発明を実施するための形態	Detailed Description',
             '特許請求の範囲	What is Claimed is:',
             '特許請求の範囲	patent claims']
    expected = ['技術分野	Technical Field',
                '背景技術	Related Art',
                '発明の概要	Summary',
                '課題	Problem',
                '手段	Means',
                '図面の簡単な説明	Brief Description of the Drawings',
                '発明を実施するための形態	Detailed Description',
                '特許請求の範囲	What is Claimed is:',
                '特許請求の範囲	patent claims']
    output = term_checker.remove_duplicates(input)
    assert output == expected


def test_group_terminology():
    input = ['技術分野	Technical Field',
             '発明の概要	Summary',
             '特許請求の範囲	What is Claimed is:',
             '特許請求の範囲	patent claims',
             '要約書	Abstract',
             '実施形態	exemplary embodiment',
             '実施の形態	exemplary embodiment',
             '解決	address',
             '解決	solve',
             '解決	solution',
             '装置	device',
             '装置	apparatus',
             'つまり	that is',
             'つまり	in other words',
             'つまり	namely',
             'つまり	specifically',
             '断面模式図	cross-sectional schematic view',
             '平面模式図	plan schematic view']
    expected = {'技術分野': ['Technical Field'],
                '発明の概要': ['Summary'],
                '特許請求の範囲': ['What is Claimed is:', 'patent claims'],
                '要約書': ['Abstract'],
                '実施形態': ['exemplary embodiment'],
                '実施の形態': ['exemplary embodiment'],
                '解決': ['address', 'solve', 'solution'],
                '装置': ['device', 'apparatus'],
                'つまり': ['that is', 'in other words', 'namely', 'specifically'],
                '断面模式図': ['cross-sectional schematic view'],
                '平面模式図': ['plan schematic view']}
    output = term_checker.group_terminology(input)
    assert output == expected


def test_get_translation():
    expected = [('[図1]...を示す断面模式図である。',
                 'Fig. 1 is a schematic view depicting ...'),
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
                 'Fig. 7 is a plan schematic depicting ...')]
    segments = term_checker.get_translation(TRANSLATION_FILE_1)
    output = []
    for segment in segments:
        output.append((segment.source_text, segment.target_text))
    assert output == expected


def test_basic_check():
    terminology = {'技術分野': ['Technical Field'],
                   '発明の概要': ['Summary'],
                   '特許請求の範囲': ['What is Claimed is:', 'patent claims'],
                   '要約書': ['Abstract'],
                   '実施形態': ['exemplary embodiment'],
                   '実施の形態': ['exemplary embodiment'],
                   '解決': ['address', 'solve', 'solution'],
                   '装置': ['device', 'apparatus'],
                   '断面模式図': ['cross-sectional schematic view'],
                   '平面模式図': ['plan schematic view']}
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
    translation = term_checker.get_translation(TRANSLATION_FILE_1)
    checked_trans, missing = term_checker.basic_check(terminology, translation)
    # Extract content from Segment objects for assertion comparison
    output = []
    for seg in checked_trans:
        output.append((seg.source_text, seg.target_text, seg.missing_terms))
    assert output == expected


def test_lemma_check():
    pass


@pytest.mark.parametrize('user_input,expected', [
                          ('device', 'device'),
                          ('devices', 'device'),
                          ('printing devices', 'printing device'),
                          ('information processing devices', 'information processing device'),
                          ('exemplary embodiments', 'exemplary embodiment'),
                          ('cross-sectional views', 'cross-sectional view')
                          ])
def test_get_lemma(user_input, expected):
    assert term_checker.get_lemma(user_input, nlp) == expected


def test_target_search():
    # Test 1 - positive
    target_term_lemma = 'information processing device'
    target_text = 'The information processing devices 10B receive the request, and then store the functional information related to the function 2 in the storage unit and validates display of the function 2.'
    found = term_checker.target_search(target_term_lemma, target_text, nlp)
    assert found
    # Test 2 - positive
    target_term_lemma = 'image printing device'
    target_text = 'The information processing devices 10B receive the request, and then store the functional information related to the function 2 in the image printing device and validates display of the function 2.'
    found = term_checker.target_search(target_term_lemma, target_text, nlp)
    assert found
    # Test 3 - positive
    target_term_lemma = 'cross-sectional schematic view'
    target_text = 'Fig. 3 is a cross-sectional schematic view depicting...'
    found = term_checker.target_search(target_term_lemma, target_text, nlp)
    assert found
    # Test 4 - positive
    target_term_lemma = 'suppress'
    target_text = 'Thus, in an online delivery system which uses an automatic driving vehicle, although the time and labor for the recipient increases, a delivery company driver is not required and therefore driver labor costs can be suppressed.'
    found = term_checker.target_search(target_term_lemma, target_text, nlp)
    assert found
    # Test 5 - positive
    target_term_lemma = 'transmit'
    target_text = 'The device is not usually transmitting at this time.'
    found = term_checker.target_search(target_term_lemma, target_text, nlp)
    assert found
    # Test 6 - negative
    target_term_lemma = 'color image device'
    target_text = 'Therefore, many color imaging devices acquire information regarding R, G, and B using one image sensor.'
    found = term_checker.target_search(target_term_lemma, target_text, nlp)
    assert not found
    # Test 7 - negative
    target_term_lemma = 'connect'
    target_text = 'The magnetic connector system as claimed in claim 28, further including a first connector.'
    found = term_checker.target_search(target_term_lemma, target_text, nlp)
    assert not found
    # Test 8 - negative
    target_term_lemma = 'number'
    target_text = 'In one example, the setting temperatures Setting_temp[i] (1 ≤ i ≤ n) are decided using the aforementioned numerical expression (2) only for air conditioners'
    found = term_checker.target_search(target_term_lemma, target_text, nlp)
    assert not found
    # Test 9 - negative
    target_term_lemma = 'digit'
    target_text = 'By carrying out digital image processing for selecting and integrating pixels, color images can be generated with the images transmitted through the two regions 1202 being separated.'
    found = term_checker.target_search(target_term_lemma, target_text, nlp)
    assert not found
    # Test 10 - negative
    target_term_lemma = 'transmit'
    target_text = 'Fig. 5 is a drawing depicting transmittance as a wavelength characteristic of three types of filters according to an embodiment;'
    found = term_checker.target_search(target_term_lemma, target_text, nlp)
    assert not found


def test_check_hyphenated():
    terminology = {'技術分野': ['Technical Field'],
                   '発明の概要': ['Summary'],
                   '特許請求の範囲': ['What is Claimed is:'],
                   '要約書': ['Abstract'],
                   '実施形態': ['exemplary embodiment'],
                   '解決': ['address'],
                   '装置': ['device'],
                   '印刷装置': ['printing device'],
                   '撮影装置': ['photography device']}
    expected = [('技術分野', 'Technical-Field',
                 {'技術分野': ['Technical Field']},
                 {'技術分野': 'Technical-Field'}),
                ('発明の概要',
                 'Summary',
                 {}, {}),
                ('特許請求の範囲',
                 'What is Claimed is:',
                 {}, {}),
                ('要約書',
                 'Abstract',
                 {}, {}),
                ('実施形態',
                 'Another exemplary-embodiment.',
                 {'実施形態': ['exemplary embodiment']},
                 {'実施形態': 'exemplary-embodiment'}),
                ('解決',
                 'Address',
                 {}, {}),
                ('印刷装置',
                 'A printing-device.',
                 {'印刷装置': ['printing device']},
                 {'印刷装置': 'printing-device'})]
    raw_trans = term_checker.get_translation(TRANSLATION_FILE_2)
    checked_trans, missing = term_checker.basic_check(terminology, raw_trans)
    rechecked_trans = term_checker.hyphen_check(terminology, checked_trans)
    # Extract content from Segment objects for assertion comparison
    output = []
    for seg in rechecked_trans:
        output.append((seg.source_text, seg.target_text,
                       seg.missing_terms, seg.hyphenated_forms))
    assert output == expected
