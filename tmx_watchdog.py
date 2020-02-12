#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Script to monitor translation archive for the addition of new tmx files.
If a new tmx is added to a translation archive folder, the file is converted
to a txt file and saved in a glossary folder.
'''

import sys
import time
import xml.etree.ElementTree as ET
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


folder_to_track = "/Users/Jon/Work/work_local/archive/tmx_vault"
copy_destination = "/Users/Jon/Work/work_local/archive/glossary_reader/old_job_files/"


class EventHandler(FileSystemEventHandler):
    '''
    Event handler looking specifically for new files.
    '''
    def on_created(self, event):
        new_file = event.src_path
        if new_file.endswith('.tmx'):
            convert_tmx(new_file)


class Pair():
    '''
    Class for each segment extracted from a tmx file.
    Contains source text and target text.
    '''
    def __init__(self, source_text = '', target_text = ''):
        self.source_text = source_text
        self.target_text = target_text


def convert_tmx(new_file):
    '''
    Function to convert tmx file to txt file.
    '''
    tree = ET.parse(new_file)
    root = tree.getroot()
    header = root.find('./header')
    source_lang = header.get('srclang')
    seg_pairs = [] 

    # Parsing the tmx file.
    for tu in root.iter("tu"):
        target_lang = ''
        source_text = ''
        target_text = ''

        # Any children present? Should be two 'tuv' nodes
        if len(tu) > 0:

            for child in tu:

                # Only look at 'tuv' children
                if child.tag == 'tuv':

                    # Get language
                    lang = child.get('lang')

                    # Set target language if appropriate
                    if lang != source_lang:
                        target_lang = lang

                    # Any children present? Should be one 'seg' node
                    if len(child) > 0:

                        for subchild in child:

                            # Only look at 'seg' child nodes
                            if subchild.tag == 'seg':

                                # Source or target text? Check if text exists.
                                # If not, assign empty string to avoid 'None'
                                # being assigned.
                                if target_lang == '':
                                    if subchild.text:
                                        source_text = subchild.text
                                    else:
                                        source_text = ''
                                else:
                                    if subchild.text:
                                        target_text = subchild.text
                                    else:
                                        target_text = ''

        segs = Pair(source_text, target_text)
        seg_pairs.append(segs)

    file_splits = new_file.split('/')
    tmx_file = file_splits[-1]
    txt_file = tmx_file.replace('.tmx', '.txt')
    save_path = copy_destination + txt_file
    
    with open(save_path, 'w') as f:
        for pair in seg_pairs:
            f.write(pair.source_text + '\t' + pair.target_text + '\n')


def main():
    event_handler = EventHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_to_track, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
