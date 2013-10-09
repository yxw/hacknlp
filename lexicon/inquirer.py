# -*- coding: utf8 -*-
"""
Utils to load and manipulate the "General Inquirer" corpus by Harvard University
to extract sentiment lexicon.

There are 11788 words tagged in the Inquirer corpus used in this script.

For more details on the General inquirer and Descriptions of Inquirer
Categories and Use of Inquirer Dictionaries, please refer to the following
links:
    1. http://www.wjh.harvard.edu/~inquirer/inqdict.txt
    2. http://www.wjh.harvard.edu/~inquirer/homecat.htm

All rights on this corpus is reserved by Harvard University.

"""

import os

current = os.path.dirname(os.path.realpath(__file__))
# save a local copy of the dict file (the first line is removed)
general_inquirer = os.path.join(current, "inqdict.txt")

# TODO: Also need to consider adverb?
def get_inquirer_pos(plist):
    """
    Mapping the inquirer POS to sentiment interesting POS
    """
    pos_map = {
            'Noun': 'noun',
            'IAV': 'verb',
            'DAV': 'verb',
            'SV': 'verb',
            'IPadj': 'adj',
            'IndAdj': 'adj'
            }
    for p in plist:
        return pos_map.get(p, '')

def parse_inquirer_item(line):
    plist = line.split('|')[0].strip().split()
    if not plist:
        return
    word = plist[0].split('#')[0].lower()
    if 'Negativ' in plist[1:] or 'Ngtv' in plist[1:]:
        polarity = 'negative'
    elif 'Positiv' in plist[1:] or 'Pstv' in plist[1:]:
        polarity = 'positive'
    else:
        return None

    pos = get_inquirer_pos(plist)
    return (word,pos,polarity)

def load_lexicon():
    lexicon = {}
    lines = open(general_inquirer).read()
    lines = lines.split('\r')
    for line in lines:
        senti = parse_inquirer_item(line)
        if senti:
            word,pos,pol = senti
            lexicon.setdefault(word,{})[pos] = [pol,'']
    return lexicon
