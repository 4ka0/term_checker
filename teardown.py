#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Script to teardown a completed translation project.
Tasks carried out include:
    Saving project master glossary local archive, desktop, and dropbox.

To execute:
python3 teardown.py project_folder

Typical project folder path:
/Volumes/Untitled/mac_local_jobs/projects/chizai/project_folder
'''

import os
import sys
import shutil
import zipfile
import xml.etree.ElementTree as ET


def save_glossary(project_path):
    '''
    Function to save master glossary in project folder to the archive,
    the desktop, and the honyaku dropboox folder.
    '''

    print("\nSaving glossary ...")

    # source paths
    project_glossary = project_path + "/draft/glossary/glossary.txt"
    master_glossary = project_path + "/draft/glossary/master glossary.txt"

    print("Project glossary = " + project_glossary)
    print("Master glossary = " + master_glossary)

    # extract content from project glossary
    with open(project_glossary, 'r') as input_file:
        project_glossary_content = input_file.readlines()

    print("Content extracted from project glossary.")

    # append project glossary content to master glossary
    with open(master_glossary, 'a') as output_file:
        output_file.writelines(project_glossary_content)

    print("Content added to master glossary.")
    print("Building destination paths.")

    # destination paths
    archive = "/Users/Jon/Documents/work_local/archive/glossary_reader/"\
              "glossary_files/master glossary.txt"
    desktop = "/Users/Jon/Desktop/master glossary.txt"
    dropbox = "/Users/Jon/Dropbox/honyaku/master glossary.txt"

    print("Archive destination = " + archive)
    print("Desktop destination = " + desktop)
    print("Dropbox destination = " + dropbox)

    # copy master glossary
    shutil.copyfile(master_glossary, archive)
    shutil.copyfile(master_glossary, desktop)
    shutil.copyfile(master_glossary, dropbox)

    print("Master glossary copied to archive, desktop, and "\
          "dropbox destinations.\n")


def save_tmx(project_path):
    '''
    Function to save the project tmx file to the archive.
    '''

    # destination path
    tmx_archive = "/Users/Jon/Documents/work_local/archive/tmx_vault"

    # local tmx file path
    tmx_file = project_path + "/draft/draft-omegat.tmx"

    # build a new name for the tmx file
    project_path_splits = project_path.split('/')
    folder = project_path_splits[-1]
    folder_splits = folder.split('_')
    new_name = folder_splits[0] + ' - ' + folder_splits[1] + '.tmx'

    # rename local tmx file and copy newly named tmx file across to archive
    os.rename(tmx_file, new_name)
    tmx_file = project_path + "/draft/" + new_name
    shutil.copy(tmx_file, tmx_archive)

    # call next function
    save_tmx_as_txt(tmx_file, new_name)


def save_tmx_as_txt(tmx_file, new_name):
    '''
    Function to save a txt version of the project tmx file to the
    glossary reader archive.
    '''

    # destination path
    txt_archive = "/Volumes/Untitled/mac_local_jobs/archive/" \
                  "glossary_reader/old_job_files/"

    # read in tmx file
    with open(tmx_file, 'rb') as f:
        tree = ET.parse(f)
    root = tree.getroot()
    tmx_content = []
    for tu in root.iter('tu'):
        jap = tu.find('tuv/[@lang="JA"]/seg').text
        eng = tu.find('tuv/[@lang="EN-US"]/seg').text
        tmx_content.append(jap + '\t' + eng)

    # write as txt file
    text_file_name = new_name.replace('.tmx', '.txt')
    save_path = txt_archive + text_file_name
    with open(save_path, 'w') as f:
        f.write(tmx_content)


def zip_project(project_path):
    '''
    Function to zip project folder and save in archive.
    '''

    # zip project folder
    newZip = zipfile.ZipFile('new.zip', 'w')
    newZip.write(project_path, compress_type=zipfile.ZIP_DEFLATED)
    newZip.close()

    # save zip file to archive

    # send current project to trash

    print('Teardown completed.')


def main():
    project_path = sys.argv[-1]
    save_glossary(project_path)
    # save_tmx(project_path)
    # zip_project(project_path)


if __name__ == '__main__':
    main()
