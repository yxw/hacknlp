#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Simple enough (so maybe not highly accurate) tools to quickly parse text
into sentences, phrases and words. Only works for English.
"""

import re
from utils.pytrie import StringTrie

class SentenceSpliter(object):
    SPLITER_RE = r'(\.|!|\?|~)+'
    """
    Parser for spliting text into sentences.
    """

    def __init__(self):
        pass

    @classmethod
    def split(self, text):
        return filter(None,re.sub(self.SPLITER_RE, '\g<0>_|_', text).split('_|_'))

def is_prefix_valid(phr, text):
    """
    Check whether phr is an valid word/phrase prefix of text.

    Assumption: "len(phr) <= len(text)" is always True.
    """
    if len(phr)==len(text) or (text[len(phr)] in [' ', ',', '.']):
        return True
    return False

class WordSegmenter(object):
    """
    Segment a sentent into pieces of words. For English, also check phrases.

    English only.
    """
    def __init__(self, iterable, value=None, max_word_num=7):
        """
        Construct PhraseDetector from an iterable containing the keys, and
        all values of the keys are set to #value#.

        if #iterable# is None, phrases are not considered.
        """
        if iterable:
            #self._trie = StringTrie(seq=None, **kwargs)
            self._trie = StringTrie.fromkeys(iterable, value=value)
        else:
            self._trie = None
            #raise ValueError('you need to provide phrase list to help word segmenter')
        self._max_word_num = max_word_num

    def split(self, text):
        if self._trie:
            return self._split_by_phrase(text)
        return self._split_naive(text)

    def _split_naive(self, text):
        wlist = []
        for w in text.split():
            w = w.strip().rstrip(',.!')
            if w:
                #yield w
                wlist.append(w)
        return wlist

    def _split_by_phrase(self, text):
        """
        Split the given text into words or phrases.

        NOTE: words returned are all lowercase-ed (to fix ?)
        """
        #FIXME: only for sentence.
        words = text.lower().split()
        i = 0
        wlist = []
        while (i < len(words)):
            s = ' '.join(words[i:i + self._max_word_num])
            try:
                phr = self._trie.longest_prefix(s)
                #if len(s) > len(phr) and s[len(phr)].isalnum():
                if is_prefix_valid(phr, s):
                    i += len(phr.split(' '))
                else:
                    phr = words[i]
                    i += 1
            except KeyError:
                phr = words[i]
                i += 1
            wlist.append(phr)
            #yield phr
        return wlist
