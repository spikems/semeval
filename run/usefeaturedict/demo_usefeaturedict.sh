#
# demo to extract features by using feature dictionary 
#

homedir=$_semevalproject_
if [ -z $homedir ] ; then
    echo 'init semeval environment first please, quit...'
    exit 0
fi


#
# prepare data
#
cp $homedir/data/trainset/car/dataset-v4-dedup.dat .
cp $homedir/data/trainset/car/dataset-v4-dedup.txt.bz2 .
bzip2 -d dataset-v4-dedup.txt.bz2
exit

mkdir -p feature_dicts
cp $homedir/data/feature_dict/car/*.dict feature_dicts
mkdir -p jieba_dict
cp $homedir/data/jieba_dict/dict.txt.small jieba_dict/dict.txt

# create user dict by the feature dictionary
python -m tumnus.learn.buildfeature -o car.userdict --jieba jieba_dict/ --dict feature_dicts/ --builduserdict

# extract features
python -m tumnus.learn.buildfeature -i dataset-v4-dedup.txt -o v4-all-tag.cut --userdict car.userdict --dict feature_dicts/ --dat dataset-v4-dedup.dat

# select featuretag as features
python -m tumnus.learn.buildfeature -i v4-all-tag.cut -o v4-feature-new.cut --selectfeature 0

# split dataset
python -m tumnus.preprocess.stratesample v4-feature-new.cut v4 0.8

# train model
mkdir -p demo
cd demo
ln -s ../train-r-v4 train1.cut
ln -s ../test-r-v4 test1.cut

python -m tumnus.learn.train --trainfile train1.cut --testfile test1.cut --appname test --classifier xgb --vectorizer_type count --debug --bin_class -1
python -m tumnus.learn.train --trainfile train1.cut --testfile train1.cut --appname train --classifier xgb --vectorizer_type count --debug --bin_class -1
