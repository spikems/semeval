#!/bin/bash
if [ $# -ne "2" ]; then
    echo "testeval.sh <model name> <appname>"
    echo "  modelname: output .pkl filename by tumnus.learn.train"
    exit 0
fi

banner()
{
    echo "====================================="
    echo $1
    echo "====================================="
}

datadir=$_tumnusproject_/data
#
# this is a demo of training process
#

#ln -s ../$1 train1.cut
#ln -s ../$2 test1.cut
#python ../train_xgb.py --testmodel $1 --testfile  ../../cardata/newcar_raw.cut --appname _testsmall_car --bin_class -1
#python ../train_xgb.py --testmodel $1 --testfile  ../../cardata/newcar_all.cut --appname _testsmall_car --bin_class -1
python -m tumnus.learn.train --testmodel $1 --testfile  test1.cut --appname checkmodel_$2 --bin_class -1
