# LSTM with dropout for sequence classification in the IMDB dataset
import numpy
import sys
from keras.datasets import imdb
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from sklearn import metrics






def train_model(datapath, useCNN=False, top_words=5000, max_rec_length=500):
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

if __name__=="__main__":

    if len(sys.argv) < 2:
        print('usage: lstm.py <dataset> [useCnn]')
        sys.exit(-1)

    dataset = sys.argv[1]
    useCNN = True if len(sys.argv)>=3 and sys.argv[2] !='false' else False
    runid = dataset[:dataset.rfind('.')]

    model, x_test, y_test = train_model(dataset, useCNN)
    eval_model(model, x_test, y_test, runid)


