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
                'moreover, the positive  hole transport layers 12 may...',
                {})
    assert isinstance(s, Segment)


'''
Test user input verification.
'''
@pytest.mark.parametrize('user_input,expected',
                         [(['checker.py', 'test.tmx'], True),
                          (['checker.py'], False),
                          (['checker.py', 'test1.tmx', 'test2.tmx'], False),
                          (['checker.py', 'test1.txt'], False)])
def test_user_input_check(user_input, expected):
    assert term_checker.user_input_check(user_input) == expected


'''
Test extraction of glossary terms from txt file.
'''
def test_get_terminology():
    pass


'''
Test extraction of translation from tmx file.
'''
def test_get_translation():
    pass


'''
Test terminology checking funcionality.
'''
def test_check_translation():
    pass
