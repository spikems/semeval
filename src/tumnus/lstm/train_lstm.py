#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A LSTM trainer

Usage: trainlstm.py -h for help

"""

import logging
import numpy as np
from optparse import OptionParser
import sys, os
from time import time
from sklearn import metrics
from gensim.models import KeyedVectors

from keras.models import Sequential
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D
from keras.preprocessing import sequence
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Dense, Input, LSTM, Embedding, Dropout, Activation
from keras.models import Model
from keras.layers.normalization import BatchNormalization
from keras.callbacks import EarlyStopping, ModelCheckpoint

from .makenpz import makedata

logger = logging.getLogger(__name__)
#Global settings
MAX_NB_WORDS = 500000

def savelist(filename, lst):
    with open(filename, 'w') as outf:
        for w in lst:
            if type(w) == unicode:
                outf.write('%s\n'%(w.encode('utf-8')))
            else:
                outf.write('%s\n'%(w))


def train(opts):
    '''
    Load dataset from the raw .cut files.
    Refer to imdb.load_data code
    https://github.com/fchollet/keras/blob/master/keras/datasets/imdb.py

    training code refer to:
    https://www.kaggle.com/lystdo/lstm-with-word2vec-embeddings

    '''
    #load data
    x,y,trainCnt,wordlist, wordindex = makedata(opts.trainfile, opts.testfile)

    #padding
    xdata = pad_sequences(x, maxlen= opts.max_seq_len)
    #ydata = pad_sequences(y, maxlen= opts.max_seq_len)
    ydata = y

    #train/validation split
    if opts.validation_split != 0:
        logger.info('validation split as %s', opts.validation_split)
        perm = np.random.permutation(trainCnt)

        subCnt = int(trainCnt*(1-opts.validation_split))
        idx_train = perm[:subCnt]
        idx_val = perm[subCnt:trainCnt]

        data_train = xdata[idx_train]
        data_val = xdata[idx_val]
        data_test = xdata[trainCnt:]

        label_train = ydata[idx_train]
        label_val = ydata[idx_val]
        label_test = ydata[trainCnt:]
    else:
        data_train = xdata[:trainCnt]
        data_test = xdata[trainCnt:]
        label_train = ydata[:trainCnt]
        label_test = ydata[trainCnt:]
        data_val = []
        label_val = []

    ## add class weight
    ratioNeg = (np.sum(label_test[:] == 0) * data_train.shape[0])*1.0 / \
               (np.sum(label_train[:] == 0) * data_test.shape[0]) 
    ratioPos = (np.sum(label_test[:] == 1) * data_train.shape[0])*1.0 / \
               (np.sum(label_train[:] == 1) * data_test.shape[0])
        
    if opts.re_weight:
        class_weight = {0: ratioNeg, 1: ratioPos}
    else:
        class_weight = {0: 1., 1: 1.}

    weight_val = np.ones(len(label_val))
    if opts.re_weight:
        weight_val *= ratioPos
        weight_val[labels_val==0] = ratioNeg

    logger.info('dataset ready, trainCnt=%d, validationCnt=%d, testCnt=%d, class_weight=%s', \
            data_train.shape[0], data_val.shape[0], data_test.shape[0], class_weight)


    #load embedding
    if os.path.exists(opts.word2vec_model):
        #word2vec = KeyedVectors.load_word2vec_format(opts.word2vec_model, binary=True)
        word2vec = KeyedVectors.load_word2vec_format(opts.word2vec_model, binary=False)
        EMBEDDING_DIM = word2vec.word_vec(word2vec.index2word[0]).shape[0]
        logger.info('Found %sx%s word vectors of word2vec model %s',len(word2vec.vocab), EMBEDDING_DIM, opts.word2vec_model)

        nb_words = min(MAX_NB_WORDS, len(wordindex))+1
        
        embedding_matrix = np.zeros((nb_words, EMBEDDING_DIM))
        
        nullword = []
        #test vocab
        #testkw = []
        #for kw in word2vec.vocab:
        #    testkw.append(kw)
        #    if len(testkw) > 10:
        #        break
        #logger.info('word2vec.voacb type:%s', ' '.join([type(x) for x in testkw]))
        #logger.info('word2vec.voacb items:%s', ' '.join([x.encode('utf-8') for x in testkw]))

        for word, i in wordindex.items():
            #vocab is unicode, wordindex is utf-8
            #word = unicode(word)
            try:
                wordx = word.decode('utf-8')
            except:
                wordx = word

            if wordx in word2vec.vocab:
                embedding_matrix[i] = word2vec.word_vec(wordx)
            else:
                nullword.append(wordx)

        savelist('nullword.lst', nullword)
        savelist('wordindex.lst', wordindex)
        logger.info('Null word embeddings: %d' % np.sum(np.sum(embedding_matrix, axis=1) == 0))


    #define the model structure
    num_lstm = opts.lstm_len
    num_dense = opts.dense_len
    rate_drop_lstm = opts.dropout_lstm
    rate_drop_dense = opts.dropout_dense
    MAX_SEQUENCE_LENGTH = opts.max_seq_len

    embedding_layer = Embedding(nb_words,
                    EMBEDDING_DIM,
                    weights=[embedding_matrix],
                    input_length=opts.max_seq_len,
                    trainable=False)
    lstm_layer = LSTM(num_lstm, dropout=rate_drop_lstm, recurrent_dropout=rate_drop_lstm)

    sequence_1_input = Input(shape=(MAX_SEQUENCE_LENGTH,), dtype='int32')
    embedded_sequences_1 = embedding_layer(sequence_1_input)
    x1 = lstm_layer(embedded_sequences_1)

    #merged = concatenate([x1, y1])
    merged = x1
    merged = Dropout(rate_drop_dense)(merged)
    merged = BatchNormalization()(merged)

    merged = Dense(num_dense, activation='relu')(merged)
    merged = Dropout(rate_drop_dense)(merged)
    merged = BatchNormalization()(merged)

    preds = Dense(1, activation='sigmoid')(merged)

    ## train the model
    model = Model(inputs=sequence_1_input, \
                    outputs=preds)
    model.compile(loss='binary_crossentropy',
                    optimizer='nadam',
                    metrics=['acc'])

    #train the model
    STAMP = 'lstm_%d_%d_%.2f_%.2f'%(num_lstm, num_dense, rate_drop_lstm, rate_drop_dense)
    logger.info(STAMP)
    bst_model_path = STAMP + '.h5'
    early_stopping =EarlyStopping(monitor='val_loss', patience=3)
    bst_model_path = STAMP + '.h5'
    model_checkpoint = ModelCheckpoint(bst_model_path, save_best_only=True, save_weights_only=True)

    hist = model.fit(data_train, label_train, \
                    validation_data=(data_val, label_val, weight_val), \
                    epochs=opts.epoch, batch_size=opts.batchsize, shuffle=True, \
                    class_weight=class_weight, callbacks=[early_stopping, model_checkpoint])

    #hist = model.fit(data_train, label_train, \
    #                epochs=opts.epoch, batch_size=opts.batchsize, shuffle=True, verbose=1)

    model.load_weights(bst_model_path)
    bst_val_score = min(hist.history['val_loss'])

    #predict on test
    y_proba = model.predict(data_test, batch_size=8192, verbose=0)
    pred = (y_proba > 0.5).astype('int32')
    y_test = label_test

    precision = metrics.precision_score(y_test, pred, average=None)
    recall = metrics.recall_score(y_test, pred, average=None)
    score = metrics.accuracy_score(y_test, pred)
    f1_score = metrics.f1_score(y_test, pred, average=None)
    print("accuracy:   %0.3f" % score)
    print("precision:   %s" % precision)
    print("recall:   %s" % recall)
    print("f1 score:   %s" % f1_score) 
    
    print("confusion matrix:")
    cmstr = metrics.confusion_matrix(y_test, pred)
    print(cmstr)

    #save result to file
    with open(STAMP + '.cm','w') as outf:
        outf.write("%s\n"%model.summary())
        outf.write("accuracy:   %0.3f\n" % score)
        outf.write("precision:   %s\n" % precision)
        outf.write("recall:   %s\n" % recall)
        outf.write("f1 score:   %s\n" % f1_score) 
        outf.write("confusion matrix:")
        outf.write("%s\n"%cmstr)

    return


def train_model_old(datapath, useCNN=False, top_words=5000, max_rec_length=500):
    # fix random seed for reproducibility
    numpy.random.seed(7)
    # load the dataset but only keep the top n words, zero the rest
    #top_words = 5000
    
    print('Start training path=%s, useCNN=%s', datapath, useCNN)
    
    (X_train, y_train), (X_test, y_test) = imdb.load_data(path=datapath
            ,num_words=top_words)
    
    print('records = %s'% X_train.shape)
    
    # truncate and pad input sequences
    max_review_length = max_rec_length
    X_train = sequence.pad_sequences(X_train, maxlen=max_review_length)
    X_test = sequence.pad_sequences(X_test, maxlen=max_review_length)

    # create the model
    embedding_vecor_length = 32
    model = Sequential()
    model.add(Embedding(top_words, embedding_vecor_length, input_length=max_review_length))
    
    if useCNN:
        model.add(Conv1D(filters=32, kernel_size=3, padding='same', activation='relu'))
        model.add(MaxPooling1D(pool_size=2))
        model.add(LSTM(100))
    else:
        model.add(LSTM(100, dropout=0.2, recurrent_dropout=0.2))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    print(model.summary())
    model.fit(X_train, y_train, epochs=10, batch_size=64)
    return model, X_test, y_test

def eval_model(model, X_test, y_test, runid):
    # Final evaluation of the model
    #scores = model.evaluate(X_test, y_test, verbose=0)
    #print("Accuracy: %.2f%%" % (scores[1]*100))
    
    #predict and evaluate by sklearn
    y_proba = model.predict(X_test, verbose=0)
    pred = (y_proba > 0.5).astype('int32')
    
    precision = metrics.precision_score(y_test, pred, average=None)
    recall = metrics.recall_score(y_test, pred, average=None)
    score = metrics.accuracy_score(y_test, pred)
    f1_score = metrics.f1_score(y_test, pred, average=None)
    print("accuracy:   %0.3f" % score)
    print("precision:   %s" % precision)
    print("recall:   %s" % recall)
    print("f1 score:   %s" % f1_score) 
    
    print("confusion matrix:")
    cmstr = metrics.confusion_matrix(y_test, pred)
    print(cmstr)

    #save result to file
    with open(runid + '.cm','w') as outf:
        outf.write("%s\n"%model.summary())
        outf.write("accuracy:   %0.3f\n" % score)
        outf.write("precision:   %s\n" % precision)
        outf.write("recall:   %s\n" % recall)
        outf.write("f1 score:   %s\n" % f1_score) 
        outf.write("confusion matrix:")
        outf.write(cmstr)


# parse commandline arguments
def load_option():
    op = OptionParser()

    # dataset
    op.add_option("--trainfile",
                  action="store", type=str, default="train.cut", 
                  help="define the train dataset file name, train.cut by default.")
    op.add_option("--testfile",
                  action="store", type=str, default="test.cut", 
                  help="define the test dataset file name, test.cut by default.")
    op.add_option("--validation_split",
                  action="store", type=float, default="0.1", 
                  help="define the ratio of validation datasset, subset from trainset is selected out as validation dataset.")
    op.add_option("--re_weight",
                  action="store_true", 
                  help="Set to balanced class weight.")
 
    # model structure
    op.add_option("--max_seq_len",
                  action="store", type=int, default="64",
                  help="Define the max record length, 64 by default.")
    op.add_option("--lstm_len",
                  action="store", type=int, default=200,
                  help="Define the neurons of lstm layer, 200 by default.")
    op.add_option("--dense_len",
                  action="store", type=int, default=100,
                  help="Define the neurons of dense layer, 100 by default.")
    
    op.add_option("--word2vec_model",
                  action="store", type=str, default="word2vec.model", 
                  help="Load a pre-trained word2vec model if set, otherwise train on the trainset.")
    op.add_option("--dropout_lstm",
                  action="store", type=float, default="0.2", 
                  help="define the value of lstm layer dropout, 0.2 by default.")
    op.add_option("--dropout_dense",
                  action="store", type=float, default="0.2", 
                  help="define the value of dense layer dropout, 0.2 by default.")
    
    op.add_option("--usecnn",
                  action="store_true",
                  help="set to use a cnn layer(filtes=32,kernel_size=3,act=relu).")

    # training parameters
    op.add_option("--epoch",
                  action="store", type=int, default="200",
                  help="Define the max epoch number, 200 by default.")

    op.add_option("--batchsize",
                  action="store", type=int, default="2048",
                  help="Define the mini batch size, 2048 by default.")

    op.add_option("--debug",
                  action="store_true", 
                  help="Show debug info.")
    op.add_option("--h",
                  action="store_true", dest="print_help",
                  help="Show help info.")
    
    (opts, args) = op.parse_args()
   
    if opts.print_help:
        print(__doc__)
        op.print_help()
        print()
        sys.exit(0)

    logger.info('Start lstm training:[%s]',opts)
    return opts


if __name__=="__main__":
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

    opts = load_option()
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(-1)

    # check data
    if not (os.path.exists(opts.trainfile) and os.path.exists(opts.testfile)):
        logger.error('train and test file not exitst, quit')
        sys.exit(-1)
    
    if opts.word2vec_model and (not os.path.exists(opts.word2vec_model)):
        logger.error('word2vec model file not exitst, quit')
        sys.exit(-1)

    #train it
    train(opts)
