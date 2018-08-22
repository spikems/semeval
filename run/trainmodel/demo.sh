#
# demo to show the process of training
#

python -m semeval.labelprocess.xlsx-yy ../trainset/dataset-v4-dedup.xlsx dataset-v4-dedup
python -m semeval.labelprocess.cut -f dataset-v4-dedup.txt
python -m tumnus.preprocess.stratesample sdataset-v4-dedup.cut v4 0.8

##
## 1_use_userdict
##
#python -m semeval.labelprocess.cut --userdict newwords_car.userdict -f dataset-v4-dedup.txt
#python -m tumnus.preprocess.stratesample sdataset-v4-dedup.cut v4 0.8
#./semeval.sh train-r-v4 test-r-v4 
#
##
## 0_original_tumus
##
#python -m semeval.labelprocess.cut -f dataset-v4-dedup.txt
#python -m tumnus.preprocess.stratesample sdataset-v4-dedup.cut v4-oringal 0.8
#./semeval.sh train-r-v4-oringal test-r-v4-oringal

#
# baseline training
#
./semeval.sh train-r-v4 test-r-v4 

#
# feature filtering
#
cd demo/
cp ../v2_vocab.txt .
../fasteval.sh xgb ../v2_vocab.txt v2
cd ..


#
# checkresult
# 
./checkresult.sh 01 demo/semeval_car_lr_balanced_l1_count_0
