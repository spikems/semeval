train lstm model
======================

### basic model

http://machinelearningmastery.com/sequence-classification-lstm-recurrent-neural-networks-python-keras/

Sequence classification is a predictive modeling problem where you have some sequence of inputs over space or time and the task is to predict a category for the sequence.

What makes this problem difficult is that the sequences can vary in length, be comprised of a very large vocabulary of input symbols and may require the model to learn the long-term context or dependencies between symbols in the input sequence.

### dataset format

[Large Movie Review Dataset](http://ai.stanford.edu/~amaas/data/sentiment/)

25,000 highly polar movie reviews for training, and 25,000 for testing.

```py

import keras.datasets import imdb

(x_train, y_train), (x_test, y_test) = imdb.load_data(path="imdb.npz",
        num_words=None,
        skip_top=0,
        maxlen=None,
        seed=113,
        start_char=1,
        oov_char=2,
        index_from=3)
```

- x_train, x_test: list of sequences, which are lists of indexes (integers). If the num_words argument was specific, the maximum possible index value is num_words-1. If the maxlen argument was specified, the largest possible sequence length is maxlen.
- y_train, y_test: list of integer labels (1 or 0).

### install keras and deep learning engine

http://machinelearningmastery.com/setup-python-environment-machine-learning-deep-learning-anaconda/

https://www.tensorflow.org/install/install_linux#NVIDIARequirements

```sh

$ conda create -n tensorflow
$ source activate tensorflow
pip install --ignore-installed --upgrade
#https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow_gpu-1.2.1-cp27-none-linux_x86_64.whl

```

### howto save and load lstm model

https://keras.io/getting-started/faq/

```py
from keras.models import load_model

model.save('my_model.h5')  # creates a HDF5 file 'my_model.h5'
del model  # deletes the existing model

# returns a compiled model
# identical to the previous one
model = load_model('my_model.h5')
```

### test on car dataset -v5-

refer to /run/lstmtest/demo_lstm.sh

```sh

(tensorflow) [pengb@r-003 car-v5]$ python -m tumnus.lstm.train_lstm car-v5-raw-test1k.npz
accuracy: 0.962
precision: [ 0.42105263 0.98924731]
recall: [ 0.66666667 0.97097625]
f1 score: [ 0.51612903 0.98002663]
confusion matrix:
[[ 16 8]
 [ 22 736]]

```

### Conclusions 

* When train lstm model on car dataset, it does not show a decent performance when trained without feature extraction. 
* When trained with feature extraction, lstm doest not get significant better performance than xgb.
* Current testset is only 1k with 25 neg class items. A larger testset is prefered for future experiments.






