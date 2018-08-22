#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Create id mapping file

input format:
    label id text
output format:
    newid fileid id

Usage:
    mapping <file name> ...

"""

import string
import sys,time
import os, os.path
import logging
from optparse import OptionParser


def process_file(fileName, newid, fileid, writer, idf):
    '''
    cut from file and output to filename.cut
    '''
    reader = open(fileName, 'rb')
    #
    # parse the records
    # id label hidden text
    #
    errcnt = 0
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
            content = line[pos2:-1]
            recid = int(float(line[pos1:pos2-1]))

            idf.write('%d %d %d\n'%(newid, fileid, recid))
            writer.write('%d %d %s\n'%(label, newid, content))
            newid += 1
        else:
            errcnt += 1

    logger.info('process file %s with errcnt = %d', filename, errcnt)
    reader.close()
    return newid


if __name__=="__main__":
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

    # cmd argument parser
    if len(sys.argv) <2 :
        logger.error(globals()['__doc__'] % locals())
        sys.exit(1)
    
    newid, fileid = 0,0
    idf = open('idmap.txt','w')
    writer = open('all.cut','w')
    writer2 = open('filemap.txt','w')

    for filename in sys.argv[1:]:
        writer2.write('%d %s\n'%(fileid, filename))
        newid = process_file(filename, newid, fileid, writer, idf)
        fileid += 1

    idf.close()
    writer.close()
    writer2.close()

