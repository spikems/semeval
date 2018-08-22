#
# demo to predict 
#

#
# prepare input .xlsx and model file
#
ln -s $_semevalproject_/run/trainmodel/model/model_car_xgb.pkl model_car_xgb.pkl
ln -s $_semevalproject_/data/trainset/car/labelset-v1.xlsx input.xlsx

#
# dump data
#
python -m semeval.labelprocess.xlsx-yy input.xlsx input
python -m semeval.labelprocess.cut -f input.txt 
python -m semeval.labelprocess.mapping sinput.cut 

#
# predict
#
python -m tumnus.learn.train --testmodel model_car_xgb --testfile all.cut --appname _predict

#
# output to output.xlsx, sort by probability of neg
#
sort -nr -k 4 model_car_xgb_predict.prob | gawk '{print $1,$3}' >select.id
python -m semeval.labelprocess.combinexlsx --uselabel --useoldid output.xlsx
