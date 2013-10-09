#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
A generated and customizable sentiment lexicon could be used for
sentiment analyze.

"""

import os
import subjclus
import inquirer

cur_dir = os.path.dirname(os.path.abspath(__file__))
# See gen-senti-lexicon.py about how to generate this dictionary
# you can customize this dict by adding your own sentiment words
# with custmized weight.
senti_words_dic = os.path.join(cur_dir, 'sentiwords_en.dic')
# A modifier dict could be customized and included in order
# to get more accurate scores. Only some examples are included.
# You can customize to add in more modifers.
modifiers_dic = os.path.join(cur_dir, 'modifiers_en.dic')

def load_sentiwords(filename=senti_words_dic):
    """
    Load sentimental words from local dict file

    There are two corpus available online could be used to generate
    sentiment lexicon. see
        subjclus.py
        inquirer.py
    for more details.
    """
    try:
        lex = {}
        with open(filename) as fp:
            for line in fp:
                line = line.strip()
                word, pos, score = line.split(',')
                score = float(score)
                lex.setdefault(word, {})[pos] = score
        return lex
    except IOError:
        raise Exception("""No sentiment dict was generated. Please find gen-senti-lexicon.py on details of how to generate the dictionary.""")

def load_modifiers(filename=modifiers_dic):
    """
    Load modifiers from local dict file.

    For modifiers, POS is ignored.
    """
    lex = {}
    try:
        with open(filename) as fp:
            for line in fp:
                line = line.strip()
                word,pos,wtype = line.split(',')
                lex[word] = wtype
    except IOError:
        # no modifer dict provided.
        print "\tlexicon is loaded without modifiers ..."
    return lex

class SentimentLexicon(object):
    """
    A generated and customizable sentiment lexicon could be used for
    sentiment analyze.

    sentiwords: dictionary of words with sentiment
    modifiers:   dictionary of words which could potentially
                strenghen/weaken a sentiword by a certain factor
    """
    # customizable factor for types of modifiers
    mtype_scaler = {
            'n': -1.0, # negator
            's': 3.0, # Strong
            'a': 1.2, # affirmation
            'w': 0.5, # weak
            }

    def __init__(self):
        """
        Load the sentiment lexicon from local dictionary files.
        """
        self.sentiwords = load_sentiwords()
        self.modifiers = load_modifiers()

    def __contains__(self, word):
        return (word in self.sentiwords) or (word in self.modifiers)

    def is_modifier(self, word, to_scale_num=True):
        """
        Check if the word is a modifier.

        If True, return the type of modifier.
            If #to_scale_num# is set, map this type to a scale number
        """
        mtype = self.modifiers.get(word)
        if mtype:
            return to_scale_num and self.mtype_scaler[mtype] or mtype
        return False

    def get_sentiment(self, word, pos=None):
        if pos:
            return self._get_score(word, pos)
        return self._get_score_without_pos(word)

    def _get_score_without_pos(self, word):
        pos_senti = self.sentiwords.get(word)
        if not pos_senti:
            return 0.0
        return self.is_consistant(word) and pos_senti.values()[0] or 0.0

    def _get_score(self, word, pos):
        return self.sentiwords.get(word, {}).get(pos, 0)

    def is_consistant(self, word):
        """
        Check the sentiment consistance of the word.

        If the polarity for all possible POS are the same, return True
        otherwise return False
        """
        sentis = set(self.sentiwords.get(word, {}).values())
        return len(sentis) <= 1

    def check_consistance(self):
        """
        Check the consistance of all words' sentiment
        """
        for word in self.sentiwords:
            if not self.is_consistant(word):
                print '## inconsistant:', word,self.sentiwords[word]
                return False
        return True

    def check_redundancy(self):
        """
        Check whether there is redundant words in sentiwords and modifiers
        """
        pass

    def all_words(self):
        """
        Return all words in the lexicon
        """
        import itertools
        return itertools.chain(self.sentiwords, self.modifiers)

    def all_phrases(self):
        """
        Return all words in the lexicon
        """
        wlist = self.all_words()
        return [w for w in wlist if len(w.split(' ')) > 1]


sentiment_lexicon = SentimentLexicon()

def test_lexicon():
    lexicon = sentiment_lexicon
    lexicon.check_consistance() == True
    while True:
        word = raw_input('\nInput a word to get sentiment:')
        word_pos = word.strip().split()
        print '------'
        scale = lexicon.is_modifier(word_pos[0])
        if scale:
            print '%s (Modifier)' % scale
        else:
            print '%s' % lexicon.get_sentiment(*word_pos)

if __name__ == "__main__":
    test_lexicon()

