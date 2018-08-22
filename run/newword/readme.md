newword
=============

learn the new words:

    python -m mxword.newword.nwfinder -i ../dump_car_all.txt -o newwords_car_smalldict.txt --jieba=/tmp/hpda/next/labelprocess/newword/smalldict/ --savelog

    cat auto/unknow_dir/* >newwords_car.userdict

use the userdict:

    python -m semeval.labelprocess.cut --userdict=USERDICT -f input.txt

