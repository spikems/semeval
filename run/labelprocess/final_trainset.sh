#!/bin/bash

#
# help
#
help()
{
echo <<EOF
Usage: final_trainset.sh <version>

build final trainset from the trainset-v"$version".cut file

EOF
}

homedir=`dirname $0`
# check files
ver=$1
if [ $# -ne 1 ] ; then
    help
    exit 0
fi

trainset=trainset-v"$ver".cut

#
#the initial version of trainset should be checked manually, just like 
#other labelsets
#
#tainset-v1.cut

##
## here you can adjust the balance of the classes
## for example, add more pos samples
##
#grep "^1 " ../cut/all.cut >>all-v0-pos.cut
#python -m tumnus.preprocess.stratesample all-v0-pos.cut v0pos 25000
#cat train-r-v0pos trainset-v"$ver".cut >dataset.cut
##
## dedup if necessary
##
#trainset=output-final.cut
#python -m tumnus.preprocess.dedup -i dataset.cut -o $trainset -k3
#

#
# dump labelset and merge with neg/pos records to make a select.id file
#
gawk '{print $2,$1}' $trainset >select.id

#
# make xlsx
#
python -m semeval.labelprocess.combinexlsx --uselabel trainset-v"$ver".xlsx




