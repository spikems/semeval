#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
dump dataset from original xlsx files by selected <ids,label> list

input files:
    idmap   : newid, fileid, recid
    filemap : id sxxxxx.cut
    car xlsx files: xxxxx.xlsx
    select.id:  newid, label

output format:
    .xlsx
    trainset deliver to the label process with uniq newid

Usage:
    combinexlsx.py --uselabel --useoldid <outfile>
        --uselabel    ; use the label in xlsx file by default, set to use the label in select.id file, 
        --useoldid    ; use the id in xlsx file if set, use id in select file by default
"""


import os, sys,re
import xlsxwriter as xlwt
#import xlwt
import xlrd
import logging
from optparse import OptionParser

#standard format
#IDMAP = {u'序号':0,u'监控对象':1,u'分类':2, u'主题':3,u'链接':4,u'发表日期':5,u'来源':6,u'点击':7,u'回复':8, u'摘要':9,u'作者':10,u'评级':11}
IDMAP = {0:u'序号',1:u'监控对象',2:u'分类', 3:u'主题',4:u'链接',5:u'发表日期',6:u'来源',7:u'点击',8:u'回复', 9:u'摘要',10:u'作者',11:u'评级'}
LABELS={0:u'中立',1:u'正面',-1:u'负面'}
LABELINDEX=11


def make_xlsx(output, uselabel, useoldid):
    #start dump
    logger.info('Start dump, using label from %s', 'select.id' if uselabel else 'source xlsx')


    #load idmapping files
    idf = open('idmap.txt','r')
    idmap = {}
    for line in idf:
        items = line.strip().split()
        idmap[int(items[0])] = (int(items[1]), int(items[2]))
    logger.info('read idmap.txt, reccnt=%d', len(idmap))

    #load filemapping
    fnf = open('filemap.txt','r')
    filemap = {}
    for line in fnf:
        items = line.strip().split()
        #DEPRECATED: should be sxxxxx.cut
        #m = re.search('s(.*)\..*', items[1])
        #if m:
        #    filemap[int(items[0])] = m.group(1)
        #no limit on the file name 
        #remove .ext
        itemname = items[1][:items[1].rfind('.')]
        filemap[int(items[0])] = itemname
        

    logger.info('read filemap.txt, reccnt=%d', len(filemap))

    #
    self = open('select.id','r')
    selmap = {}
    selids = []
    for line in self:
        items = line.strip().split()
        # id, label_id or prob
        selmap[int(float(items[0]))] = int(float(items[1]))
        selids.append(int(float(items[0])))
    logger.info('read select.id, reccnt=%d', len(selmap))

    #file
    sheet = []
    recmap = []
    colmap = []
    for db in filemap:
        logger.info('open xlsx files:%s...', filemap[db])
        workbook0 = xlrd.open_workbook(filemap[db] + '.xlsx')
        sheet0 = workbook0.sheet_by_index(0)

        #build col id map
        row = sheet0.row(0)  # 1st row
        colmap0 = {}
        for idx, cell_obj in enumerate(row):
            #save the idx mapping
            colmap0[cell_obj.value] = idx
    
        # build recid->rowid mapping
        recmap0 = {}
        for row_idx in range(1, sheet0.nrows):    # Iterate through rows
            recid = sheet0.cell_value(row_idx, 0)
            recmap0[recid] = row_idx
        logger.info('load %s.xlsx, reccnt=%d', filemap[db], len(recmap0))
        
        #save it
        sheet.append(sheet0)
        recmap.append(recmap0)
        colmap.append(colmap0)
 
    #output
    outbook = xlwt.Workbook(output)
    sheet2 = outbook.add_worksheet('trainset')
    #standard column names and order
    data = [IDMAP[col] for col in range(len(IDMAP))]

    #data = [sheet[0].cell_value(0, col) for col in range(sheet[0].ncols)]
    for index, value in enumerate(data):
        sheet2.write(0, index, value)

    #
    rowcnt = 1
    for selid in selids:
        fid, recid = idmap[selid]
        rowid = recmap[fid][recid]

        #data = [sheet[fid].cell_value(rowid, col) for col in range(sheet[fid].ncols)]
        type = [sheet[fid].cell_type(rowid, colmap[fid][IDMAP[col]]) for col in range(len(IDMAP))]
        data = [sheet[fid].cell_value(rowid, colmap[fid][IDMAP[col]]) for col in range(len(IDMAP))]

        if not useoldid:
            #change recid
            data[0] = selid

        if uselabel:
            data[LABELINDEX] = LABELS[selmap[selid]]

        for index, value in enumerate(data):
            #debug
            #if rowcnt == 1:
            #    logger.info('type of col: %s', type)

            #override the urls writing, force to use write_string
            #if type[index] == xlrd.XL_CELL_DATE:
            #    as_datetime = xlrd.xldate.xldate_as_datetime(value,workbook0.datemode)
            #    sheet2.write_datetime(rowcnt, index, as_datetime)
            #elif type[index] == xlrd.XL_CELL_NUMBER:
            #    sheet2.write_number(rowcnt, index, value)
            #elif type[index] == xlrd.XL_CELL_BLANK:
            #    sheet2.write_blank(rowcnt, index, value)
            #elif type[index] == xlrd.XL_CELL_TEXT:
            #    sheet2.write_string(rowcnt, index, value)
            #else:
            #    sheet2.write(rowcnt, index, value)
            if type[index] == xlrd.XL_CELL_TEXT:
                sheet2.write_string(rowcnt, index, value)
            else:
                sheet2.write(rowcnt, index, value)


        rowcnt += 1

        #debug for only one record
        #break

    logger.info('dump %d records', rowcnt)

    outbook.close()
    

if __name__=="__main__":
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

    if len(sys.argv) < 2:
        logger.error(globals()['__doc__'] % locals())
        sys.exit(1)

    op = OptionParser()
    op.add_option("--uselabel",
                  action="store_true", 
                  help="use the label in select file.")
    op.add_option("--useoldid",
                  action="store_true", 
                  help="use the id in xlsx file.")
    
    (opts, args) = op.parse_args()

    make_xlsx(args[0], opts.uselabel, opts.useoldid)
