#!/bin/bash

#
# validate that adding feature can really improve the performance, especially the recall
#
homedir=$_semevalproject_
if [ -z $homedir ] ; then
    echo 'init semeval environment first please, quit...'
    exit 0
fi


# prepare data
cp $homedir/data/trainset/car/dataset-v4-dedup.dat .
cp $homedir/data/trainset/car/dataset-v4-dedup.txt.bz2 .
bzip2 -d dataset-v4-dedup.txt.bz2

mkdir -p feature_dicts
cp $homedir/data/feature_dict/car/*.dict feature_dicts
mkdir -p jieba_dict
cp $homedir/data/jieba_dict/dict.txt.small jieba_dict/dict.txt


#follow the result of the last train 
#demo_checkresult.sh
#check the result , and add possible features into add.txt

# here , very simple way to add as aspect
gawk '{print "aspect n ", $1}' add.txt >> feature_dicts/aspect.dict 

# rebuild userdict
python -m tumnus.learn.buildfeature -o car.userdict --jieba jieba_dict/ --dict feature_dicts/ --builduserdict

# cut by new feature dicts
python -m tumnus.learn.buildfeature -i dataset-v4-dedup.txt -o v4-all-new.cut --userdict car.userdict --dict feature_dicts/ --dat dataset-v4-dedup.dat

# select featuretag as features
python -m tumnus.learn.buildfeature -i v4-all-new.cut -o v4-feature-new.cut --selectfeature 0

# train by xgb
fasttrain.sh v4-feature-new.cut 
