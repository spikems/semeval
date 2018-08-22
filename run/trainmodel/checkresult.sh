#!/bin/bash

if [ $# -ne "2" ]; then
    echo "output html file for better view of the prediction results"
    echo "need to read .coef file, which is only support by lr,lsvc models"
    echo ""
    echo "checkresult.sh <checktype> <modelame>"
    echo "  checktype: truelabel+predictlabel as the checktype, e.g., "
    echo "      01 means check records neg but predicted as pos"
    echo "  modelname: output .pkl filename by tumnus.learn.train"
    exit 0
fi

python -m tumnus.postprocess.res2html --filter $1 $2

