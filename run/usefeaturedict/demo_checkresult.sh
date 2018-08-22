#
# demo to use the checkresult tool
#
#Create a html view for prediction result files.
#1. Tool to help do feature engineering.
#2. Highlight the features used in model. 
#   If .coef file given, the neg/pos will be highlight as blue/red.
#   If .color file given, the features will be highlight by color.
#
#This tool replace the old res2html.
#
#
#Usage: checkres.py [options] resfile
#
#Options:
#  -h, --help            show this help message and exit
#  --filter=FILTER       set the filter pattern <true_y, pred_y>,'all' by
#                        default, '01' is most used.
#  --datfile=DATFILE     set the dat file name to get properties of reacords,
#                        such as target name.
#  --vocabfile=VOCABFILE
#                        set the source .vocab file contain the features.
#  --cutfile=CUTFILE     set the source .cut file contain the original
#                        contents.
#  --colorfile=COLORFILE
#                        set the color map file name to coloring the features.
#  --useprob             set to use the .prob file to sort the result by
#                        probability.
#  --usecoef             set to use the .coef file to weight the color of
#                        features.
#  --tagmode             set to use tag as features instead using words.
#


source /tmp/hpda/next/semeval/bin/init_env.sh 

#
# compatible with old res2html
#
mkdir nofeaturetag
cd nofeaturetag

cp ../../../trainmodel/test-r-v4 .
cp ../../../trainmodel/dataset-v4-dedup.* .
cp ../../../trainmodel/demo/semeval_car_lr_balanced_l1_count_0.* .
#
# check by vocab file
#
cp ../../../trainmodel/demo/v2_vocab.txt .
python -m tumnus.postprocess.checkresult --filter 01 --dat dataset-v4-dedup.dat --vocabfile v2_vocab.txt semeval_car_lr_balanced_l1_count_0.res 
#
# check by .coef file, color by weight
#
python -m tumnus.postprocess.checkresult --filter 01 --dat dataset-v4-dedup.dat --usecoef semeval_car_lr_balanced_l1_count_0.res 


#
# check feature dict result
#
mkdir usefeaturedict
cd usefeaturedict

# create the cut file by feature dict
#python -m tumnus.learn.buildfeature --userdict car.userdict --dict feature_dicts/ --dat dataset-v4-dedup.dat -i dataset-v4-dedup.txt -o v4-all-tag.cut

cp ../../dataset-v4-dedup.* .
cp ../../demo/new_xgb_no_count_0.* .
cp ../../v4-all-tag.cut .

#
# tag mode, and use cut file to show original contents
#
python -m tumnus.postprocess.checkresult --filter 01 --dat dataset-v4-dedup.dat --colorfile car.colormap --cutfile v4-all-tag.cut --useprob --tagmode new_xgb_no_count_0.res 2>&1 |tee log

#
# output .html, open it
#


