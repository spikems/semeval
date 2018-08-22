#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Remove records in the test set

input files: .cut
    label id content

output files:
    id grp(A,B,C) label predict oldlabel

Usage:
    removetest.py -i <input> -f <testset> -o <outfile name>

"""

import string
import sys,time
import os, os.path
import logging
from optparse import OptionParser


def read_file(fname):
    """
        return list of list[]
    """
    recs=[]
    logger.info('Start read file %s', fname)
    with open(fname) as inf:
        for line in inf:
            recs.append(line)
            #recs.append(line.strip().split())
    logger.info('End reading with recnumber %d', len(recs))
    return recs

def build_id_map(recs):
    """
        input: <label, id> list
        output: <id:lineid> dict
    """
    map = {}
    lineid = 0
    for items in recs:
        label, id = items.strip().split()[:2]
        map[id] = lineid
        lineid += 1

    return map

def remove_test(infile, testfile, outfile):
    '''
    '''
    inf = read_file(infile)
    testf = read_file(testfile)
    outf = open(outfile, 'w')

    #build a id,label mapping
    in_map = build_id_map(inf)
    test_map = build_id_map(testf)

    #remove recs in test
    for id in in_map:
        if not id in test_map:
            outf.write('%s'%inf[in_map[id]])


if __name__=="__main__":
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

    # cmd argument parser
    parser = OptionParser(globals()['__doc__'] % locals())
    parser.add_option("-i", dest="infile")
    parser.add_option("-t", dest="testfile")
    parser.add_option("-o", dest="outfile")
    opt, args = parser.parse_args()

    if opt.outfile is None:
        logger.error(globals()['__doc__'] % locals())
        sys.exit(1)

    remove_test(opt.infile, opt.testfile, opt.outfile)
