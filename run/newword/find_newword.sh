
python -m mxword.newword.nwfinder -i ../dump_car_all.txt -o newwords_car_smalldict.txt --jieba=./smalldict/ --savelog

cat smalldict/auto/unknow_dir/* >newwords_car.userdict
