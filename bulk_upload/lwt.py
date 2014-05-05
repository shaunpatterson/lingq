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

def createLesson(fox, lessonName, lessonText, tags):
    fox.get('http://localhost/lwt/long_text_import.php')

    titleField = fox.find_element_by_css_selector('.tab3 > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > input:nth-child(1)')
    titleField.send_keys(lessonName)

    textField = fox.find_element_by_css_selector('.tab3 > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2) > textarea:nth-child(9)')
    fox.execute_script("arguments[0].value = '{}'".format(lessonText.strip()), textField)

    fox.find_element_by_css_selector('.posintnumber').send_keys('999')
    fox.find_element_by_css_selector('html body form.validate table.tab3 tbody tr td.td1 ul#texttags.tagit li.tagit-new input.ui-widget-content').send_keys(tags)

    # Click next button
    fox.find_element_by_css_selector('.tab3 > tbody:nth-child(1) > tr:nth-child(8) > td:nth-child(1) > input:nth-child(2)').click()
    time.sleep(3)

    # Click "Create X text button"
    fox.find_element_by_css_selector('.tab3 > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > input:nth-child(3)').click()

    time.sleep(3)
 
def loadFromZip(zipFileName):
    #lessons = OrderedDict()
    #with open('current.srt') as f:
        #lessonTextList = f.readlines()
        #lessonText = "\\n".join([ x.strip() for x in lessonTextList ])
        #lessonText = lessonText.replace("'", r"\'")
        #print lessonText
        #lessonName = os.path.splitext('test')[0]
        #lessons[lessonName] = lessonText
    #return lessons



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
            lessonText = "\\n".join([ x.strip() for x in lessonTextList ])
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
    pass
    # Todo
    #with open(bookFileName) as f:
        #lessonTextList = f.readlines()
        #lessonText = '<br/>'.join([ x.strip() for x in lessonTextList ])
        #lessonText = lessonText.replace("'", r"\'")
        #lessonTexts = lessonText.split("NEW_CHAPTER")
     
    #with open(headerFileName) as f:
        #lessonTitleList = f.readlines()
     
    #lessons = OrderedDict()
             
    #counter = 0
    #for lessonText in lessonTexts:
        #lessonWords = lessonText.split()
        #lessonTitle = lessonTitleList[counter].strip()
         
        #if any("BREAK_CHAPTER" in s for s in lessonWords):     
            ## Chapter is broken up into smaller chapters
            #lessonTexts2 = lessonText.split("BREAK_CHAPTER")
             
            #counter2 = 1
            #for lessonText2 in lessonTexts2:
                #lessonTitle2 = "%s_%s" % (lessonTitle, counter2)
                #lessons[lessonTitle2] = lessonText2
                #counter2+=1
                 
                #lessonWords = lessonText2.split()
                #print "Make lesson %s with nwords %d" % (lessonTitle2, len(lessonWords))

        #else:
            ## Full chapter 
            #lessons[lessonTitle] = lessonText
            #print "Make lesson %s with nwords %d" % (lessonTitle, len(lessonWords))
 
        #counter+=1

    ##print lessons
    #return lessons


def main():
    if len(sys.argv) == 3:
        # zip file name
        zipFileName = sys.argv[1]
        tag = sys.argv[2]
        lessons = loadFromZip(zipFileName)
    elif len(sys.argv) == 4:
        (bookFileName, headerFileName, tag) = (sys.argv[1:])
        lessons = loadFromFileAndHeader(bookFileName, headerFileName)
    else:
        print "Usage"
        return
    
    profile = webdriver.FirefoxProfile()
    fox = webdriver.Firefox(profile)
    
    print "Creating lessons"
    for lessonName, lessonText in lessons.iteritems():
        createLesson(fox, lessonName, lessonText, tag)

    fox.quit()

if __name__ == "__main__":
    main()
