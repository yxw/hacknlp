#! /usr/bin/env python
"""
SVM Classifer for sentiment analysis.
"""

import random
from nltk.classify.svm import SvmClassifier
import nltk.classify.util
import simplejson as json

from en_parser import WordSegmenter, SentenceSpliter
from lexicon import sentiment_lexicon as lexicon
from bayes_analyzer import load_corpus, get_text_words
from bayes_analyzer import word_feats, get_word_features

def classify():
    #corpus = 'Cornell_text_polarity'
    #corpus = 'BingLiu_selected_sentences'
    corpus = 'Cornell_sentence_polarity'
    cases = load_corpus(corpus)
    features = get_word_features(cases)

    train_feats = []
    test_feats = []
    for polarity, feats in features.items():
        #cutoff = len(feats) * 2 / 4
        cutoff = 1000
        print polarity, 'number of train:', cutoff
        #train_feats += feats[:cutoff]
        #test_feats += feats[cutoff:]
        temp_feats = feats[:]
        random.shuffle(temp_feats)
        train_feats += temp_feats[:cutoff]
        test_feats += temp_feats[cutoff:]

    print 'train on %d instances, test on %d instances' % (len(train_feats), len(test_feats))

    classifier = SvmClassifier.train(train_feats)
    print 'Test classify:', classifier.classify(dict([('I', 0.0),('love',1.0), ('you', 0.0)]))
    print 'accuracy:', nltk.classify.util.accuracy(classifier, test_feats)
    classifier.show_most_informative_features()

if __name__ == "__main__":
    classify()
    #test_bayes()
