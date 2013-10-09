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

Try Naive Bayes Classifer for sentiment anaylsis with the custermized lexicon
   (Note: Since the training cases are selected randomly, you may get different
    result for each running of the script.)

Example:

➜  hacknlp git:(master) ✗ python bayes_analyzer.py
P number of features: 5331
N number of features: 5331
P number of train: 1000
N number of train: 1000
train on 2000 instances, test on 8662 instances
accuracy: 0.724313091665
Most Informative Features
                     our = True                P : N      =      9.7 : 1.0
                powerful = True                P : N      =      7.7 : 1.0
                 culture = True                P : N      =      7.0 : 1.0
                    rare = True                P : N      =      7.0 : 1.0
              compelling = True                P : N      =      6.6 : 1.0
                 journey = True                P : N      =      6.3 : 1.0
                   seems = True                N : P      =      6.1 : 1.0
                 history = True                P : N      =      5.8 : 1.0
                interest = True                N : P      =      5.7 : 1.0
                    pure = True                P : N      =      5.7 : 1.0
