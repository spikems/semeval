#!/bin/bash

#
# validate that adding feature can really improve the performance, especially the recall
#
homedir=$_semevalproject_
if [ -z $homedir ] ; then
    echo 'init semeval environment first please, quit...'
    exit 0
fi

#
# check the installation of deep learning tool 
#
python -m tumnus.lstm.deep_versions
#theano: 0.9.0.dev-c697eeab84e5b8a74908da654b66ec9eca4f1291
#tensorflow: 1.2.1
#Using TensorFlow backend.
#keras: 2.0.6

#
# prepare data
#
cp $homedir/data/trainset/car/dataset-v5-dedup.xlsx .
cp $homedir/data/testset/car/car_test_20170811.xlsx .

python -m semeval.labelprocess.xlsx-yy dataset-v5-dedup.xlsx dataset-v5-dedup
python -m semeval.labelprocess.xlsx-yy car_test_20170811.xlsx car_test_1k

mkdir -p feature_dicts
cp $homedir/data/feature_dict/car/v2/*.dict feature_dicts
mkdir -p jieba_dict
cp $homedir/data/jieba_dict/dict.txt.small jieba_dict/dict.txt

# rebuild userdict
python -m tumnus.learn.buildfeature -o car.userdict --jieba jieba_dict/ --dict feature_dicts/ --builduserdict

# cut by new feature dicts
python -m tumnus.learn.buildfeature -i dataset-v5-dedup.txt -o v5-all-new.cut --userdict car.userdict --dict feature_dicts/ --dat dataset-v5-dedup.dat
# select featuretag as features
python -m tumnus.learn.buildfeature -i v5-all-new.cut -o v5-feature-new.cut --selectfeature 0

python -m tumnus.learn.buildfeature -i car_test_1k.txt -o car_test_1k.cut --userdict car.userdict --dict feature_dicts/ --dat car_test_1k.dat
python -m tumnus.learn.buildfeature -i car_test_1k.cut -o car_test_1k_fe.cut --selectfeature 0

#
#make the dataset for keras
#
python -m tumnus.lstm.makenpz --train v5-all-new.cut --test car_test_1k.cut --output car-v5-raw-test1k.npz
python -m tumnus.lstm.makenpz --train v5-feature-new.cut --test car_test_1k_fe.cut --output car-v5-fe-test1k.npz

cp *.npz ~/.keras/datasets/

#
# train by lstm
#
python -m tumnus.lstm.train_lstm car-v5-raw-test1k.npz
python -m tumnus.lstm.train_lstm car-v5-fe-test1k.npz
#python -m tumnus.lstm.train_lstm car-v5-fe-test1k.npz useCNN
#python -m tumnus.lstm.train_lstm car-v5-raw-test1k.npz useCNN
