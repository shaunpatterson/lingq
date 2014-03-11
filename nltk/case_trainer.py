#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
import re
from nltk.tag.stanford import POSTagger

def stripPieces(pieces):
    stripped = []

    for p in pieces:
        if p[1] == 'ART':
            stripped.append(stripART(p[0]))
        elif p[1] == 'ADJA':
            stripped.append(stripADJA(p[0]))
        else:
            stripped.append(p[0])

    return stripped



def stripART(art):
    # Strips endings off articles

    # der/die/das/den/dem/des
    regex = re.compile('^(d)(er|ie|as|en|em|es)$', re.IGNORECASE)
    m = regex.match(art)
    if m:
        return "%s__" % (m.group(1))
    
    # (k)ein, (k)eine, etc
    regex = re.compile('^(k?)(ein)(e|en|em|er|es)$', re.IGNORECASE)
    m = regex.match(art)
    if m:
        return "%sein%s" % (m.group(1), '_' * len(m.group(3)))

    return art

def stripADJA(adja):
    # strips adjective endings

    regex = re.compile('^(.*)(e|er|ie|as|en|em|es)$', re.IGNORECASE)
    m = regex.match(adja)
    if m:
        return "%s%s" % (m.group(1), '_' * len(m.group(2)))
    
    return adja
    


def main():

    st = POSTagger("/home/shaun/stanford-postagger-full-2013-11-12/models/german-dewac.tagger", \
        "/home/shaun/stanford-postagger-full-2013-11-12/stanford-postagger.jar")

    #st = POSTagger("/home/shaun/stanford-postagger-full-2013-11-12/models/german-fast.tagger", \
            #"/home/shaun/stanford-postagger-full-2013-11-12/stanford-postagger.jar")

    #print st.tag("Die Kinder in Bayern haben lange Ferien".split())

    #return

    with open(sys.argv[1], 'r') as f:
        content = f.read()

    sentences = re.split('\n|\.|\?', content)

    for s in sentences:
        if len(s) == 0: continue
        #print s
        pieces = st.tag(s.split())
        strippedPieces = stripPieces(pieces)
    
        print ' '.join(strippedPieces)


    # Nouns = NN
    # Articles (ein, eine, einer) = ART
    # Determiners (der, die, das) = ART
    # Adjectives = ADJA


if __name__ == "__main__":
    main()
