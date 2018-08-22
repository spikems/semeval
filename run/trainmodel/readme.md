trainmodel
===============

steps to train a useful model:

1. prepare the trainset, split to train/test sets

2. try standard models, try semeval.sh, or searcheval.sh

3. feature filtering, edit .chi2 file to remove useless features such as brand name, location name etc.

4. re-train a model by filtered vocabulary, use fasteval.sh

5. check the results and investigate the reasons of error, use python -m tumnus.postprocess.res2html --filter 01 

refer demo.sh for details
