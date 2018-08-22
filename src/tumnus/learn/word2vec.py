#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
build word2vec model from text

input format:
    .cut
    label id content

output files:
    save word2vec model file

Usage:
    word2vec.py --output <word2vec.model> <infiles...>

"""

import string
import sys,time
import os, os.path
import random
import logging
import numpy as np
from optparse import OptionParser
from gensim.models.word2vec import Word2Vec
from gensim.models import KeyedVectors
#from classifier import load_file 

class Bunch(dict):
    """Container object for datasets
    Dictionary-like object that exposes its keys as attributes.
    >>> b = Bunch(a=1, b=2)
    >>> b['b']
    2
    >>> b.b
    2
    >>> b.a = 3
    >>> b['a']
    3
    >>> b.c = 6
    >>> b['c']
    6
    """

    def __init__(self, **kwargs):
        dict.__init__(self, kwargs)

    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setstate__(self, state):
        # Bunch pickles generated with scikit-learn 0.16.* have an non
        # empty __dict__. This causes a surprising behaviour when
        # loading these pickles scikit-learn 0.17: reading bunch.key
        # uses __dict__ but assigning to bunch.key use __setattr__ and
        # only changes bunch['key']. More details can be found at:
        # https://github.com/scikit-learn/scikit-learn/issues/6196.
        # Overriding __setstate__ to be a noop has the effect of
        # ignoring the pickled __dict__
        pass

def load_file(fname):
    """Load and return the dataset (classification).
       -1 23456 content...
    """
    data = []
    target = []
    ids = []
    with open(fname, 'r') as inf:
        for line in inf:
            line = line.strip()

            pos1 = line.find(' ')
            #put the id into data, extract into X_id in the future
            pos2 = line.find(' ', pos1+1)
            #pos2 = pos1
            ids.append(line[pos1+1:pos2])

            features = []
            words = line[pos2+1:].split(' ')
            for w in words:
                #add special comb feature pass-through
                if w.find('#') > 0:
                    features.append(w)
                else:
                    features.append(w)
            data.append(" ".join(features))

            target.append(int(line[:pos1]))

    return Bunch(data=data, target=target, ids=ids)


class W2V:
    def __init__(self):
        self.data = []
        self.w2v = None

    def load_data(self, fname):
        data = load_file(fname)
        self.data.extend(data.data)

    def train(self, size=600, min_count=5, sg=1, iter=20, workers=16):
        _data = [x.decode('utf-8').split() for x in self.data]
        token_count = sum([len(sentence) for sentence in _data])
        #Initialize model and build vocab
        #self.w2v = Word2Vec(size=600, min_count=5, sg=1, iter=20)
        self.w2v = Word2Vec(size=size, min_count=min_count, sg=sg, iter=iter, workers=workers)
        self.w2v.build_vocab(_data, keep_raw_vocab=False)
        #self.w2v.train(_data, total_examples=w2v.corpus_count)
        self.w2v.train(_data, total_examples = token_count, epochs = self.w2v.iter)

    def save(self, fname):
        self.w2v.save_word2vec_format(fname)

    def print_model(self, modelfile):
        """
        print the model, save the word name into output
        """
        if os.path.exists(modelfile):
            word2vec = KeyedVectors.load_word2vec_format(modelfile, binary=False)
            EMBEDDING_DIM = word2vec.word_vec(word2vec.index2word[0]).shape[0]
            logger.info('Found %sx%s word vectors of word2vec model %s',len(word2vec.vocab), EMBEDDING_DIM, modelfile)
            with open(modelfile + '.word', 'w') as outf:
                for w in word2vec.vocab:
                    outf.write('%s\n'%(w.encode('utf-8')))
                    #outf.write('%s\n'%(w))




def load_option():
    op = OptionParser()
    op.add_option("--print",
                  action="store_true", dest="print_model",
                  help="Set to print the model.")
    op.add_option("--output",
                  action="store", type=str, default="word2vec.model", dest="output_fname",
                  help="Output model file name.")
 
    (opts, args) = op.parse_args()
    return opts, args

if __name__=="__main__":
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))

    if len(sys.argv) < 2:
        logger.error(globals()['__doc__'] % locals())
        sys.exit(1)

    # cmd argument parser
    opts, args = load_option()

    w2v = W2V()

    if opts.print_model:
        #print
        w2v.print_model(args[0])

    else:
        #train
        for infile in args:
            logger.info('loadint %s', infile)
            w2v.load_data(infile)

        w2v.train()
        w2v.save(opts.output_fname)


