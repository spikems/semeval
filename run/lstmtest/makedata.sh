 python -m tumnus.preprocess.stratesample v5-all-new.cut v5-raw 0.8
 python -m tumnus.lstm.makenpz --train train-r-v5-raw --test test-r-v5-raw --output car-v5-raw.npz
 python -m tumnus.lstm.makenpz --train train-r-v5 --test test-r-v5 --output car-v5-fe.npz
 cp car-v5*.npz ~/.keras/datasets/
