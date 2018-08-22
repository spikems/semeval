#!/bin/bash

banner()
{
    echo "====================================="
    echo $1
    echo "====================================="
}


clfs=(xgb rf)
vects=(count tfidf)
fs_types=(l1 chi2)
n_features=5000

clf=$1

#for clf in ${clfs[*]}; do
for vect in ${vects[*]}; do
for fs in ${fs_types[*]}; do

name="$clf"_"$vect"_"$fs"
banner $name

#run
#python -m tumnus.learn.train --trainfile train1.cut --testfile test1.cut --appname semeval_car --classifier xgb --vectorizer_type count --fs_type l1 --debug --bin_class -1
#
#python -m tumnus.learn.train --trainfile train1.cut --testfile test1.cut --appname semeval_car --classifier xgb --vectorizer_type tfidf --fs_type l1 --debug --bin_class -1
#
python -m tumnus.learn.train --trainfile train1.cut --testfile test1.cut --appname car --classifier $clf --vectorizer_type $vect --fs_type $fs --n_features 5000 --debug --bin_class -1 $2

#python -m tumnus.learn.train --trainfile train1.cut --testfile test1.cut --appname semeval_car --classifier rf --vectorizer_type count --fs_type l1 --debug --bin_class -1

done
done
#done

