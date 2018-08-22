# coding=utf-8
import os
def count_max_log_number(result_file_path):

    """
    :param result_file_path: 新词结果文件路径
    :return: 文件最大编号
    新词结果文件编码格式:'jin_'+日期+编号‘.log’,例如：jin_20140630_0.log，jin_20140630_1.log......
    """
    max_file_number = 0
    if os.path.exists(result_file_path) == True:
        for parent, dirnames ,filenames in os.walk(result_file_path):
            # string_to_deal = ''
            for filename in filenames:
                if filename.startswith('jin_'):
                    file_number=int(filename[12:len(filename)].strip('_.log'))
                    if file_number>max_file_number:
                        max_file_number = int(filename.strip('jin_.log'))
    return max_file_number