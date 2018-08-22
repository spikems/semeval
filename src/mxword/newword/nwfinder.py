# -*- coding: utf-8 -*-
# !/usr/bin/python
"""
Find new words from .txt input


"""


import time
import sys,os

from optparse import OptionParser
import logging
from deal_words.merge_new_words import merge
from deal_words.load_jieba_dict import load_jieba_words
from deal_words.merge_new_words import merge
from deal_new_words import deal_new_words_for_dict
from save_words.write_new_words_to_log import write_to_log
from find_new_words import WordsFinder
import jieba

def save_result(filename, result):
    with open(filename,'w') as outf:
        for rec in result:
            outf.write('%s %s %s %s\n'%(rec[0].encode('utf-8'), rec[1], rec[2], rec[3]))


class NewWordFinder(object):
    def __init__(self, inputfile='input.txt',
                jieba_dict_path = (jieba.get_abs_path_dict(),u" "),
                max_tokens=5,
                freq_IS_IG_product_cut=30, IS_IG_product_cut=20, 
                IG_cut=11.5,data_volume_unit=10):
        """
        从文件中读取数据，识别新词，然后与之前识别的新词合并，继续读取数据....
        :param jieba_dict_path:
        :param data_volume_unit:
        :rtype : object
        :param max_tokens:
        :param freq_IS_IG_product_cut:
        :param IS_IG_product_cut:
        :param IG_cut:
        """
        self.input = inputfile
        self.jieba_dict_path = jieba_dict_path
        self.dic_set = set()
        self.max_tokens = max_tokens
        self.freq_IS_IG_product_cut = freq_IS_IG_product_cut
        self.IS_IG_product_cut = IS_IG_product_cut
        self.IG_cut = IG_cut
        self.useless_word_dict = [u'的', u'了', u'着', u'是', u'会', u'都', u'就', u'要']
        self.newwords = list()
        self.token_list = list()  #记录newwords中已经存在的词
        self.span_list = []
        self.text_list = []
        self.data_volume_unit = data_volume_unit  #一个测试单元的数据量大小，单位MB，用于测试性能

    def find_words(self, startcol = 2, unittype = 'CHAR'):
        """
            unittype = 'CHAR' or 'WORD'
        """
        self.dic_set = load_jieba_words(self.jieba_dict_path)

        inf = open(self.input, 'r')
        start_all = time.time()
        texts_size = 0
        start = time.time()
        chunkid = 0

        for line in inf:
            data = line.strip()
            #all convert to unicode
            #because ngram depend on the char boundary
            data = data.decode('utf-8')

            # find the start col
            pos = 0
            while startcol > 0:
                pos = data.find(u' ',pos)
                if pos > 0:
                    pos += 1
                else:
                    break
                startcol -= 1
            if startcol > 0:
                break
            data = data[pos:]
                    
            #char or word as basic unit
            if unittype == 'CHAR':
                #have to use unicode
                data = u' '.join([ x for x in data])

            self.text_list.append(data)
            texts_size += sys.getsizeof(data)
            if texts_size >= self.data_volume_unit * 1024* 1024 * 1024:
                end = time.time()
                # print "------------------ fetch data done------------------ ", end - start, 's'
                ab = WordsFinder(text_list=self.text_list, max_tokens=self.max_tokens,
                                                freq_IS_IG_product_cut=self.freq_IS_IG_product_cut,
                                                IS_IG_product_cut=self.IS_IG_product_cut, IG_cut=self.IG_cut)
                ab.find_words()
                self.span_list.append(ab.spans)

                save_result('result.%d'%chunkid, ab.result)
                save_result('all.%d'%chunkid, ab.retall)
                chunkid += 1

                merge(ab.result, self.dic_set, self.useless_word_dict,self.token_list,self.newwords)
                self.text_list = []
                texts_size = 0
                start = time.time()

        end = time.time()
        # print "------------------ fetch data done------------------ ", end - start, 's'
        ab = WordsFinder(text_list=self.text_list, max_tokens=self.max_tokens,
                                        freq_IS_IG_product_cut=self.freq_IS_IG_product_cut,
                                        IS_IG_product_cut=self.IS_IG_product_cut, IG_cut=self.IG_cut)
        ab.find_words()
        self.span_list.append(ab.spans)

        save_result('result.%d'%chunkid, ab.result)
        save_result('all.%d'%chunkid, ab.retall)
 
        merge(ab.result, self.dic_set, self.useless_word_dict,self.token_list,self.newwords)

        end_all = time.time()
        total_time = end_all - start_all
        # print "\ntotal Time:", total_time, 's'
        # print "Time Efficiency:", round(self.data_volume_unit / total_time, 3), ' MB/Second'
        # print 'len(self.newwords)', len(self.newwords)


def load_option():
    op = OptionParser()
    op.add_option("-i",
                  action="store", type = str, dest='input',
                  help="set the input filename.")
    op.add_option("-o",
                  action="store", type = str, dest='output',
                  help="set the output filename.")
    op.add_option("--jieba",
                  action="store", type = str, dest='jiebadir',
                  default='',
                  help="set the jieba home dir.")
    op.add_option("--savelog",
                  action="store_true",
                  help="set to save context of newwords.")
 
    (opts, args) = op.parse_args()

    return opts


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

    # cmd argument parser
    opts = load_option()

    #out put the final
    max_tokens = 5  #
    freq_IS_IG_product_cut = 5  #
    IS_IG_product_cut = 3.6 #10
    IG_cut = 4 #11.5
    data_volume_unit = 40  
    file_words_count = 10000
    industry = 'auto'

    # check --jiebadir
    if opts.jiebadir:
        jieba_dict_maintenance_dir = opts.jiebadir
    else:
        # ../jiebadict/
        jieba_dict_maintenance_dir= sys.argv[0][:sys.argv[0].rfind('/')] + '/../jiebadict/'

    jieba_main_dict_path = jieba_dict_maintenance_dir+"dict.txt"

    if not os.path.exists(jieba_main_dict_path):
        logger.error('%s not found, quit...', jieba_main_dict_path)
        sys.exit(-1)
    
    industry_dir = jieba_dict_maintenance_dir + industry
    unknown_dir = industry_dir + "/unknow_dir/"
    done_dir = industry_dir + "/done_dir/"
    jieba_industry_dict_path = industry_dir + "/industry_words.txt"
    jieba_dict_path = (jieba_main_dict_path, jieba_industry_dict_path)

    if opts.savelog:
        if os.path.exists(industry_dir)==False:
            os.mkdir(industry_dir)
        
        if os.path.exists(unknown_dir)==False:
            os.mkdir(unknown_dir)
        
        if os.path.exists(done_dir)==False:
            os.mkdir(done_dir)
    
        if os.path.isfile(jieba_industry_dict_path)==False:
            f=open(jieba_industry_dict_path,'w')
            f.close()

    # print 'Data Base : ', db
    # print 'Table Name : ', table_name
    # print 'Columns : ', cols
    # print 'Date of data : ', data_date
    # print 'N of N-Gram : ', max_tokens
    # print 'Min Product of (Frequency ,IS ,IG ,0.1 ) : ', freq_IS_IG_product_cut  #
    # print 'Min Product of (IS ,IG) : ', IS_IG_product_cut
    # print 'Min IG : ', IG_cut
    # print 'Data Volume of A Unit : ', data_volume_unit, ' MB'  #一个测试单元的数据量大小，单位MB，用于测试性能
    # print 'Words Count of A .Log File : ', file_words_count
    # print 'Result File Path : ', unknown_dir
    # print 'jieba Dictionary Path : ', jieba_dict_path[0], ',', jieba_dict_path[1]
    
   
    finder = NewWordFinder(opts.input, jieba_dict_path, max_tokens, 
            freq_IS_IG_product_cut, IS_IG_product_cut, 
            IG_cut, data_volume_unit)
    finder.find_words()
    newwords = finder.newwords

    #save the result
    save_result(opts.output, newwords);

    if opts.savelog:
        NR_Preffix=['长','常委','主任','主席','经理','总裁','明星','助理','教师','总监','记者','师','员',
                    '人','主管','官','CEO','CFO','CTO','CIO','COO','会计','导购','代理','演员','礼仪',
                    '导游','医生','大使','司仪']
        NR_Suffix=['先生','小姐','女士']
 
        # it's very slow to run deal, find_context
        dnWD = deal_new_words_for_dict(newwords, finder.span_list, jieba_dict_path)
        dnWD.deal((NR_Preffix,NR_Suffix))

        write_to_log(dnWD.new_words, dnWD.new_words_dic_frequency, dnWD.context_dict, file_words_count, unknown_dir)
    



