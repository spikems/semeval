#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Extract Features from text for semeval tasks
Functions:
1). extract features tags by features dictionary
    1. Seprate to sentence, 
    2. cws cut with pos tag, 
    3. tagging and filtering by feature dictionary
    4. recongnize target from the brand names
    5. output word/featuretag as standard output
2). make userdict of jieba
    --builduserdict
3). select features and make .cut file
    --selectfeature
    1. SEL_FTONLY output featuretag only
    2. SEL_FTCOMBINE output <target, aspect, opinion, syntax_tag> tuples 

feature dictionaries:
    aspect.dict
    brand_names.dict
    diffcomp.dict
    opinion.dict
    syntax.dict

"""
import string
import sys,time
import os, os.path
import logging
import jieba
import re
from jieba.norm import norm_cut, norm_seg
from optparse import OptionParser

#
# output format
#
# cutsep to output the feature as "word/tag"
CUTSEP='/'  
FT_MARKER='#'
FT_SPACE='_'
#
# feature dict format
# 
FEATURETAG=0
POSTAG=1
TARGET=0

# select feature commands
SEL_FTONLY = '0'      #only feature tags
SEL_FTCOMBINE = '1'   #combine <target, aspect, opinion> pairs

#
# feature tags
#
FT_TARGET = 'target'
FT_SENT = 'br'
FT_BRAND = 'brand'
FT_ASPECT= 'aspect'
FT_OPINION = 'opinion'
FT_COMP = 'comp'
FT_COMPR= 'comp_r'
FT_WISH = 'wish'
FT_IF =  'if'
FT_NEG =   'neg'
FT_BUT =   'but'
FT_ALTHOUGH =  'although'
FT_AND =   'and'
FT_SO =   'so'
 

FEATURETAG_LIST=[
    'brand', 
    'aspect', 
    'opinion',
    'comp', 'comp_r', 
    'wish', 'if',
    'neg',
    'but', 'although', 'and', 'so'
    ]

def gettag(tag):
    return '%s#'%tag
def getword(tag, word):
    return '%s#%s'%(tag,word.replace(' ','_'))

#
# helper functions read files 
#
def read_datfile(datfile):
    """
        .dat  is the dump from dataset
        id, target, class, timestamp

        return: {(int)id: (target, class,...)}
    """
    datmap = {}
    if datfile == "":
        return None
    with open(datfile, 'r') as inf:
        for line in inf:
            items = line.strip().split()
            datmap[int(float(items[0]))] = items[1:]
    logger.debug('datmap = %s', datmap[datmap.keys()[0]])
    return datmap

def read_jiebadict(datfile):
    """
        word, freq, postag
        return: {word: (freq,postag)}
    """
    datmap = {}
    with open(datfile, 'r') as inf:
        for line in inf:
            items = line.strip().split()
            datmap[items[0]] = items[1:]
    return datmap


def read_dict(featureDict, wordmap):
    """
        .dict is the feature dictionary file
         tag  postag  word

         return: {word: (tag, postag)}
    """
    #wordmap = {}
    with open(featureDict, 'r') as inf:
        logger.info('load dict %s', featureDict)
        for line in inf:
            items = line.strip().split()
            word = FT_SPACE.join(items[2:])
            if word in wordmap:
                logger.info('duplicate word in feature dictionary: %s',line)
            else:
                wordmap[word] = items[:2]
    return wordmap


def read_featuredicts(dictpath):
    dictfiles=[
        'aspect.dict',
        'brand_names.dict',
        'diffcomp.dict',
        'opinion.dict',
        'syntax.dict',
        ]
    
    wordmap = {}
    for df in dictfiles:
        read_dict(dictpath + '/' + df, wordmap)

    logger.info('load feature dictionary, recs = %d', len(wordmap))
    return wordmap

#============================================================
# main functions
#============================================================
def make_userdict(jieba_dictpath, feature_dictpath, output):
    """
    Add the words in feature dictionary into jieba userdict dynamically
    """
    NR_Preffix=['长','常委','主任','主席','经理','总裁','明星','助理','教师','总监','记者','师','员',
                    '人','主管','官','CEO','CFO','CTO','CIO','COO','会计','导购','代理','演员','礼仪',
                    '导游','医生','大使','司仪']
    NR_Suffix=['先生','小姐','女士']
 
    from mxword.newword.deal_new_words import deal_new_words_for_dict
    
    # load feature dicts
    wordmap = read_featuredicts(feature_dictpath)
    jiebadict = read_jiebadict(jieba_dictpath)

    #filtering by jieba dict
    newwords = []
    for x in wordmap:
        if x not in jiebadict:
            newwords.append((x.decode('utf-8'),1))
            
    logger.info('load feature dictionaries, rec=%d', len(newwords))
    
    #calc new freq
    dnWD = deal_new_words_for_dict(newwords, list(), (jieba_dictpath,''))
    dnWD.deal((NR_Preffix,NR_Suffix))
    
    logger.info('build freq for jieb userdict, rec=%d',len(dnWD.new_words_dic_frequency))

    #write output
    with open(output, 'w') as outf:
        for word in dnWD.new_words_dic_frequency:
            outf.write('%s %s %s\n'%(word, dnWD.new_words_dic_frequency[word], wordmap[word][POSTAG]))

#=========================================================
def extract_feature(content, target, wordmap):
    """
    Extract features defined in the feature dictionaries.
    input:
        line of text

    target: target brand name
    wordmap: feature dictionary format
        word: feature_tag, post_tag

    output:
        features: word/tag seq
    """
    #split into  sentences
    sents = content.split('...')
    #tag 
    result = []
    
    for sent in sents:
        #cut 
        words = norm_seg(sent)
        #words = norm_cut(sent)
        output = ''
        #for word in words:
        for it in words:
            word = it.word.encode('utf-8').lower().replace(' ',FT_SPACE)
            postag = it.flag.encode('utf-8')
            # all convert to lower case
            #logger.debug('%s %s ', word, postag.encode('utf-8'))
            if word in wordmap:
                # check the feature tag
                if wordmap[word][FEATURETAG] == FT_BRAND:
                    # check if the brand is target
                    if (target in word) or (word in target):
                        output = gettag(FT_TARGET)
                    else:
                        output = gettag(FT_BRAND)
                elif (wordmap[word][FEATURETAG] == FT_ASPECT) or \
                     (wordmap[word][FEATURETAG] == FT_OPINION):
                    output = getword(wordmap[word][FEATURETAG], word)
                else:
                    output = gettag(wordmap[word][FEATURETAG])

                #append this feature
                result.append(word + CUTSEP + output)
            else:
                result.append(word + CUTSEP + postag)
                

        if output:
            result.append('...' + CUTSEP + gettag(FT_SENT))

    return result

def extract_test(datfile, feature_dictpath, jieba_userdict):
    if datfile:
        datmap = read_datfile(datfile)

    if jieba_userdict:
        logger.info('jieba load user dictionary: %s', jieba_userdict)
        jieba.load_userdict(jieba_userdict)

    wordmap = read_featuredicts(feature_dictpath)

   
    logger.info('Enter test mode, q to quit')
    line = raw_input()
    while(line != 'q'):
        # format of line
        #add a id 
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

            target = datmap[id][TARGET].lower()
    
            # extract feature from a line
            result = extract_feature(content, target, wordmap)
            result = ' '.join(result)
            print('%d %d %s\n'%(label, id, result))

        line = raw_input()
    logger.info('bye')


def extract_file(input, output, datfile, feature_dictpath, jieba_userdict):
    '''
    Extract from the .txt file
    input format: dump file
        label id  content
        
    '''
    #import jieba
    #from jieba.norm import norm_cut, norm_seg

   
    writer = open(output, 'w')
    reader = open(input, 'rb')
 
    if datfile:
        datmap = read_datfile(datfile)

    if jieba_userdict:
        logger.info('jieba load user dictionary: %s', jieba_userdict)
        jieba.load_userdict(jieba_userdict)

    wordmap = read_featuredicts(feature_dictpath)

    reccnt = 0
    #
    # parse the records
    # label id text
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
            id = int(float(line[pos1:pos2-1]))
            content = line[pos2:-1]

            # get target
            #if id not in datmap:
            #    logger.error('id %d not found in datmap', id)
            #logger.debug('datmap type = %s', type(datmap[id]))
            target = datmap[id][TARGET].lower()
    
            # extract feature from a line
            result = extract_feature(content, target, wordmap)
            result = ' '.join(result)
            writer.write('%d %d %s\n'%(label, id, result))
        reccnt += 1

    #end
    logger.info('done!, rec=%d', reccnt)

    reader.close()
    writer.close()

#=========================================================
def select_feature(inputfile, outputfile, seltype):
    """
    input:
        intputfile  ; .cut file with feature tags
        seltype     ; SEL_FTONLY, SEL_FTCOMBINE
    output:
        outputfile  ; .cut file with selected features
    """
    writer = open(outputfile, 'w')
    reader = open(inputfile, 'rb')
 
    reccnt = 0
    #
    # parse the records
    # label id text
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
            id = int(float(line[pos1:pos2-1]))
            content = line[pos2:-1]

            result = []
            if seltype == SEL_FTONLY:
                #get feature tag only
                items = content.split()
                for _w in items:
                    winfo = _w.split(CUTSEP)
                    word = winfo[0]
                    if word:
                        #tag = winfo[1].split(FT_MARKER)[0]
                        if winfo[1].find(FT_MARKER) > 0:
                            result.append(winfo[1])
            elif seltype == SEL_FTCOMBINE:

                sentences = re.split('。|；|;|？|\?|！|!|，|,', content) 
                for sentence in sentences:
                    sentence = sentence.replace(FT_SENT, FT_SENT + '。')
                    items = sentence.split()
                    pos = 0
                    feats = []
                    ft_pos = {}
                    for _w in items:
                        winfo = _w.split(CUTSEP)
                        word = winfo[0]
                        if word:
                            #tag = winfo[1].split(FT_MARKER)[0]
                            if winfo[1].find(FT_MARKER) > 0:
                                feats.append(winfo[1])
                                flag = winfo[1]

                                if flag[:-1] in (FT_BRAND , FT_TARGET, FT_COMP, FT_COMPR) or  flag.startswith(FT_OPINION):
                                    feat = flag[:-1]

                                    if flag.startswith(FT_OPINION):
                                        feat = FT_OPINION
                                    if not feat in ft_pos:
                                        ft_pos[feat] = []
                                    ft_pos[feat].append(pos)
                                pos += 1
                    #extract combine feature
                    com_feats = extract_combine_feature(feats, ft_pos)
                    feats.extend(com_feats)
                    result.extend(feats)
            else:
                logger.error('seltype %s not found error, quit', seltype)
                return

            result = ' '.join(result)
            writer.write('%d %d %s\n'%(label, id, result))
        reccnt += 1

    #end
    logger.info('done!, rec=%d', reccnt)

    reader.close()
    writer.close()

def extract_combine_feature(feats, ft_pos):

    com_feats = []
    if FT_TARGET in ft_pos and FT_OPINION in ft_pos:
        if FT_COMP in ft_pos or FT_COMPR in ft_pos:
            compind0, c_label = (ft_pos[FT_COMP][0], FT_COMP) if FT_COMP in ft_pos else (ft_pos[FT_COMPR][0], FT_COMPR)
            targetind0 = ft_pos[FT_TARGET][0]
            com_feat = '%s_%s' % (c_label, FT_TARGET) if compind0 < targetind0 else '%s_%s' % (FT_TARGET, c_label)
            for pos in ft_pos[FT_OPINION]:
                if pos < compind0:
                    continue
                opinion = feats[pos]
                com_feat0 = '%s_%s' % (com_feat, opinion)
                com_feats.append(com_feat0)         
        else:
            for pos in ft_pos[FT_OPINION]:
                opinion = feats[pos]
                com_feat = '%s_%s' % (FT_TARGET, opinion)
                com_feats.append(com_feat)
    return com_feats

#=========================================================
if __name__=="__main__":
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)

    # cmd argument parser
    parser = OptionParser('Usage: buildfeature.py [options] --builduserdict|--selectfeature seltype')
    parser.add_option("-i", dest="inputfile",
            help="input file name")
    parser.add_option("-o", dest="outputfile",
            help="output file name")
    parser.add_option("--dict", dest="feature_dictpath",
            help="feature dictionaries path")
    parser.add_option("--userdict", dest="user_dictpath",
            help="jieba user dictionary path")
    parser.add_option("--jieba", dest="jieba_dictpath",
            help="jieba dictionary path")
    parser.add_option("--dat", dest="dat_filepath", default='',
            help="target name database file name")
    parser.add_option("--builduserdict",
                  action="store_true", 
                  help="run command: build user dict file for jieba. By default will run command of extract features by feature dict and save to .cut file.")
    parser.add_option("--selectfeature",
                  action="store", default='',
                  help="run command: select features from .cut file and save to new .cut file as input of trainer. E.g., select only the featuretag as the features.")
    
    opt, args = parser.parse_args()

    if len(sys.argv) < 2:
        print(globals()['__doc__'] % locals())
        parser.print_help()
        sys.exit(1)
    
    logger.info("running %s" % ' '.join(sys.argv))

    if opt.builduserdict:
        make_userdict( opt.jieba_dictpath + '/dict.txt',
                opt.feature_dictpath, opt.outputfile)
    elif opt.selectfeature:
        select_feature(opt.inputfile, opt.outputfile,opt.selectfeature)
    elif opt.inputfile:
        extract_file(opt.inputfile, opt.outputfile, 
                opt.dat_filepath,
                opt.feature_dictpath, opt.user_dictpath)
    else:
        extract_test(
                opt.dat_filepath,
                opt.feature_dictpath, opt.user_dictpath)

