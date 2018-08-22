python -m tumnus.preprocess.stratesample $1 v4 0.8

# train model
mkdir -p demo
cd demo
ln -s ../train-r-v4 train1.cut
ln -s ../test-r-v4 test1.cut

python -m tumnus.learn.train --trainfile train1.cut --testfile test1.cut --appname test --classifier xgb --vectorizer_type count --debug --bin_class -1
python -m tumnus.learn.train --trainfile train1.cut --testfile train1.cut --appname train --classifier xgb --vectorizer_type count --debug --bin_class -1
