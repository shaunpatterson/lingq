#!/usr/bin/env python
# -*- coding: utf-8 -*-    

import sys
import urllib
from pyquery import PyQuery as pq
from lxml import etree
from unidecode import unidecode

NAME=0
URL=1

baseUrl = "http://www.memrise.com/course/58866/5000-words-sorted-by-frequency-strict-typing/"


def scrapeLevel(level):
    url = "%s%s" % (baseUrl, level)
    d = pq(url=url)

    scrapedGerman = d('div.col_a div.text')
    german = []
    for w in scrapedGerman:
        german.append(w.text.encode('utf-8').strip())

    scrapedEnglish = d('div.col_b div.text')
    english = []
    for w in scrapedEnglish:
        english.append(w.text.encode('utf-8').strip())

    
    foundWords = []
    if len(german) != len(english):
        print "WTF"
        raise

    # I think a zip or something would be better. phucket
    i = 0
    for g in german:
        e = english[i]
        foundWords.append((g, e))
        i = i + 1

    # Old way before page change
    #scrapedWords = d('div.thing.text-text div.text')
    #index = 0
    #lastGerman = ""
    #foundWords = [] # Result
    #for w in scrapedWords:
        #print w
        #print w.text
        #text = w.text.encode('utf-8').strip()
        #if len(text) == 0:
            #continue

        #if (index % 2 == 0):
            ## german
            #lastGerman = text
        #else:
            ## got everything
            #print "%s, %s" % (lastGerman, text)
            #foundWords.append((lastGerman, text))

        #index = index + 1

    return foundWords
    
def main():
    englishWords = []
    twice = []

    for i in range(1, 102):
        words = scrapeLevel(i)
        print "Level %d" % (i)
        for w in words:
            g = w[0]
            e = w[1]
            print "%s,%s" % (w[0], w[1])

            twice.append((i, g, e))

            if e in englishWords:
                englishWords.append(e)
            


        print "\n\n"

    for e in englishWords:
        print e

        for t in twice:
            (level, german, english) = t
            if english == e:
                print "Level %s: %s=%s" % (level, german, english)



if __name__ == "__main__":
    main()


