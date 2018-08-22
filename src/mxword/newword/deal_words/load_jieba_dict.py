# coding=utf-8
import jieba
import os

def load_jieba_words(jieba_dict_path=(jieba.get_abs_path_dict(), u'')):
    """
    加载结巴词典中的词
    :param jieba_dict_path: jieba词典的路径
    :return: dic_set 结巴词典中的词
    """
    dic_set = set()

    with open(jieba_dict_path[0]) as f:
        for row in f:
            # items = row.decode('utf-8').split(' ')
            items = row.split(' ')
            dic_set.add(items[0])

    if jieba_dict_path[1] != "" :
        if os.path.isfile(jieba_dict_path[1]):
            with open(jieba_dict_path[1]) as f:
                for row in f:
                    # items = row.decode('utf-8').split(' ')
                    items = row.split(' ')
                    dic_set.add(items[0])
    return dic_set


def load_jieba_frequency(jieba_dict_path=(jieba.get_abs_path_dict(), u'')):
    dict_frequency = dict()
    #jieba.set_dictionary(jieba_dict_path)
    with open(jieba_dict_path[0]) as f:
        for row in f:
            #items = row.decode('utf-8').split(' ')
            items = row.split(' ')
            dict_frequency[items[0]] = int(items[1])

    if jieba_dict_path[1] != "":
        if os.path.isfile(jieba_dict_path[1]):
            with open(jieba_dict_path[1]) as f:
                for row in f:
                #items = row.decode('utf-8').split(' ')
                    items = row.split(' ')
                    dict_frequency[items[0]] = int(items[1])
    return dict_frequency
