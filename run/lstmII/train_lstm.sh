#build trainset


#train
python -m tumnus.lstm.filtercut --tags '#,x,n,v,a' --input v2-all-new.cut --output v2-xnva.cut
python -m tumnus.preprocess.stratesample v2-xnva.cut xnva 0.8
python -m tumnus.lstm.train_lstm --trainfile train-r-xnva --testfile test-r-xnva
