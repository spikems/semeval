#!/bin/bash

if [ $# -ne "3" ]; then
    echo "fast evaluation on features in vocabluary"
    echo "fasteval.sh <classifier> <vocabfile> <appname>"
    echo "  classifier: lsvc, lr, rf, xgb, refer to tumnus.learn.train"
    echo "  vocabfile : vocabulary filename to filter out features"
    exit 0
fi


python -m tumnus.learn.train --trainfile train1.cut --testfile train1.cut --appname $3_train --classifier $1 --vectorizer_type count --vocabulary $2 --debug --bin_class -1
python -m tumnus.learn.train --trainfile train1.cut --testfile test1.cut --appname $3_test --classifier $1 --vectorizer_type count --vocabulary $2 --debug --bin_class -1
