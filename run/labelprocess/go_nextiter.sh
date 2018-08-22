#!/bin/bash
if [ -z "$_semevalproject_" ] ; then
    echo "semeval env not set yet, quit"
    echo "run \"source semeval/bin/init_env.sh\" first"
    exit 1
fi


#
# help
#
help()
{
echo <<EOF
Usage: go_nextiter.sh <version>

input: 
    labelset_v?.xlsx, the labeled set 
    trainset_v?.cut, testset_v?.cut, the last version of train/test set

EOF
}

checkfile()
{
if [ ! -f "$1" ]; then
    echo "$1 not found, quit..."
    exit -1
fi
}

# check files
ver=$1
nextver=`echo $1 + 1 | bc -l`
if [ $# -ne 1 ] ; then
    help
    exit 0
fi

labelset_file="labelset-v"$ver".xlsx"
trainset_file="trainset-v"$ver".cut"
testset_file="testset-v"$ver".cut"

checkfile $labelset_file
checkfile $trainset_file
checkfile $testset_file

echo "start building labelset from ver=$ver to ver=$nextver......"
next_labelset="labelset-v"$nextver".xlsx"
next_trainset="trainset-v"$nextver".cut"
next_testset="testset-v"$nextver".cut"

homedir=`dirname $0`


#
#dump()
#
python -m semeval.labelprocess.xlsx-yy $labelset_file labelset-v$ver

#
#cut
#
python -m semeval.labelprocess.cut -f labelset-v"$ver".txt

#
# combine with old trainset, and build new version of trainset/testset
#
cat $trainset_file slabelset-v"$ver".cut >$next_trainset
#
# remove the new trainset from the old testset
#
python -m semeval.labelprocess.removetest -i $testset_file -t $next_trainset -o $next_testset

#
# dedup
#
python -m tumnus.preprocess.dedup -i $next_testset -o test-final.cut -k3

#train a classifier
if [ -d "demo" ]; then
    mv -f demo demo-v"$ver"
fi
$homedir/semeval.sh $next_trainset test-final.cut

#
#probe
#   select A,B,C subset from the prediction results
#   A: predict as neg, but wrong
#   B: predict as non-neg, and right,
#   C: prediction unsure, diff value smaller than thres
# output: A,B,C.txt; output-out.A,B,C
#
python -m semeval.labelprocess.probe demo/semeval_makeup_lrl1_balanced_no_count_0_1-2.prob

#
#make xlsx to label
#
#select 10000 A, 5000 B, 5000 C  -> select.id
head -10000 output-out.A >select.id
head -5000 output-out.B >>select.id
tail -5000 output-out.C >>select.id

python -m semeval.labelprocess.combinexlsx $next_labelset
