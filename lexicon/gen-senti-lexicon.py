#!/usr/bin/env python

"""
Generate a fairly reliable sentiment lexicon for SentiLexicon.

This is done by combining the two corpus:
    subjcluslen1.tff  --> find subjclus.py for more details
    inqdict.txt       --> find inquirer.py for more details

How to combine to get the final lexicon:
    1. If a word is in both corpus with the same polarity (pos/neg):
        INCLUDE the word with the polarity into lexicon
    1. If a word is in both corpus but with opposite polarity (pos/neg):
        EXCLUDE the word from lexicon
    2. If a word is in either corpus,
        INCLUDE the word with the polarity into lexicon

"""

from collections import namedtuple
from nltk.corpus import wordnet

import subjclus
import inquirer

SentiWord = namedtuple('SentiWord', 'word, pos, score, source')

wordnet_pos_map = {
        wordnet.ADJ:'adj',
        wordnet.ADJ_SAT:'adj',
        wordnet.ADV:'adv',
        wordnet.VERB:'verb',
        wordnet.NOUN:'noun',
        }

def get_pos_from_wordnet(word):
    """
    return a POS list of the given word. Query from wordnet
    """
    return [wordnet_pos_map.get(ss.pos, ss.pos) for ss in wordnet.synsets(word)]

def load_lexicons():
    subjclus_lexicon = subjclus.load_lexicon()
    inquirer_lexicon = inquirer.load_lexicon()

    def get_source(word):
        # get the soure where the sentiword comes from.
        s1 = subjclus_lexicon.get(word) and 'subjcluslen' or ''
        s2 = inquirer_lexicon.get(word) and 'inquirer' or ''
        return '|'.join(filter(None,[s1,s2]))

    def get_pos_senti(word):
        """
        return the POS:polarity dict of the word which have sentiment

        Handle special POS:
            '*' or 'anypos': get all possible POS from wordnet by the word
            '': Only get 'adj'/'adv' POS from wordnet by the word
        """
        #First check the subjcluslen lexicon
        s1 = subjclus_lexicon.get(word)
        if s1:
            pos_pol = dict([(k, v[0]) for k,v in s1.items() if k not in ['anypos','*']])
            if 'anypos' in s1 or '*' in s1:
                pol = s1.get('*') or s1.get('anypos')
                pol = pol[0]
                for pos in get_pos_from_wordnet(word):
                    if pos not in pos_pol:
                        pos_pol[pos] = pol
                    elif pos_pol[pos] != pol:
                        #print '    CONFLICT sentiment:', word
                        raise ValueError('Sentiment value confilict!:', word, pol, '<-->', pos_pol[pos])
            return pos_pol

        # then check the Inquirer lexicon
        s2 = inquirer_lexicon.get(word)
        if s2:
            pos_pol = dict([(k, v[0]) for k,v in s2.items() if k != ''])
            if '' in s2:
                pol = s2.get('')[0]
                pos_list = get_pos_from_wordnet(word)
                pos_list = [p for p in pos_list if p in ['adj', 'adv']]
                for pos in pos_list:
                    if pos not in pos_pol:
                        pos_pol[pos] = pol
            return pos_pol
        # should not come here
        return {}

    def get_subject_strength(word, pos):
        """
        return the subjective strength of the word.

        If the word only exists in Inquirer, set its strength as "weak",
        otherwise get it directly from subjclulen
        """
        s1 = subjclus_lexicon.get(word)
        s2 = inquirer_lexicon.get(word)

        if s2:
            return 'weaksubj'
        else:
            return s1.get(pos) and s1.get(pos)[1]


    all_words = set(list(subjclus_lexicon.keys()) + list(inquirer_lexicon.keys()))
    for word in sorted(all_words):
        source = get_source(word)
        for pos, pol in get_pos_senti(word).items():
            score = 0.0
            if pol == 'positive':
                score = 1.0
            elif pol == 'negative':
                score = -1.0
            yield (word, pos, str(score))

lexicon = load_lexicons()
for item in lexicon:
    print ','.join(item)
#print str(lexicon)
