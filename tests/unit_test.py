#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
import spacy
from spacy.tokenizer import Tokenizer
from spacy.util import compile_infix_regex

from .. import term_checker
from ..term_checker import Segment


GLOSSARY_FILE_1 = 'tests/test_glossary_1.txt'
GLOSSARY_FILE_2 = 'tests/test_glossary_2.txt'
TRANSLATION_FILE_1 = 'tests/test_translation_1.tmx'
TRANSLATION_FILE_2 = 'tests/test_translation_2.tmx'
TRANSLATION_FILE_3 = 'tests/test_translation_3.tmx'

nlp = term_checker.setup_tokenizer()


# Test for instantiating Segment():
def test_constructor():
    s = Segment('なお、正孔輸送層12は、NiO、（またはMoO3）等の無機材料を...',
                'Moreover, the positive  hole transport layers 12 may...',
                {}, {})
    assert isinstance(s, Segment)


# Test for the user input check
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


# Testing obtaining terminology from the glossary file
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


# Testing cleaning of the input from the glossary file
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


# Testing checking of the format of the glossary content
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


# Testing removal of duplicates in glossary content
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


# Testing sorting of the glossary content
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


# Testing obtaining translation segments from a tmx file
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


# Testing the basic check of the glossary against the translation
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

    output = []
    for seg in checked_trans:
        output.append((seg.source_text, seg.target_text, seg.missing_terms))

    assert output == expected


# Testing obtaining the lemma form of a term
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


# Testing searching target text for the lemma form of a term
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


# Testing the lemma-based check of the glossary against the translation
def test_lemma_check():

    terminology = {'複合機': ['multifunction device'],
                   'バックアップ処理': ['backup processing'],
                   'クラウドサーバ': ['cloud server'],
                   '機器登録部': ['device registration unit'],
                   '設定バックアップメニュー画面': ['setting backup menu screen'],
                   '実施形態': ['exemplary embodiment'],
                   '事務所': ['office'],
                   'リストア処理': ['restoration processing'],
                   '遠隔操作端末': ['remote operation terminal'],
                   '新機種の複合機': ['new-model multifunction device']}

    expected = [('その場合、旧機種の複合機200Aの設定情報をクラウドサーバ100に一旦バックアップし、当該クラウドサーバ100にバックアップされた設定情報を新機種の複合機200Bにリストアするなら、新機種の複合機200Bにおいて最初から設定をやり直す必要がなくなる。',
                 'In such cases, if the setting information of the old-model multifunction device 200A is temporarily backed up to the cloud server 100 and the setting information backed up to the cloud server 100 is restored in the new-model multifunction device 200B, it is no longer necessary for settings to be implemented again from the beginning in the new-model multifunction device 200B.',
                 {}),
                ('したがって、バックアップ処理を行うつもりのない他の複合機は、この一覧には表示されない。',
                 'Consequently, other multifunction devices for which there is no intention to carry out backup processing are not displayed in this list.',
                 {}),
                ('なお、バックアップ／リストア処理に先立ってクラウドサーバ100はオーダー番号を発行しており、このオーダー番号はこの登録処理を行うカスタマーエンジニアつまりテナントと予め対応付けられているものとする。',
                 'It should be noted that the cloud servers 100 issue an order number prior to the backup/restoration processing, and this order number is associated in advance with a customer engineer who carries out this registration processing, namely a tenant.',
                 {}),
                ('なお、上記実施形態においては、クラウドサーバ100の機器登録部115にオーダー番号が複合機200のユーザインタフェース205から直接入力されたときのみオーダー番号と機器情報とを対応付けて登録することを許可する機能を設け、また、複合機200の機器情報送信部212にも、オーダー番号が本複合機200のユーザインタフェース205から直接入力されたとき以外には、機器情報の送信処理を禁止する機能を設けた例を説明したが、本発明は、クラウドサーバ100と複合機200のいずれか一方に上述の機能を設けるようにしてもよい。',
                 'In the aforementioned embodiment, an example has been described in which the device registration unit 115 of the cloud server 100 is provided with a function to permit an order number and device information to be associated and registered only when an order number is input directly from the user interface device 205 of the multifunction device 200, and the device information transmission unit 212 of the multifunction device 200 is also provided with a function to prohibit transmission processing for device information apart from when an order number is input directly from the user interface device 205 of the multifunction device 200. However, it should be noted that the present disclosure may be implemented in such a way that the aforementioned functions are provided in either one of the cloud server 100 and the multifunction device 200.',
                 {'実施形態': ['exemplary embodiment']}),
                ('なお、図7（B）の設定バックアップメニュー画面703は、図6（C）の設定バックアップメニュー画面604よりも表示される項目が少なくなっている。',
                 'It should be noted that the setting backup screens 703 of Fig. 7B has less displayed items compared to the setting backup screen 604 of Fig. 6C.',
                 {'設定バックアップメニュー画面': ['setting backup menu screen']}),
                ('なお、本実施形態においては、遠隔操作端末300の表示装置に表示される画像はクラウドサーバ100の制御部114が生成するウェブユーザインタフェースとして提供されるものであり、遠隔操作端末300は、単にクラウドサーバ100のいわばユーザインタフェースとして使用されるに過ぎない。',
                 'It should be noted that, in the present exemplary embodiment, images displayed on the display device of the remote terminal 300 are provided as a web user interface generated by the controller 114 of the cloud servers 100, and the remote terminal 300 is merely used simply as a user interface so to speak for the cloud server 100.',
                 {'遠隔操作端末': ['remote operation terminal']})]

    raw_trans = term_checker.get_translation(TRANSLATION_FILE_3)
    checked_trans, missing = term_checker.basic_check(terminology, raw_trans)
    translation = term_checker.lemma_check(nlp, terminology, checked_trans)
    output = []
    for seg in translation:
        output.append((seg.source_text, seg.target_text, seg.missing_terms))
    assert output == expected


# Testing searching for the hyphenated form of a term
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

    output = []
    for seg in rechecked_trans:
        output.append((seg.source_text, seg.target_text,
                       seg.missing_terms, seg.hyphenated_forms))
                       
    assert output == expected
