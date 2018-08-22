#
# demo to build trainset, 
# for more details, refer to go_nextiter.sh and final_trainset.sh
#

python -m semeval.labelprocess.xlsx-yy trainset-v1.xlsx trainset-v1
gawk '{print $2,$1}' trainset-v1.txt >select.id
gawk '{print $2,$1}' labelset-v1.txt >>select.id
python -m semeval.labelprocess.combinexlsx --uselabel trainset-v2.xlsx
