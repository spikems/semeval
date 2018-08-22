#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Dump columns from xlsx file and save as txt file

input:
    序号    监控对象    分类    主题    链接    发表日期    来源    点击    回复    评级    摘要    作者
    中立,正面,负面

output: 
    .txt
    sorted by timestamp
    senti, id , text
    
    .dat
    id 监控对象 分类 发表日期

Usage: xlsx-yy.py <input> <output>

"""
from __future__ import print_function
from os.path import join, dirname, abspath
import xlrd
import sys,os
import numpy as np

import logging
logger = logging.getLogger(__name__)

def checksheet(xl_workbook, sheet_id):
    """
    """

    #idmap = {u'序号':0,u'监控对象':1,u'分类':2, u'主题':3,u'发表日期':5,u'评级':9,u'摘要':10}
    idmap = {u'序号':-1,u'监控对象':-1,u'分类':-1, u'主题':-1,u'发表日期':-1,u'评级':-1,u'摘要':-1}
    xl_sheet = xl_workbook.sheet_by_index(sheet_id)
    # Pull the first row by index
    #  (rows/columns are also zero-indexed)
    #
    row = xl_sheet.row(0)  # 1st row
    
    # Print 1st row values and types
    #
    from xlrd.sheet import ctype_text   
    
    print('(Column #) type:value')
    for idx, cell_obj in enumerate(row):
        cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
        print('(%s) %s %s' % (idx, cell_type_str, cell_obj.value))
        
        #save the idx mapping
        if cell_obj.value in idmap:
            idmap[cell_obj.value] = idx
    
    logger.info('idmapping: %s', idmap)
    return idmap
 
def trim(line):
    """
        remove all \n\r\t in line
    """
    return line.replace('\n','').replace('\r','').replace('\t','')


def dumpsheetEx(xl_workbook, sheet_id, idmap, outfname):

    print('dumping sheet %s'%xl_workbook.sheet_names()[sheet_id])
    xl_sheet = xl_workbook.sheet_by_index(sheet_id)
    if xl_sheet.nrows == 0:
        return None

    txtfs = {}
    # all values, iterating through rows and columns
    #

    #idmap = {u'序号':0,u'监控对象':1,u'分类':2, u'主题':3,u'发表日期':5,u'评级':9,u'摘要':10}

    typename={u'中立':0,u'正面':1,u'负面':-1,u'中性':0}
    nullcnt = 0
    sheet = []
    num_cols = xl_sheet.ncols   # Number of columns
    for row_idx in range(0, xl_sheet.nrows):    # Iterate through rows
        arow = []

       # dump type, hidden, title, abstract
        cell_obj = xl_sheet.cell_value(row_idx, idmap[u'评级']).strip()  # type
        #cell_obj = xl_sheet.cell_value(row_idx, 9)  # type
        if cell_obj not in typename:
            print(cell_obj, type(cell_obj))
            nullcnt += 1
            continue
        arow.append(typename[cell_obj])

        #cell_obj = xl_sheet.cell_value(row_idx, 16)  # hidden
        arow.append(0)

        cell_obj = xl_sheet.cell_value(row_idx, idmap[u'主题'])  # title
        arow.append(cell_obj)
        cell_obj = xl_sheet.cell_value(row_idx,  idmap[u'摘要'])  # abstract
        arow.append(cell_obj)
        # add timestamp
        cell_obj = xl_sheet.cell_value(row_idx,  idmap[u'发表日期'])  # post timestamp
        arow.append(cell_obj)

        cell_obj = xl_sheet.cell_value(row_idx,  idmap[u'监控对象'])  # object
        arow.append(cell_obj)
        if not cell_obj in txtfs:
            #txtfs[cell_obj] = open('%s.txt'%cell_obj,'w')
            txtfs[cell_obj] = cell_obj
        #add id    
        cell_obj = xl_sheet.cell_value(row_idx,  idmap[u'序号'])  # id
        arow.append(cell_obj)
    
        cell_obj = xl_sheet.cell_value(row_idx,  idmap[u'分类'])  # id
        arow.append(cell_obj)
 
 
        #check the record
        if arow[0] not in (0,1.,-1.) or arow[1] not in (0,1.,-1.) :
            nullcnt += 1
            continue

        sheet.append(arow)

    outf = open(outfname + '.txt','w')
    datf = open(outfname + '.dat', 'w')
    # sort the data by timestamp
    sheet = sorted(sheet, key = lambda arow: (arow[5], arow[4]))
    for arow in sheet:
        try:
            #old format, start from type
            #txtfs[arow[5]].write('%s %s %s %s\n'%(arow[0], arow[1], arow[2].encode('utf-8'), arow[3].encode('utf-8')))
            #new format, start from id, type
            #txtfs[arow[5]].write('%s %s %s %s %s\n'%(arow[6],arow[0], arow[1], arow[2].encode('utf-8'), arow[3].encode('utf-8')))
            #output by id
            outf.write('%s %s %s %s\n'%(arow[0], arow[6], trim(arow[2].encode('utf-8')), trim(arow[3].encode('utf-8'))))

            # database
            datf.write('%s %s %s %s\n'%(arow[6], arow[5].encode('utf-8'), arow[7].encode('utf-8'), arow[4]))
        except:
            nullcnt += 1
            pass
 
    outf.close()
    datf.close()
    #for i in txtfs:
        #txtfs[i].close()
    logger.info('objs:%s', txtfs.keys())
        
    print('nullcnt = %d'%nullcnt)
    #write <type, hidden> to file
    array = np.array([[x[0],x[1], x[4]] for x in sheet])
    #np.savetxt(xl_workbook.sheet_names()[sheet_id], array, fmt='%d')
    return array

def calcAcc(hidArray):
    """
        type, hidden

        acc = (hidden < 0)/(hidden <= 0)
        noise = (hidden >0) / total

    """
    if hidArray is None:
        return
    total = hidArray.shape[0]

    #print('err:%s'%(hidArray[:,1] < 0))
    #print('correct:%s'%(hidArray[:,1] == 0))
    err = np.count_nonzero(np.array(hidArray[:,1] < 0))
    correct = np.count_nonzero(np.array(hidArray[:,1] == 0))

    print('total=%d, correct=%d, err=%d, cleanAcc=%.02f, acc=%.02f'%(total, correct, err, (err + correct)*1.0/total, correct*1.0/(err + correct)))

    posCnt = np.count_nonzero(np.array(hidArray[:,0] > 0))
    negCnt = np.count_nonzero(np.array(hidArray[:,0] < 0))
    midCnt = np.count_nonzero(np.array(hidArray[:,0] == 0))

    print('posCnt = %d, midCnt=%d, negCnt=%d'%(posCnt, midCnt, negCnt))
    print('posCnt = %.02f, midCnt=%.02f, negCnt=%.02f'%(posCnt*1./total, midCnt*1./total, negCnt*1./total))

    #get all valid records
    hidArray = hidArray[hidArray[:, 1] <=0]
    posCnt = np.count_nonzero(np.array(hidArray[:,0] > 0))
    posArray = hidArray[hidArray[:, 0] > 0]
    posErrCnt = np.count_nonzero(np.array(posArray[:,1] < 0))
    negCnt = np.count_nonzero(np.array(hidArray[:,0] < 0))
    negArray = hidArray[hidArray[:, 0] < 0]
    negErrCnt = np.count_nonzero(np.array(negArray[:,1] < 0))
    midCnt = np.count_nonzero(np.array(hidArray[:,0] == 0))
    midArray = hidArray[hidArray[:, 0] == 0]
    midErrCnt = np.count_nonzero(np.array(midArray[:,1] < 0))
 
    print('posCnt = %d, midCnt=%d, negCnt=%d'%(posCnt, midCnt, negCnt))
    print('posCnt = %.02f, midCnt=%.02f, negCnt=%.02f'%(posCnt*1./total, midCnt*1./total, negCnt*1./total))
    if posCnt > 0 and midCnt >-0 and negCnt > 0:
        print('pos acc=%.02f, mid acc=%.02f, neg acc=%.02f'%((posCnt-posErrCnt)*1./posCnt, 
                (midCnt-midErrCnt)*1./midCnt, 
                (negCnt-negErrCnt)*1./negCnt))


def loadbook(fname):
    logger.info('loading %s....', fname)
    xl_workbook = xlrd.open_workbook(fname)
    logger.info('load done!')
    return xl_workbook

if __name__=='__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

    if len(sys.argv) < 3:
        logger.error(globals()['__doc__'] % locals())
        sys.exit(1)

 
    fname = sys.argv[1]
    oname = sys.argv[2]

    # Open the workbook
    xl_workbook = loadbook(fname)
    # List sheet names, and pull a sheet by name
    #
    sheet_names = xl_workbook.sheet_names()
    print('Sheet Names', sheet_names)
   
    #for id in range(len(sheet_names)):
    id = 0
    idmap = checksheet(xl_workbook, id)
    array = dumpsheetEx(xl_workbook, id, idmap, oname)
    calcAcc(array)
