#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Check the label result

input files:
    oldlabel: cut/all.cut
    newlabel: sdump.cut 
    dedup id: dedup/ddump.cut.grp
    predict : dedup/sdump.cut  (10000A, 5000B, 5000C)

output files:
    id grp(A,B,C) label predict oldlabel

Usage:
    checklabel.py -o <outfile name>

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
            recs.append(line.strip().split())
    logger.info('End reading with recnumber %d', len(recs))
    return recs

def build_id_map(recs):
    """
        input: <label, id> list
        output: <id:label> dict
    """
    map = {}
    for items in recs:
        label, id = items[:2]
        map[id] = label

    return map

def build_grp_map(map, recs, grpid):
    """
        input: <id >
        output: <id:grpid> dict
    """
    #map = {}
    for items in recs:
        
        id = int(float(items[0]))
        if id in map:
            map[id] = map[id] + grpid
        else:
            map[id] = grpid

    return map

def check_labelfile(outfile):
    '''
    '''
    
    #check all the input files
    inputfiles={
        'old_labelfile':'../cut/all.cut',
        'new_labelfile':'sdump.cut',
        'dedup_grpfile':'../dedup/ddump.cut.grp',
        'predict_file':'../dedup/sdump.cut',
        'prob_Afile':'../probe/output-out.A',
        'prob_Bfile':'../probe/output-out.B',
        'prob_Cfile':'../probe/output-out.C'
    }

    records={}
    for fid in inputfiles:
        fname = inputfiles[fid]
        if not os.path.exists(fname):
            logger.info('%s not found, quit', fname)
            return
        else:
            records[fid] = read_file(fname)

    #build a id,label mapping
    newlabel_map = build_id_map(records['new_labelfile'])

    #deal with dedup
    for duprecs in records['dedup_grpfile']:
        label = 'X'
        #find the new label
        #the id is lineid refer to predict_file
        for lineid in duprecs:
            id = records['predict_file'][int(lineid) + 1][1]
            if id in newlabel_map:
                label = newlabel_map[id]
                break
        if label == 'X':
            #fatal error, not found
            logger.info('dedup grp not found in new label file, quit..., recs=%s', duprecs)
            #return

        #set all the ids in the duprecs
        for lineid in duprecs:
            id = records['predict_file'][int(lineid) + 1][1]
            newlabel_map[id] = label

    #now, newlabel_map is full version before dedup
    #get predict label
    predlabel_map = build_id_map(records['predict_file'])

    #get old label
    oldlabel_map = build_id_map(records['old_labelfile'])

    #get the group id
    grpid_map = {}
    grpid_map = build_grp_map(grpid_map, records['prob_Afile'],'A')
    grpid_map = build_grp_map(grpid_map, records['prob_Bfile'],'B')
    grpid_map = build_grp_map(grpid_map, records['prob_Cfile'],'C')

    outf = open(outfile, 'w')
    #logger.info('rec:219 ->', grpid_map['219'])
    #for id in grpid_map:
    #    outf.write('%s %s\n'%(id, grpid_map[id]))

    #output result
    for id in newlabel_map:
        iid = int(id)
        outf.write('%s %s %s %s %s\n'%(id, 
                    newlabel_map[id], predlabel_map[id],
                    oldlabel_map[id], 
                    grpid_map[iid] if iid in grpid_map else 'X'))


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
    parser.add_option("-o", dest="outfile")
    opt, args = parser.parse_args()

    if opt.outfile is None:
        logger.error(globals()['__doc__'] % locals())
        sys.exit(1)

    check_labelfile( opt.outfile)
