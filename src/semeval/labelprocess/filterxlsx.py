#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import xlwt
import xlrd
import logging



def make_xlsx(input, output):
    self = open('final.id','r')
    selmap = {}
    selids = []
    for line in self:
        items = line.strip().split()
        selmap[int(float(items[0]))] = 1
        selids.append(int(float(items[0])))
    logger.info('read final.id, reccnt=%d', len(selmap))

    #file 0
    logger.info('open car xlsx files...')
    workbook0 = xlrd.open_workbook(input)
    sheet0 = workbook0.sheet_by_index(0)
 
    # build recid->rowid mapping
    recmap0 = {}
    for row_idx in range(1, sheet0.nrows):    # Iterate through rows
        recid = sheet0.cell_value(row_idx, 0)
        recmap0[recid] = row_idx
    logger.info('load %s, reccnt=%d', input , len(recmap0))
 
    #output
    outbook = xlwt.Workbook()
    sheet2 = outbook.add_sheet('trainset')
    data = [sheet0.cell_value(0, col) for col in range(sheet0.ncols)]
    for index, value in enumerate(data):
        sheet2.write(0, index, value)

    #
    rowcnt = 1
    for selid in selids:
        rowid = recmap0[selid]

        data = [sheet0.cell_value(rowid, col) for col in range(sheet0.ncols)]
        #change recid
        for index, value in enumerate(data):
            sheet2.write(rowcnt, index, value)

        rowcnt += 1

        #debug for only one record
        #break

    logger.info('dump %d records', rowcnt)

    #book.save(output)
    outbook.save(output)
    

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

    make_xlsx(sys.argv[1], sys.argv[2])
