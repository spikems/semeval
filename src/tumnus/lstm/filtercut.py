#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

input format: (.cut file)
    label id content

output format:

Usage:
    filtercut --tags <pos tags> --replace --input <.cut> --output <output>

"""

import string
import sys,time
import os, os.path
import logging
import numpy as np
from optparse import OptionParser

def makedata(tags, fileName, outputfile, replace = False):
    '''
    input:
        label id content
    return:
        data    ; [label, [words]]
    '''

    tags= tags.split(',')


    data = []
    if not os.path.exists(fileName):
        logger.error('load_cutfile fail as the file not exists: %s', fileName)
        return data

    writer = open(outputfile, 'w')
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
            content = line[pos2:-1].split()
            
            #filtering by tags
            out = []
            for item in content:
                cells = item.split('/')
                if len(cells) > 1:
                    if replace:
                        #replace mode
                        match = False
                        for tag in tags:
                            if tag in cells[1]:
                                #a tag match
                                out.append(cells[1])
                                match = True
                                break
                        if match == False:
                            out.append(cells[0])
                    else:
                        #filter mode
                        for tag in tags:
                            if tag in cells[1]:
                                #a tag match
                                out.append(cells[0])
            
            writer.write('%d %d %s\n'%(label, stype, ' '.join(out)))


        reccnt += 1

    reader.close()
    logger.info('load_cutfile %s with %d records', fileName, reccnt)
    return data

if __name__=="__main__":
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)

    # cmd argument parser
    usage = 'filtercut --tags <pos tags> --input <.cut> --output <output>'
    parser = OptionParser(usage)
    parser.add_option("--input", dest="inputfile")
    parser.add_option("--output", dest="outputfile")
    parser.add_option("--replace", action="store_true", help='set to replace word with pos tag')
    parser.add_option("--tags", dest="tags", default='#,x')
    opt, args = parser.parse_args()

    if not (opt.outputfile and opt.inputfile):
        print(globals()['__doc__'] % locals())
        sys.exit(1)

    logger.info("running %s" % ' '.join(sys.argv))

    makedata(opt.tags, opt.inputfile, opt.outputfile, opt.replace)
