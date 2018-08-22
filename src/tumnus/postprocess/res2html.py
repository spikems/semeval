#coding=utf-8
#!/usr/bin/python

"""
Create a html view for prediction result files.
1. Tool to help do feature engineering.
2. Highlight the features used in model. 
   If .coef file given, the neg/pos will be highlight as blue/red.
   If .color file given, the features will be highlight by color.

    Useage:
        res2html --filter <filter> --datfile <datfile> <resfiles name>
            filter: 'all' by default, '01' is most used 
            datfile: .dat file <id, 监控对象 分类 发表日期>
            resfiles: include .res, .coef, .prob

"""

import sys,os
import csv
import logging
from optparse import OptionParser
#from jieba.norm import norm_cut, norm_seg

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

def read_prob(resfile):
    """
        .prob
        id y predy prob1 .....
    """
    f = open(resfile,'r')
    resData = []
    yy = []
    recids = []
    for l in f:
        items = l.strip().split()
        yy.append('%s%s'%(items[1],items[2]))
        recids.append(int(items[0]))
        resData.append(l.strip())
    print 'read_res readin reccnt = ', len(resData)
    return resData, yy, recids

def read_res(resfile):
    """
    Read in res file and return a list of records

    """
    f = open(resfile,'r')
    resData = []
    for l in f:
        pos1 = l.find(' ')
        pos2 = l.find(' ', pos1+1)
        resData.append(l[pos2+1:].strip())

    print 'read_res readin reccnt = ', len(resData)
    return resData

def loadfeatures(coeffile):
    """
    coef file:
    neg\t车存\t-9.74207363139
    """
    features = {}
    with open(coeffile) as cf:
        for line in cf:
            items = line.strip().split('\t')
            #check if it has pos tag
            pos =items[1].find('_')
            if pos > 0:
               items[1] = items[1][:pos] 
            weight = float(items[2])
            #use only neg features
            if weight != 0:
                features[items[1]] = weight
    return features

def highlight(text, features):
    """
    output highlight <>word<> with feature match
    """

    # words = [x.encode('utf-8') for x in norm_cut(text)]
    words = text.split()
    output = []
    #pick colors, red1, red2/blue1, blue2
    colors=['#FF0000','#FF8000','#0000FF','#0080FF']
    flip = [0,0]
    for w in words:
        if w in features.keys():
            #TODO: get weight to make a color

            # just add a color
            if features[w] > 0:
                #red
                output.append('<span style="color:' + colors[flip[0]%2] + '">' + w + '</span>')
                flip[0] += 1
            else:
                output.append('<span style="color:' + colors[2 + flip[1]%2] + '">' + w + '</span>')
                flip[1] += 1
        else:
            output.append(w)

    return " ".join(output)

def read_datfile(datfile):
    datmap = {}
    if datfile == "":
        return None
    with open(datfile, 'r') as inf:
        for line in inf:
            items = line.strip().split()
            datmap[int(float(items[0]))] = (items[1:])
    return datmap


#def items2html(items_fn, coeffile):
def items2html(fname, filter, datfile):
    """
        .res
        .coef
        .prob
    """
    items_fn = fname + '.res'
    coeffile = fname + '.coef'
    probfile = fname + '.prob'


    logger.info('Start items2html, items_fn= %s, filter = %s', items_fn, coeffile)

    html_fn = os.path.splitext(os.path.basename(items_fn))[0] + '.%s.html'%filter

    probs,yyhat,recids = read_prob(probfile)
    items = read_res(items_fn)
    datmap = read_datfile(datfile)
    features = loadfeatures(coeffile)
    if not features:
        logger.info('load empty feature file, quit', coeffile)

    # sort the data by f1 score
    #items = sorted(items[1:], key = lambda x: float(x[3])*float(x[4])/(float(x[3]) + float(x[4]) + 1e-12))

    htmlfile = open(html_fn,"w")# Create the HTML file for output
    # resultData = []

    #colidx = {'id':0,'stype':9, 'title':3, 'text':10}
    colidx = [0,9,3,10]
    colname = ['id','stype', 'prob', 'text']
    # colwidth = ["6", "2", "30", "30", "30", "2"]
    # colwidth = ["60", "200", "200", "20", "20", "100","20","100","20","20"]
    #colwidth = ["6%", "6%", "20%", "68%"]
    colwidth = ["6%", "6%", "6%", "82%"]
    # write <table> tag
    #       table {border-collapse:collapse; table-layout:fixed; width:1800px;}
    htmlfile.write('''<html><head><meta charset="utf-8">
            <style>
            table {border-collapse:collapse; table-layout:fixed; }
            table td {border:solid 1px #fab;word-wrap:break-word;vertical-align:top}
            </style></head><table width="100%" >''')
    #width="100%"

    htmlfile.write('<tr>')# write <tr> tag
    for index in range(len(colname)):
        htmlfile.write('<th width="' + colwidth[index] + '%">' + colname[index] + '</th>')

    htmlfile.write('</tr>')
    rownum = 0

    # generate table contents
    i=0
    #for row in items: # Read a single row from the CSV file
    for rowid in xrange(len(items)): # Read a single row from the CSV file
        if filter != 'all':
            if yyhat[rowid] != filter: 
                continue

        row = items[rowid]
        prob = probs[rowid]
        # print row[3],row[4]
        htmlfile.write('<tr>')
        for rid in range(len(colidx)):
            #if rid == 0:
            #    #url
            #    htmlfile.write('<td width="' + colwidth[rid] + '%"><a href="' + str(row[rid]) + '", target="_blank">' + str(row[rid]) + '</a></td>')

            #else:
            # if rid == 0 or rid == 1:
            #     htmlfile.write('<td width="' + colwidth[rid] + '%">' + str(row[colidx[rid]]) + '</td>')
            # else:
            #     htmlfile.write('<td width="' + colwidth[rid] + '%">' + highlight(str(row[colidx[rid]]), features) + '</td>')
            if rid < 2:
                if datmap is not None:
                    htmlfile.write('<td width="' + colwidth[rid] + '%">' + datmap[recids[rowid]][rid] + '</td>')
                else:
                    htmlfile.write('<td width="' + colwidth[rid] + '%">' + ' ' + '</td>')
            elif rid ==2:
                 htmlfile.write('<td width="' + colwidth[rid] + '%">' +prob + '</td>')
 
            else:
                 htmlfile.write('<td width="' + colwidth[rid] + '%">' + highlight(str(row), features) + '</td>')

        htmlfile.write('</tr>')
        rownum += 1
    # write </table> tag
    htmlfile.write('</table>')
    # print results to shell
    print "Created " + str(rownum) + " row table."

if __name__ == "__main__":
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
    op.add_option("--filter",
                  action="store", type=str, default="all",
                  help="set the filter pattern <true_y, pred_y>.")
    op.add_option("--datfile",
                  action="store", type=str, default="",
                  help="set the dat file name.")
    (opts, args) = op.parse_args()

    infname = args[0]
    items2html(infname, opts.filter, opts.datfile)

