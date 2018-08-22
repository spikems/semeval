# encoding=utf-8
import datetime
from find_new_words_from_DB import find_new_word_from_DB
from deal_new_words import deal_new_words_for_dict
from save_words.write_new_words_to_log import write_to_log
from ConfigParser import ConfigParser
import sys, os

# 系统关键参数
config = ConfigParser()
file_config = 'industry.config'
config.read(file_config)
industry = sys.argv[1]
industry_path = config.get(u'Path', industry)
db = config.get(industry+"_db", 'db')
table_name= config.get(industry+"_db", 'table')
cols= config.get(industry+"_db", 'columns').split(",")
delay= int(config.get(industry+"_db", 'day_delay'))
data_date = (datetime.datetime.now()-datetime.timedelta(days=delay)).strftime("%Y%m%d")
batch_id = 'batch_id=' + data_date


max_tokens = 5  #
freq_IS_IG_product_cut = 15  #
IS_IG_product_cut = 10
IG_cut = 11.5
data_volume_unit = 10  #一个测试单元的数据量大小，单位MB，用于测试性能
file_words_count = 100

jieba_dict_maintenance_dir="/home/next/coopinion/correct_jieba/jieba_dict_maintenance/"
jieba_main_dict_path = jieba_dict_maintenance_dir+"original_dict.txt"

industry_dir = jieba_dict_maintenance_dir + industry
if os.path.exists(industry_dir)==False:
    os.mkdir(industry_dir)

unknown_dir = industry_dir + "/unknow_dir/"
if os.path.exists(unknown_dir)==False:
    os.mkdir(unknown_dir)

done_dir = industry_dir + "/done_dir/"
if os.path.exists(done_dir)==False:
    os.mkdir(done_dir)

jieba_industry_dict_path = industry_dir + "/industry_words.txt"
if os.path.isfile(jieba_industry_dict_path)==False:
    f=open(jieba_industry_dict_path,'w')
    f.close()
jieba_dict_path = (jieba_main_dict_path, jieba_industry_dict_path)


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

NR_Preffix=['长','常委','主任','主席','经理','总裁','明星','助理','教师','总监','记者','师','员',
            '人','主管','官','CEO','CFO','CTO','CIO','COO','会计','导购','代理','演员','礼仪',
            '导游','医生','大使','司仪']
NR_Suffix=['先生','小姐','女士']

fnDB = find_new_word_from_DB(db, table_name, cols, batch_id, jieba_dict_path, max_tokens, freq_IS_IG_product_cut,
                             IS_IG_product_cut, IG_cut, data_volume_unit)
fnDB.find_words()
newwords = fnDB.newwords
dnWD = deal_new_words_for_dict(newwords, fnDB.span_list, jieba_dict_path)
dnWD.deal((NR_Preffix,NR_Suffix))
write_to_log(dnWD.new_words, dnWD.new_words_dic_frequency, dnWD.context_dict, file_words_count, unknown_dir)
