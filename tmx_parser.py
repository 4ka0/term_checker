#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''
Basic parser for tmx (translation memory exchange) files.

Basic tmx structure:

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE tmx SYSTEM "tmx11.dtd">
<tmx version="1.1">
    <header creationtool="OmegaT" o-tmf="OmegaT TMX" adminlang="EN-US" datatype="plaintext" creationtoolversion="3.0.8_3" segtype="sentence" srclang="JA"/>
    <body>
    <tu>
        <tuv lang="JA">
            <seg>変換部5の画像変換処理(1)</seg>
        </tuv>
        <tuv lang="EN-US" ... >
            <seg>Image conversion processing (1) of the conversion unit 5</seg>
        </tuv>
    </tu>
'''

import xml.etree.ElementTree as ET


def main():

    # Change path as necessary
    tree = ET.parse('/Volumes/Untitled/test1.tmx')
    root = tree.getroot()

    # Get source language
    header = root.find('./header')
    source_lang = header.get('srclang')
    print(source_lang)

    # Look at each tu node
    for tu in root.iter('tu'):

        print('++++++++++++++++++++++++++++++++++++')

        # Any children present?
        if len(tu) > 0:

            for child in tu:

                # Only look at tuv child nodes
                if child.tag == 'tuv':

                    # Get language
                    print('lang = ' + child.get('lang'))

                    # Any children present?
                    if len(child) > 0:

                        for subchild in child:

                            if subchild.tag == 'seg':

                                print(subchild.text)


if __name__ == '__main__':
    main()
