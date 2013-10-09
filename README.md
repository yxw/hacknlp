hacknlp
=======

My collection of tailored tools and toys playing with NLP.

Dependencies:

The following tools may be used in this project:
hence you might need to install them manually before running this project.
    nltk >= 2.01rc1
    nltk-data
    svmlight (for SVM classifier)
    numpy (not for now)

How To Use:

1. try Naive Bayes Classifer for sentiment anaylsis with my custermized lexicon
   (Note: Since the training cases are selected randomly, you may get different
    result for each running of the script.)

will@will-mac:~/hacknlp$ python bayes_analyzer.py
P number of features: 5331
N number of features: 5331
P number of train: 1000
N number of train: 1000
tran on 2000 instances, test on 8662 instances
accuracy: 0.714961902563
Most Informative Features
                 culture = True                P : N      =      9.0 : 1.0
                    lack = True                N : P      =      7.7 : 1.0
                    ride = True                P : N      =      7.7 : 1.0
                    rare = True                P : N      =      7.7 : 1.0
                  deeply = True                P : N      =      7.7 : 1.0
                    dull = True                N : P      =      7.7 : 1.0
                     bad = True                N : P      =      7.6 : 1.0
                   solid = True                P : N      =      7.0 : 1.0
                  boring = True                N : P      =      7.0 : 1.0
             beautifully = True                P : N      =      7.0 : 1.0


