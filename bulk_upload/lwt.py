#!/usr/bin/env python
#
# Authors:
#  Shaun Patterson
#  Colin Johnson
#

import os
import uuid
import zipfile
import glob
import sys, time
from datetime import date, timedelta
import datetime
import shutil
import traceback
from collections import OrderedDict
import argparse

import requests

def createLesson(lessonName, lessonText, tag):
    url = 'http://localhost/lwt/edit_texts.php'

    data = {}
    data['op'] = "Save"
    data['TxLgID'] = "1"
    data['TxTitle'] = lessonName
    data['TxText'] = lessonText
    data['TxSourceURI'] = ''
    data['TextTags[TagList][]'] = tag
    data['TxAudioURI'] = ''

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.post(url, data=data, headers=headers)
    #r = requests.post('http://httpbin.org/post', data=data, headers=headers)
    #print r.text


def loadFromFile(fileName, lessonName):
    # LessonName(filename) -> Lesson Text
    lessons = OrderedDict()
    with open(fileName) as f:
        lessonTextList = f.readlines()
        lessonText = "\n".join([ x.strip() for x in lessonTextList ])
        lessonText = lessonText.replace("'", r"\'")
        lessons[lessonName] = lessonText
    
    return lessons
    


def loadFromDir(dirName):
    lessonFilenames = sorted(os.listdir(dirName))
    
    # Not the best way... but it's the way I'm doing it
    # You should be able to just read the files out of the zip without extracting to
    #  a temp directory.  Maybe in version 2...
    # LessonName(filename) -> Lesson Text
    lessons = OrderedDict()
    for lessonFilename in lessonFilenames:
        path = os.path.join(dirName, lessonFilename)
        if not os.path.isfile(path):
            continue

        with open(path) as f:
            lessonTextList = f.readlines()
            lessonText = "\n".join([ x.strip() for x in lessonTextList ])
            lessonText = lessonText.replace("'", r"\'")
            lessonName = os.path.splitext(lessonFilename)[0]
            lessons[lessonName] = lessonText

    return lessons
 
def loadFromZip(zipFileName):
    # Extract the zip into a tmp directory in the current path
    folderName = str(uuid.uuid1())
    print folderName

    with zipfile.ZipFile(zipFileName) as zf:
        zf.extractall(folderName)
    
    lessons = loadFromDir(folderName)

    # Clean up the zip
    shutil.rmtree(folderName)
    return lessons
    

# Book file contains ALL the text for the book.  Each lesson break is signaled with a 
#  NEW_CHAPTER line.
# Exceptionally long chapters can be broken up using BREAK_CHAPTER
# The header file contains a list of the names of each chapter
# There must be N header lines and N-2 NEW_CHAPTERs for this to work correctly
#  (First chapter does not need an initial NEW_CHAPTER. Last chapter does not need
#   trailing NEW_CHAPTER)
def loadFromFileAndHeader(bookFileName, headerFileName):
    with open(bookFileName) as f:
        lessonTextList = f.readlines()
        lessonText = '\n'.join([ x.strip() for x in lessonTextList ])
        lessonText = lessonText.replace("'", r"\'")
        lessonTexts = lessonText.split("NEW_CHAPTER")
     
    with open(headerFileName) as f:
        lessonTitleList = f.readlines()
     
    lessons = OrderedDict()
             
    counter = 0
    for lessonText in lessonTexts:
        lessonWords = lessonText.split()
        lessonTitle = lessonTitleList[counter].strip()
         
        if any("BREAK_CHAPTER" in s for s in lessonWords):     
            # Chapter is broken up into smaller chapters
            lessonTexts2 = lessonText.split("BREAK_CHAPTER")
             
            counter2 = 1
            for lessonText2 in lessonTexts2:
                lessonTitle2 = "%s_%s" % (lessonTitle, counter2)
                lessons[lessonTitle2] = lessonText2
                counter2+=1
                 
                lessonWords = lessonText2.split()
                print "Make lesson %s with nwords %d" % (lessonTitle2, len(lessonWords))

        else:
            # Full chapter 
            lessons[lessonTitle] = lessonText
            print "Make lesson %s with nwords %d" % (lessonTitle, len(lessonWords))
 
        counter+=1

    #print lessons
    return lessons


def main():
    parser = argparse.ArgumentParser()
    inputGroup = parser.add_mutually_exclusive_group()
    inputGroup.add_argument('-z', '--zip', type=str)
    inputGroup.add_argument('-d', '--dir', type=str)
    inputGroup.add_argument('-b', '--book', type=str, action='store', nargs='*')
    inputGroup.add_argument('-f', '--file', type=str, action='store', nargs='*')
    outputGroup = parser.add_mutually_exclusive_group()
    outputGroup.add_argument('--test', action='store_true')    # Trial run. No upload
    parser.add_argument('-t', '--tag', type=str)
    args = parser.parse_args()
    
    if args.zip:
        print args.zip
        lessons = loadFromZip(args.zip)
    elif args.dir:
        print args.dir
        lessons = loadFromDir(args.dir)
    elif args.book:
        bookFileName = args.book[0]
        headerFileName = args.book[1]
        lessons = loadFromFileAndHeader(bookFileName, headerFileName)
    elif args.file:
        fileName = args.file[0]
        lessonName = args.file[1]
        lessons = loadFromFile(fileName, lessonName)
    else:
        return
   

    print "Creating lessons"
    for lessonName, lessonText in lessons.iteritems():
        if args.test:
            print lessonName
        else:
            createLesson(lessonName, lessonText, args.tag)


if __name__ == "__main__":
    main()
