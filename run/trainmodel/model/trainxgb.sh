
python -m tumnus.learn.train --trainfile train1.cut --testfile test1.cut --appname _car --classifier xgb --vectorizer_type count --vocabulary v2_vocab.txt --debug

#
#[[3260  782   84]
# [ 472 4429  687]
# [  41  959 3162]]
#precision:   [ 0.86403393  0.7178282   0.80396644]
#recall:   [ 0.79011149  0.79259127  0.7597309 ]
#f1 score:   [ 0.82542094  0.75335941  0.78122298]
