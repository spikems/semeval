#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Cutword for sentiment dataset

input format:
    id sentitype text

Usage:
    cut -t [pos] -c [hidden]  -f <file name>
        -t  ; save pos tag
        -c  ; output <hidden, text cut>, otherwise output <senti,  text cut> by default
        -f  ; input file name

"""

import string
import sys,time
import os, os.path
import logging
import jieba
from jieba.norm import norm_cut, norm_seg
from optparse import OptionParser

def cut_test():
    '''
    cut from std input
    '''
    logger.info('Enter test mode, q to quit')
    line = raw_input()
    while(line != 'q'):
        result = norm_seg(line.strip())
        wordsList = []
        for w in result:
            wordsList.append(w.word + '/' + w.flag)
        words = " ".join(wordsList)
        print(words.encode('utf-8'))

        line = raw_input()

def cut_input(input, posFlag):
    '''
    cut a input string, return utf-8 string
    '''

    if posFlag == True:
        result = norm_seg(input)
        wordsList = []
        for w in result:
            wordsList.append(w.word + '_' + w.flag)
        words = " ".join(wordsList)
    else:
        words = " ".join(norm_cut(input))
    #return words.encode('utf-8')
    return words
     

def cut_file(fileName, posFlag, column):
    '''
    cut from file and output to filename.cut
    '''
    dir, name = os.path.splitext(fileName)
    prefix = 's' if column ==0 else 'h'
    writer = open( prefix + dir + '.cut', 'w')
    reader = open(fileName, 'rb')
 
    reccnt = 0
    #
    # parse the records
    # id label hidden text
    #
    for line in reader:
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

            #result = " %d"%reccnt + cut_input(content, posFlag)
            result = cut_input(content, posFlag)
            if column == 0:
                #writer.write('%d %d '%(stype,label) + result.encode('utf-8') + '\n')
                writer.write('%d %d '%(label, stype) + result.encode('utf-8') + '\n')
            else:
                writer.write('%d %d '%(int(float(hidden)), label) + result.encode('utf-8') + '\n')

        reccnt += 1

    reader.close()
    writer.close()


if __name__=="__main__":
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

    # cmd argument parser
    usage = 'cut -t [pos] -c [hidden]  -f <file name>'
    parser = OptionParser(usage)
    parser.add_option("-f", dest="pathName")
    parser.add_option("-t", dest="type")
    parser.add_option("-c", dest="column")
    parser.add_option("--userdict", dest="userdict", default='')
    opt, args = parser.parse_args()

    #load user dict
    if opt.userdict:
        logger.info('loading userdict %s...', opt.userdict)
        jieba.load_userdict(opt.userdict)


    if opt.pathName is None:
        logger.error(globals()['__doc__'] % locals())

        #enter test mode
        cut_test()

        sys.exit(1)

    posFlag = False
    column = 0  #'senti'
    if not (opt.type is None):
        posFlag = True
    if not (opt.column is None):
        column = 1  #'hidden'

    #cut
    arg_name = opt.pathName 
    if os.path.isdir(arg_name):
        for root, dirs, files in os.walk(arg_name):
            #print root, dirs, files
            for file_name in files:
                cut_file( root + '/' + file_name, posFlag, column)
            break    
    else:
        cut_file( arg_name, posFlag, column)
