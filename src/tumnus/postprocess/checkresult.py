#coding=utf-8
#!/usr/bin/python

"""
Create a html view for prediction result files.
1. Tool to help do feature engineering.
2. Highlight the features used in model. 
   If .coef file given, the neg/pos will be highlight as blue/red.
   If .color file given, the features will be highlight by color.

This tool replace the old res2html.

"""

import sys,os
import csv
import logging
from optparse import OptionParser
#from jieba.norm import norm_cut, norm_seg

#
# buildfeature.py
#
CUTSEP='/'  
FT_MARKER='#'
FT_SPACE='_'

def read_prob(resfile):
    """
    input:
        .prob
        id y predy prob1 .....
    return:
        resData ;   all
        yy      ;   y, y_hat
        recids  ;   id
    """
    if not os.path.exists(resfile):
        logger.info('probfile %s not exist', resfile)
        return [],[],[]

    f = open(resfile,'r')
    resData = []
    yy = []
    recids = []
    for l in f:
        items = l.strip().split()
        yy.append('%s%s'%(items[1],items[2]))
        recids.append(int(items[0]))
        resData.append(l.strip())
    logger.info('read prob file,  reccnt = %d'%len(resData))
    return resData, yy, recids


def read_res(resfile):
    """
    input:
        .res
        <y, predy, id, content of trainset>
    return:
        resdata: records list <id, content>
        resids: [id]
        yyhat : [ypredy]
        #resmap: {id: y, predy}
    """
    f = open(resfile,'r')
    resData = []
    yy = []
    #resmap = {}
    resids = []
    for l in f:
        pos1 = l.find(' ')
        pos2 = l.find(' ', pos1+1)
        pos3 = l.find(' ', pos2+1)
        items = l[:pos3].split()

        id = int(float(items[2]))
        #resmap[id] = (items[0], items[1])
        yy.append('%s%s'%(items[0],items[1]))
        resids.append(id)
        resData.append(l[pos2+1:].strip())

    logger.info('read res file, reccnt = %d', len(resData))
    return resData, yy, resids

def read_cut(resfile):
    """
    input:
        .cut
        <label, id, content of trainset>
    return:
        datamap: {id: content}
    """
    if (resfile == ''): 
        return {}
    if (not os.path.exists(resfile)):
        logger.info('cutfile %s not exist', resfile)
        return {}

    inf = open(resfile,'r')
    datamap = {}
    for line in inf:
        if line[0] == ' ':
            pos0 = line.find(' ')+1
        else:
            pos0 = 0
        pos1 = line.find(' ',pos0)+1
        pos2 = line.find(' ',pos1)+1

        if pos2 > 0:
            label = int(float(line[pos0:pos1-1]))
            id = int(float(line[pos1:pos2-1]))
            content = line[pos2:-1]

            datamap[id] = content

    logger.info('read_cut return reccnt = %d'%len(datamap))
    return datamap 

def read_datfile(datfile):
    """
    input:
        .dat
        id, target, class, timestamp
    return:
        datmap:{id: target, class, etc}
    """
    datmap = {}
    if datfile == "":
        return None
    with open(datfile, 'r') as inf:
        for line in inf:
            items = line.strip().split()
            datmap[int(float(items[0]))] = (items[1:])

    logger.info('read dat file return reccnt = %d'%len(datmap))
    return datmap

def read_colormap(colorfile):
    """
    input:
        color file:
            <tag color>
            brand #FF0000
    return:
        colormap: {tag: color}
    """
    if not os.path.exists(colorfile):
        logger.info('colorfile %s not exist', colorfile)
        return {}

    colormap = {}
    with open(colorfile) as cf:
        for line in cf:
            items = line.strip().split()
            colormap[items[0]] = items[1]
                
    logger.info('read color file return reccnt = %d'%len(colormap))
    return colormap

def read_vocab(coeffile):
    """
    input:
        vocab file:
            车存
    return:
        features: {word: weight}
    """
    if not os.path.exists(coeffile):
        logger.info('coeffile %s not exist', coeffile)
        return {}

    features = {}
    with open(coeffile) as cf:
        for line in cf:
            items = line.strip().replace(' ', FT_SPACE)
            features[items] = 1
    logger.info('read vocab file return reccnt = %d'%len(features))
    return features


def read_coef(coeffile):
    """
    input:
        .coef file:
        neg\t车存\t-9.74207363139
    return:
        features: {word: weight}
    """
    if not os.path.exists(coeffile):
        logger.info('coeffile %s not exist', coeffile)
        return {}

    features = {}
    with open(coeffile) as cf:
        for line in cf:
            items = line.strip().split('\t')
            #check if it has pos tag
            pos =items[1].find(CUTSEP)
            if pos > 0:
               items[1] = items[1][:pos] 
            weight = float(items[2])
            #use only neg features
            if weight != 0:
                features[items[1]] = weight
                
    logger.info('read coef file return reccnt = %d'%len(features))
    return features

def highlight_old(text, features):
    """
    input:
        text:  space separated text
        features:  {word:weight}
    output:
        highlight <>word<> with feature match
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


def get_color(weight, mode = 0):
    """
    input: 
        weight = [-1,1]
    return:
        weight > 0 : red
        weight < 0 : blue
    """
    if mode == 1:
        #scale to [20-255]
        weight = weight * (255-20) + 20

        if weight > 0:
            return '#%0.2X0000'%weight
        else:
            return '#0000%0.2X'%weight
    else:
        colors=['#FF0000','#FF8000','#0080FF','#0000FF']
        idx = int((-1 * weight + 1)/0.5)
        idx = 3 if idx >=3 else idx
        return colors[idx]


def highlight(text, features, colormap, tagmode ):
    """
    input:
        text:  space separated text
        features:  {word: weight}, weight is normalized to [0-1]
        colormap:  {word: color}
        tagmode : 
    output:
        highlight <>word<> with feature match
    """
    words = text.split()
    output = []
    debugcnt = 0
    for w in words:
        # get word, tag info
        if tagmode:
            winfo = w.split(CUTSEP)
            word = winfo[0]
            tag = winfo[1]
        else:
            word = w
            tag = 'XXX'
    
        #if debugcnt < 5:    
        #    tagx = tag.split(FT_MARKER)[0]
        #    colorx = colormap[tagx] if tagx in colormap else ''
        #
        #    logger.debug('%s %s -> %s %s', word, tag, tagx, colorx)
        #    debugcnt += 1

        if word in features:
            # default color
            #color = '#FF0000'
            color = get_color(features[word])

            output.append('<span style="color:' + color + '">' + word + '</span>')
        else:
            tagx = tag.split(FT_MARKER)[0]
            if tagx in colormap:
                #split featuretag from tag
                color = colormap[tagx]
                output.append('<span style="color:' + color + '">' + word + '</span>')
            else:
                output.append(word)

    return " ".join(output)


def items2html(fname, opts):
    """
    """
    items_fn = fname + '.res'
    coeffile = fname + '.coef'
    probfile = fname + '.prob'

    logger.info('Start items2html, resfile= %s, filter = %s, datfile=%s, cutfile=%s, colorfile=%s, vocabfile=%s,useprob=%s, usecoef=%s', 
            fname, opts.filter, opts.datfile, opts.cutfile, 
            opts.colorfile, opts.vocabfile, opts.useprob, opts.usecoef)

    html_fn = os.path.splitext(os.path.basename(items_fn))[0] + '.%s.html'%opts.filter

    #1. load files
    items,yyhat, recids = read_res(items_fn)
    datmap = read_datfile(opts.datfile)
    colormap = {}
    features = {}
    cutmap = {}
    probs = []

    if opts.colorfile:
        colormap = read_colormap(opts.colorfile)
    if opts.cutfile:
        cutmap = read_cut(opts.cutfile)
    if opts.usecoef:
        features = read_coef(coeffile)
    else:
        if opts.vocabfile:
            features = read_vocab(opts.vocabfile)
    if opts.useprob:
        probs,yyhat,recids = read_prob(probfile)

    logger.info('load total %d items', len(items))

    #2. check the feature mode, using word or featuretag?
    #tagmode = True if text.find(CUTSEP) >= 0 else False

    #3. normalize the weights
    pmax = nmax = 0
    for w in features:
        if features[w] > pmax:
            pmax = features[w]
        if features[w] < nmax:
            nmax = features[w]

    if pmax != 0 and nmax != 0:
        for w in features:
            if features[w] > 0:
                features[w] = features[w] / pmax
            elif features[w] < 0:
                features[w] = -1. * features[w] / nmax
    logger.info('tagmode = %s, pmax = %s, nmax = %s', opts.tagmode, pmax, nmax)

    logger.debug('colormap = %s', colormap)

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
        if opts.filter != 'all':
            if yyhat[rowid] != opts.filter: 
                continue

        row = items[rowid]
        prob = probs[rowid] if probs else '' 
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
                if cutmap:
                    outstr = highlight(str(cutmap[recids[rowid]]), features, colormap, opts.tagmode) 
                else:
                    outstr = highlight(str(row), features, colormap, opts.tagmode) 
                htmlfile.write('<td width="' + colwidth[rid] + '%">' +outstr + '</td>')
            

        htmlfile.write('</tr>')
        rownum += 1
    # write </table> tag
    htmlfile.write('</table>')
    # print results to shell
    logger.info("Created " + str(rownum) + " row table.")

if __name__ == "__main__":
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)

    op = OptionParser('Usage: checkres.py [options] resfile')
    op.add_option("--filter",
                  action="store", type=str, default="all",
                  help="set the filter pattern <true_y, pred_y>,'all' by default, '01' is most used.")
    op.add_option("--datfile",
                  action="store", type=str, default="",
                  help="set the dat file name to get properties of reacords, such as target name.")
    op.add_option("--vocabfile",
                  action="store", type=str, default="",
                  help="set the source .vocab file contain the features.")
    op.add_option("--cutfile",
                  action="store", type=str, default="",
                  help="set the source .cut file contain the original contents.")
    op.add_option("--colorfile",
                  action="store", type=str, default="",
                  help="set the color map file name to coloring the features.")
    op.add_option("--useprob",
                  action="store_true",
                  help="set to use the .prob file to sort the result by probability.")
    op.add_option("--usecoef",
                  action="store_true",
                  help="set to use the .coef file to weight the color of features.")
    op.add_option("--tagmode",
                  action="store_true",
                  help="set to use tag as features instead using words.")
    
    (opts, args) = op.parse_args()

    if len(sys.argv) < 2:
        print(globals()['__doc__'] % locals())
        
        op.print_help()
        sys.exit(1)

    # 
    logger.info("running %s" % ' '.join(sys.argv))
    infname = args[0]
    pos = infname.rfind('.')
    if pos > 0:
        infname = infname[:pos]
    items2html(infname, opts)
