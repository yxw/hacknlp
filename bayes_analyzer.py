#! /usr/bin/env python
"""
Naive Bayes Classifer for sentiment analysis.
"""

import random
from nltk.classify import NaiveBayesClassifier
import nltk.classify.util
import simplejson as json

from en_parser import WordSegmenter, SentenceSpliter
from lexicon import sentiment_lexicon as lexicon

def load_corpus(name):
    corpus = json.load(open('data/test_cases_en.txt'))
    return corpus[name]

def get_text_words(text, spliter):
    sentences = SentenceSpliter.split(text)
    words = []
    for sent in sentences:
        ww = spliter.split(sent)
        words.extend(ww)
    return words

def word_feats(words):
    #return dict([(w,lexicon.get_senti_score(w)) for w in words])
    return dict([(w,True) for w in words])

def get_word_features(cases):
    parser = WordSegmenter(lexicon.all_phrases(), max_word_num=4)

    features = {}
    for case in cases:
        #text, ans = case
        ans, text = case
        words = get_text_words(text, parser)
        features.setdefault(ans, []).append((word_feats(words),ans))
    for polarity, feats in features.items():
        print polarity, 'number of features:', len(feats)
    return features

def classify():
    #corpus = 'Cornell_text_polarity'
    #corpus = 'BingLiu_selected_sentences'
    corpus = 'Cornell_sentence_polarity'
    cases = load_corpus(corpus)
    features = get_word_features(cases)

    train_feats = []
    test_feats = []
    for polarity, feats in features.items():
        #cutoff = len(feats) * 1 / 4
        cutoff = 1000
        print polarity, 'number of train:', cutoff
        #train_feats += feats[:cutoff]
        #test_feats += feats[cutoff:]
        temp_feats = feats[:]
        random.shuffle(temp_feats)
        train_feats += temp_feats[:cutoff]
        test_feats += temp_feats[cutoff:]

    print 'train on %d instances, test on %d instances' % (len(train_feats), len(test_feats))

    classifier = NaiveBayesClassifier.train(train_feats)
    print 'accuracy:', nltk.classify.util.accuracy(classifier, test_feats)
    classifier.show_most_informative_features()

if __name__ == "__main__":
    classify()
