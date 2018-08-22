# cut by feature dictionary
python -m semeval.labelprocess.mapping car_05262017.txt car_08122016.txt
gawk '{print $2,$1}' all.cut >select.id
python -m semeval.labelprocess.combinexlsx --uselabel car_all.xlsx
python -m semeval.labelprocess.xlsx-yy car_all.xlsx car_all
mkdir -p feature_dicts
cp ~/hpda/semeval/data/feature_dict/car/v2/* feature_dicts/
python -m tumnus.learn.buildfeature -i car_all.txt -o car_all.cut --userdict car.userdict --dict feature_dicts/ --dat car_all.dat

#
#replace #, replace all #brand, and #target
#
python -m tumnus.lstm.filtercut --tags '#' --replace --input car_all.dat --output car_all-replace.cut

#train model, output word2vec.model
python -m tumnus.learn.word2vec car_all-replace.cut


