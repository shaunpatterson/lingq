#!/usr/bin/env python

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

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
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

    saveButton = fox.find_element_by_class_name('save_and_open-button')
    saveButton.click()

    # Cry me a river
    time.sleep(10)

def main(username, password, lang, collectionId, zipFilename):
    # Extract the zip into a tmp directory in the current path
    folderName = str(uuid.uuid1())
    print folderName

    with zipfile.ZipFile(zipFilename) as zf:
        zf.extractall(folderName)
    
    lessonFilenames = sorted(os.listdir(folderName))
    
    # Not the best way... but it's the way I'm doing it
    # LessonName(filename) -> Lesson Text
    lessons = OrderedDict()
    for lessonFilename in lessonFilenames:
        path = os.path.join(folderName, lessonFilename)
        with open(path) as f:
            lessonTextList = f.readlines()
            lessonText = '<br/>'.join([ x.strip() for x in lessonTextList ])
            lessonName = os.path.splitext(lessonFilename)[0]
            lessons[lessonName] = lessonText

    #print lessons
    # Clean up the zip
    shutil.rmtree(folderName)

    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList",2)
    profile.set_preference("browser.download.manager.showWhenStarting",False)
    profile.set_preference("browser.download.dir", os.getcwd())
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk","application/octet-stream; charset=utf-8")
   
    fox = webdriver.Firefox(profile)
    
    print "Logging in"
    login(fox, username, password)

    print "Creating lessons"
    
    for lessonName, lessonText in lessons.iteritems():
        createLesson(fox, lang, collectionId, lessonName, lessonText);

    fox.quit()

if __name__ == "__main__":
    # Username, password, lang, collection
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
