#!/bin/bash

if [ -z "$_semevalproject_" ] ; then
    echo "semeval env not set yet, quit"
    echo "run \"source semeval/bin/init_env.sh\" first"
    exit 1
fi

banner()
{
    echo "====================================="
    echo $1
    echo "====================================="
}

appname=semeval_makeup


#
# this is a demo of training process
#
mkdir -p demo
cd demo

ln -s ../$1 train1.cut
ln -s ../$2 test1.cut

#
# train models
#
banner "Step.3 train models"
#echo 
#echo "model 1. train lr with all unigram features"
#echo
#python -m tumnus.learn.train --trainfile train1.cut --testfile test1.cut --appname $appname --classifier lr --vectorizer_type count --balanced --debug
echo 
echo "model 2. train lr with 1200 unigram features selected by chi2"
echo
 python -m tumnus.learn.train --trainfile train1.cut --testfile test1.cut --appname $appname --classifier lr --vectorizer_type count --balanced --fs_type chi2 --n_features 1200 --debug --bin_class -1

#echo 
#echo "model 3. train lr with 500 unigram features selected by chi2"
#echo
# python -m tumnus.learn.train --trainfile train1.cut --testfile test1.cut --appname $appname --classifier lr --vectorizer_type count --balanced --fs_type chi2 --n_features 500 --debug
#echo 
#echo "model 4. train lr with 300 unigram features selected by chi2"
#echo
# python -m tumnus.learn.train --trainfile train1.cut --testfile test1.cut --appname $appname --classifier lr --vectorizer_type count --balanced --fs_type chi2 --n_features 300 --debug
#echo 
#echo "model 5. train lr with about 850 unigram features selected by l1 penalty"
#echo
#python -m tumnus.learn.train --trainfile train1.cut --testfile test1.cut --appname $appname --classifier lrl1 --vectorizer_type count --balanced --debug 
echo 
echo "model 6. train lr with about 1150 bigram features selected by l1 penalty"
echo
python -m tumnus.learn.train --trainfile train1.cut --testfile test1.cut --appname $appname --classifier lrl1 --vectorizer_type count --balanced --ngram_range 1,2 --debug --bin_class -1

echo 
echo "model 7. train lr with about 850 unigram features selected by l1 compressed model"
echo
python -m tumnus.learn.train --trainfile train1.cut --testfile test1.cut --appname $appname --classifier lr --vectorizer_type count --balanced --fs_type l1 --debug --bin_class -1


##
## test model on new testset
##
#banner "Step.4 test models on unseen dataset"
#echo 
#echo "test model 3. train lr with 500 unigram features selected by chi2"
#echo
#
# python -m tumnus.learn.train --testmodel $appname_lr_balanced_chi2_count_500 --testfile splitbyday/data2-42731.cut --appname _test31
#
#echo 
#echo "test model 6. train lr with about 1150 bigram features selected by l1 penalty"
#echo
#
# python -m tumnus.learn.train --testmodel $appname_lrl1_balanced_no_count_0_1-2 --testfile splitbyday/data2-42731.cut --appname _test31
#
#echo 
#echo "test model 7. train lr with about 850 unigram features selected by l1 compressed model"
#echo
#
# python -m tumnus.learn.train --testmodel $appname_lr_balanced_l1_count_0 --testfile splitbyday/data2-42731.cut --appname _test31
#
 echo
 echo "byebye!"
 echo
