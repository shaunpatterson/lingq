#!/usr/bin/env python
# -*- coding: utf-8 -*-    

import sys
import urllib
import re
from pyquery import PyQuery as pq
from lxml import etree
from unidecode import unidecode
import urllib

from translate import Translator

NAME=0
URL=1

baseUrl = "http://www.verbix.com/webverbix/German/"


#flatCategories = []


#def scrape(url, hierarchy):
    #global baseUrl
    #global flatCategories
    
    #print >> sys.stderr, len(flatCategories)

    #try:
        #d = pq(url="%s%s" % (baseUrl, unidecode(url)))

        #subCategories = d('div#catList div.categories ul li a')
        #if not subCategories:
            #pass
            ##print "No sub-categories, at a leaf"
        #else: 
            #for subCat in subCategories:
                #subCat = (unidecode(subCat.text.strip()), subCat.attrib['href'])
                #nextHierarchy = hierarchy[:]
                #nextHierarchy.append(subCat[NAME])
                #flat = '|'.join(nextHierarchy)
                #flatCategories.append(flat)

                ##print flatCategories

                #scrape(subCat[URL], nextHierarchy)
    #except:
        #print url
    

def scrapeVerb(verbText):
    global baseUrl
    translator=Translator(from_lang='de', to_lang='en')

    verbUrl = "%s%s.html" % (baseUrl, verbText)

    lines = urllib.urlopen(verbUrl).readlines()

    text = " ".join(lines)
    text = text.replace("\n", " ")
    #print text
    
    verb = {}

    #verb['infinitive'] = re.match(r'.*<b>Infinitive: </b><span class="normal">(.*?)</span><br>.*', text, re.I).group(1)
    #verb['presentPart'] = re.match(r'.*<b>Present participle:.*?<span class=".*?">(.*?)</span><br>.*', text, re.I).group(1)
    #verb['pastPart'] = re.match(r'.*<b>Past participle:</b> <span class=".*?">(.*?)</span><br>.*', text, re.I).group(1)

    # Now find the conjugations
    currentTense = ''
    for line in lines:
        line = line.strip()
        
        tenseMatch = re.match(".*(Present|Past|Perfect|Past|Pluperfect|Future II|Future I)[^ ].*", line)
        if tenseMatch:
            nextTense = tenseMatch.group(1)
            if nextTense not in verb:
                currentTense = nextTense
                verb[currentTense] = {}
                #print "Switching to Indicative: %s" % (nextTense)
            else:
                # We're only doing the indicitive
                break
            continue
       
        conjMatch = re.match(r'.*<font.*?><span.*?>(.*?)</span>.*?</font><span.*?>(.*?)</span>', line)
        if conjMatch:
            conj = conjMatch.group(2).strip()
            conj = conj.replace("&ouml;", "ö")
            conj = conj.replace("&auml;", "ä")
            conj = conj.replace("&uuml;", "ü")
            # TODO: ß

            article = conjMatch.group(1).strip()

            verb[currentTense][article] = {} 
            verb[currentTense][article]['de'] = "%s %s" % (article, conj)
            #verb[currentTense][article]['en'] = "%s %s" % (article, conj)
            trans = translator.translate("%s %s." % (article.capitalize(), conj))
            trans = trans.replace(' . ', '')
            trans = trans.replace(' .', '')
            trans = trans.replace('. ', '')
            trans = trans.replace('.', '')
            if article == 'ihr':
                verb[currentTense][article]['en'] = "%s (pl): %s - %s - %s" % (trans, article, verbText, currentTense)
            else:
                verb[currentTense][article]['en'] = "%s: %s - %s - %s" % (trans, article, verbText, currentTense)

    #for tense in ['Present', 'Past', 'Perfect', 'Pluperfect', 'Future I', 'Future II']:
    for tense in ['Present', 'Past', 'Perfect']: #, 'Pluperfect', 'Future I', 'Future II']:
        currentTense = verb[tense]
        for article in currentTense:
            print "%s,%s," % (currentTense[article]['de'], currentTense[article]['en'])
    
    #for tense in verb:
        #print tense
        #for article in verb[tense]:
            #print verb[tense][article]['de']
            #print verb[tense][article]['en']
            #print "%s,%s," % (article['de'], article['en'])

        



def main():
    scrapeVerb("geben")
    scrapeVerb("haben")
    #scrapeVerb("machen")
    #scrapeVerb("gehen")
    #scrapeVerb("spielen")

    #scrapeVerb("öffnen")

    #alexaUrl = "http://www.alexa.com/topsites/category/Top"
    #d = pq(url=alexaUrl)

    ## Top level categories
    #items = d('div.categories.top ul li a')
   
    #categories = [ (x.text.strip(), x.attrib['href']) for x in items ]

    ##for cat in categories:
        ##scrape(cat[URL], [cat[NAME]])

    #cat = categories[catIndex]
    #scrape(cat[URL], [cat[NAME]])

    #for cat in flatCategories:
        #print cat


if __name__ == "__main__":
    main()


