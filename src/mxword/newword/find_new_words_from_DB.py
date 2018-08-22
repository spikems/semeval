# -*- coding: utf-8 -*-
# !/usr/bin/python
# 这个是从服务器上的数据库中读取数据，进行新词识别的接口
#结巴词典是用来筛选unknown Words的，即通过信息熵、互信息及频率筛选的词是否已存在于词典中
import time
import sys

from db_api import connect, db_read_data
from deal_words.merge_new_words import merge
from deal_words.load_jieba_dict import load_jieba_words
from deal_words.merge_new_words import merge

from find_new_words import WordsFinder
import jieba

class find_new_word_from_DB(object):
    def __init__(self, db='next', table_name='m_table', cols=[u'clean_text'], batch_id='batch_id=20140630',
                 jieba_dict_path=(jieba.get_abs_path_dict(),u" "), max_tokens=5,
                 freq_IS_IG_product_cut=30, IS_IG_product_cut=20, IG_cut=11.5,data_volume_unit=10):
        """
        从数据库中读取数据，识别新词，然后与之前识别的新词合并，继续读取数据....
        :param jieba_dict_path:
        :param data_volume_unit:
        :rtype : object
        :param db:数据库
        :param table_name:表名
        :param cols:列名
        :param batch_id:
        :param max_tokens:
        :param freq_IS_IG_product_cut:
        :param IS_IG_product_cut:
        :param IG_cut:
        """
        self.dsn = 'localhost:' + db
        self.table_name = table_name
        self.cols = cols
        self.batch_id = batch_id
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

    def find_words(self):
        """
        """
        self.dic_set = load_jieba_words(self.jieba_dict_path)
        handler = connect(dsn=self.dsn)
        cursor = db_read_data(handler, self.table_name, self.batch_id, *self.cols)
        start_all = time.time()
        texts_size = 0
        start = time.time()
        data = cursor.fetchone()
        if not data:
            # print 'No data (' + self.batch_id + ')'
            sys.exit(0)

        self.text_list.append(data[u'clean_text'])
        texts_size += sys.getsizeof(data[u'clean_text'])
        while data:
            data = cursor.fetchone()
            if data:
                self.text_list.append(data[u'clean_text'])
                texts_size += sys.getsizeof(data[u'clean_text'])
            if texts_size >= self.data_volume_unit * 1024 * 1024:
                end = time.time()
                # print "------------------ fetch data done------------------ ", end - start, 's'
                ab = WordsFinder(text_list=self.text_list, max_tokens=self.max_tokens,
                                                freq_IS_IG_product_cut=self.freq_IS_IG_product_cut,
                                                IS_IG_product_cut=self.IS_IG_product_cut, IG_cut=self.IG_cut)
                ab.find_words()
                self.span_list.append(ab.spans)

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

        merge(ab.result, self.dic_set, self.useless_word_dict,self.token_list,self.newwords)

        end_all = time.time()
        total_time = end_all - start_all
        # print "\ntotal Time:", total_time, 's'
        # print "Time Efficiency:", round(self.data_volume_unit / total_time, 3), ' MB/Second'
        # print 'len(self.newwords)', len(self.newwords)











