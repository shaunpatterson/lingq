#!/usr/bin/env python

from nltk.tag.stanford import POSTagger

#st = POSTagger("/home/shaun/stanford-postagger-full-2013-11-12/models/german-dewac.tagger", \
        #"/home/shaun/stanford-postagger-full-2013-11-12/stanford-postagger.jar")

st = POSTagger("/home/shaun/stanford-postagger-full-2013-11-12/models/german-fast.tagger", \
        "/home/shaun/stanford-postagger-full-2013-11-12/stanford-postagger.jar")

print st.tag('Lernen Sie nicht zu viel auf einmal.'.split()) 

print st.tag('Mach nach einer halben Stundne eine Pause'.split()) 

print st.tag('Eine gute Frau'.split()) 

print st.tag('Der guter Mann'.split()) 

# Nouns = NN
# Articles (ein, eine, einer) = ART
# Determiners (der, die, das) = ART
# Adjectives = ADJA


