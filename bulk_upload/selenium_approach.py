#!/usr/bin/env python
#
# Authors:
#  Shaun Patterson
#  Colin Johnson
#
#
# To run headless:
#
# Xvfb :10 -ac
# export DISPLAY=:10
#
# then run as normal

import os
import uuid
import zipfile
import glob
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import sys, time
from datetime import date, timedelta
import datetime
import shutil
import traceback
from collections import OrderedDict

def login(fox, username, password):
    fox.get('https://www.lingq.com/accounts/login/')
    fox.find_element_by_id('id_username').send_keys(username)
    fox.find_element_by_id('id_password').send_keys(password)
    fox.find_element_by_id('submit-button').click()
    
    # Terrible.  But terribly effective for lazy people
    # Really need to find a way to make sure the page is fully loaded...
    time.sleep(10)
    
def createLesson(fox, lang, collectionId, lessonName, lessonText):
    fox.get("http://www.lingq.com/learn/%s/import/contents/?add=&collection=%s" % (lang, collectionId))
    fox.find_element_by_id('id_title').send_keys(lessonName)

    fox.switch_to_frame('id_text_ifr')
    body = fox.find_element_by_tag_name('body')
    fox.execute_script("arguments[0].innerHTML = '<p>{}</p>'".format(lessonText.strip()), body)

    # Back to the original frame
    fox.switch_to_default_content()

    saveButton = fox.find_element_by_class_name('save-button')
    saveButton.click()

    # Cry me a river
    time.sleep(10)

 
def loadFromZip(zipFileName):
    # Extract the zip into a tmp directory in the current path
    folderName = str(uuid.uuid1())
    print folderName

    with zipfile.ZipFile(zipFileName) as zf:
        zf.extractall(folderName)
    
    lessonFilenames = sorted(os.listdir(folderName))
    
    # Not the best way... but it's the way I'm doing it
    # You should be able to just read the files out of the zip without extracting to
    #  a temp directory.  Maybe in version 2...
    # LessonName(filename) -> Lesson Text
    lessons = OrderedDict()
    for lessonFilename in lessonFilenames:
        path = os.path.join(folderName, lessonFilename)
        if not os.path.isfile(path):
            continue

        with open(path) as f:
            lessonTextList = f.readlines()
            lessonText = '<br/>'.join([ x.strip() for x in lessonTextList ])
            lessonText = lessonText.replace("'", r"\'")
            lessonName = os.path.splitext(lessonFilename)[0]
            lessons[lessonName] = lessonText

    #print lessons
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
        lessonText = '<br/>'.join([ x.strip() for x in lessonTextList ])
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
    (blank, username, password, lang, collectionId) = sys.argv[:5]

    if len(sys.argv) == 6:
        # zip file name
        zipFileName = sys.argv[5]
        lessons = loadFromZip(zipFileName)
    elif len(sys.argv) == 7:
        (bookFileName, headerFileName) = (sys.argv[5:])
        lessons = loadFromFileAndHeader(bookFileName, headerFileName)
    else:
        print "Usage"
        return
    
    profile = webdriver.FirefoxProfile()
    fox = webdriver.Firefox(profile)
    
    print "Logging in"
    login(fox, username, password)

    print "Creating lessons"
    
    for lessonName, lessonText in lessons.iteritems():
        createLesson(fox, lang, collectionId, lessonName, lessonText);

    fox.quit()

if __name__ == "__main__":
    main()
