# -*- coding: utf8 -*-
"""
Utils to load and manipulate a corpus from OpinionFinder2.

Reference:
    1. OpinionFinder https://code.google.com/p/opinionfinder/
    2. the dict link: http://tinyurl.com/mqrmcnk

All rights about this corpus is reserved by OpinonFinder

"""

import os

current = os.path.dirname(os.path.realpath(__file__))
# A local copy of the corpos file
subjclus_file = os.path.join(current, "subjcluslen1.tff")

def parse_subjclus_item(line):
    line = line.strip()
    wdict = dict([s.split('=') for s in line.split(' ')])
    word = wdict['word1'].strip()
    pos = wdict['pos1'].strip()
    if pos == 'anypos':
        pos = '*'
    strength = wdict['type'].strip()
    polarity = wdict['priorpolarity'].strip()
    #if polarity == 'positive':
    #    pwords.setdefault(word,{})[pos] = strength
    #    words.setdefault(word,{})[pos] = (polarity,strength)
    #elif polarity == 'negative':
    #    nwords.setdefault(word,{})[pos] = strength
    #    words.setdefault(word,{})[pos] = (polarity,strength)
    return (word, pos, polarity, strength)

def load_lexicon(debug=False):
    lexicon = {}
    # remove all possible neutral words
    neutral_words = set()
    for line in open(subjclus_file):
        word,pos,pol, strength = parse_subjclus_item(line)
        if pol == 'neutral':
            neutral_words.add(word)
            continue
        if word not in neutral_words:
            lexicon.setdefault(word,{})[pos] = [pol,strength]
    if debug:
        print 'All neutral words:', neutral_words
        return lexicon, neutral_words
    return lexicon

if __name__ == '__main__':
    lexicon, neutral_words = load_lexicon(True)

