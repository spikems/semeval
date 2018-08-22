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
Usage: make_labelset_v1.sh <xlsx>

dump from the original dataset, and sample out train/test set v1
select a subset of data by classifier as the labelset to be checked

EOF
}

homedir=`dirname $0`


ln -s ../dataset/makeup_05262017.xlsx makeup_05262017.xlsx
ln -s ../dataset/makeup_08122016.xlsx makeup_08122016.xlsx
#
#dump()
#
if [ ! -f "makeup_05262017.txt" ]; then
    python -m semeval.labelprocess.xlsx-yy makeup_05262017.xlsx makeup_05262017
fi
if [ ! -f "makeup_08122016.txt" ]; then
    python -m semeval.labelprocess.xlsx-yy makeup_08122016.xlsx makeup_08122016
fi

#
#cut
#
if [ ! -f "smakeup_05262017.cut" ]; then
    python -m semeval.labelprocess.cut -f makeup_05262017.txt
fi
if [ ! -f "smakeup_08122016.cut" ]; then
    python -m semeval.labelprocess.cut -f makeup_08122016.txt
fi

#
# id mapping
# output: idmap.txt, filemap.txt, all.cut
#
if [ ! -f "idmap.txt" ]; then
    python -m semeval.labelprocess.mapping smakeup_08122016.cut smakeup_05262017.cut
fi

#
# build dataset
#
python -m tumnus.preprocess.dedup -i all.cut -o all-dedup.cut -k3

#
#
#
grep "^-1 " all-dedup.cut >neg.cut
grep "^1 " all-dedup.cut >pos.cut
grep "^0 " all-dedup.cut >mid.cut

#
# select 5k for each group
# output: train.cut, test.cut
#
#python -m tumnus.preprocess.stratesample pos.cut .pos.tmp 5000 True
python -m tumnus.preprocess.stratesample pos.cut pos.tmp 5000 True
python -m tumnus.preprocess.stratesample mid.cut mid.tmp 5000 True
cat neg.cut train*.tmp >train.cut
cat test*.tmp >test.cut
#rm *.tmp
#
# build version 1 of trainset and testset
#
#ln -s train.cut trainset_v1.cut
#ln -s test.cut testset_v1.cut
#remove mid in the original trainset_v1
cat neg.cut train*pos.tmp >trainset_v1.cut
cp test.cut testset_v1.cut

#train a classifier
$homedir/semeval.sh train.cut test.cut

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

python -m semeval.labelprocess.combinexlsx labelset_v1.xlsx

#
# get labelset back
# dump labelset and merge with neg/pos records to make a select.id file
#
#gawk '{print $2,$1}' dataset-v4-dedup.cut >dataset-v4-dedup.id
#ln -s dataset-v4-dedup.id select.id
#python -m semeval.labelprocess.combinexlsx --uselabel dataset-v4-dedup.xlsx




