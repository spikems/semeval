#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Converet dataset into Keras dataset format.

input format: (.cut file)
    label id content

output format:
    IMDB Movie reviews sentiment classification(https://keras.io/datasets/)
    (x_train, y_train), (x_test, y_test) = imdb.load_data(path="imdb.npz")

    x_train is encoded as sequence with word indexs, which start from 1 and sorted by frequency.

Usage:
    makenpz --train <trainset> --test <testset> --output <output>

"""

import string
import sys,time
import os, os.path
import logging
import numpy as np
from optparse import OptionParser

logger = logging.getLogger(__name__)

def load_cutfile(fileName):
    '''
    input:
        label id content
    return:
        data    ; [label, [words]]
    '''
    data = []
    if not os.path.exists(fileName):
        logger.error('load_cutfile fail as the file not exists: %s', fileName)
        return data

    reader = open(fileName, 'rb')
 
    reccnt = 0
    #
    # parse the records
    # id label hidden text
    #
    for line in reader:
        line = line.strip()
        #add a id 
        if line[0] == ' ':
            pos0 = line.find(' ')+1
        else:
            pos0 = 0
        pos1 = line.find(' ',pos0)+1
        pos2 = line.find(' ',pos1)+1

        if pos2 > 0:
            label = int(float(line[pos0:pos1-1]))
            stype = int(float(line[pos1:pos2-1]))
            content = line[pos2:-1]
            
            data.append([label, content.split()])

        reccnt += 1

    reader.close()
    logger.info('load_cutfile %s with %d records', fileName, reccnt)
    return data

def build_dict(data):
    """
    input:
        data    ; [[label, [words]]]
    return:
        list  ; [(word:freq)], sorted by freq
    """
    dictmap = {}

    #get frequecy
    for item in data:
        for word in item[1]:
            if word in dictmap:
                dictmap[word] += 1
            else:
                dictmap[word] = 1


    #sort by freq
    datalist = sorted(dictmap.items(), key=lambda x:x[1], reverse=True)

    #build a dictionary
    index = {}
    word_id = 1
    for word, freq in datalist:
        index[word] = word_id
        word_id += 1


    return datalist, index

def transform(data, wordindex):
    """
    input:
        data    ; [[label, [words]]]
        wordindex ;  {word:index}
    return:
        newdata ; word replaced by index(start from 1)
    """

    x = []
    y = []
    for item in data:
        y.append(item[0])
        line = []
        for word in item[1]:
            line.append(wordindex[word])
        x.append(line)

    return np.array(x), np.array(y)

def makedata(train, test, output = ''):
    """
    input:
        train, test ; filename
    output:
        output  ; .npz filename, 

    """
    data_train = load_cutfile(train)
    data_test = load_cutfile(test)

    if not (data_train and data_test):
        # fail
        return 

    trainCnt = len(data_train)
    logger.info('train set records count = %d', trainCnt)

    # build dictionary and transform
    data = []
    data.extend(data_train)
    data.extend(data_test)
    logger.info('trainset:%d, testset:%d, total:%d', 
            len(data_train), len(data_test), len(data))

    wordlist, wordindex = build_dict(data)
    x,y = transform(data, wordindex)

    #split to train and test
    #reset label to [0 1]
    y[y>=0] = 1
    y[y<0] = 0

    #save to file
    if output:
        #save word dictionary
        with open(output + '.vocab','w') as outf:
            for word, freq in wordlist:
                #outf.write('%s %d\n'%(word.encode('utf-8'), freq))
                outf.write('%s %d\n'%(word, freq))

        np.savez(output, x_train=x[:trainCnt], y_train=y[:trainCnt],
            x_test=x[trainCnt:],y_test=y[trainCnt:])

    return x, y, trainCnt, wordlist, wordindex

if __name__=="__main__":
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)

    # cmd argument parser
    usage = 'makenpz --train <trainset> --test <testset> --output <output>'
    parser = OptionParser(usage)
    parser.add_option("--train", dest="trainfile")
    parser.add_option("--test", dest="testfile")
    parser.add_option("--output", dest="outputfile", default='')
    opt, args = parser.parse_args()

    if not (opt.outputfile and opt.trainfile and opt.testfile):
        print(globals()['__doc__'] % locals())
        sys.exit(1)

    logger.info("running %s" % ' '.join(sys.argv))

    makedata(opt.trainfile, opt.testfile, opt.outputfile)
