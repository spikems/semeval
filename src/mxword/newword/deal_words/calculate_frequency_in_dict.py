# coding=utf-8
import jieba
import math
import os

#jieba.set_dictionary("/home/next/coopinion/correct_jieba/jieba_dict_maintenance/original_dict.txt")


def calculate_words_dict_frequency(new_word, frequency_counted, frequency_dict, word_dict,
                                   jieba_dict_path=(jieba.get_abs_path_dict(), u'')):
    """
    :param new_word: 候选新词
    :return: freq，新词加入结巴词典时的词频
            若候选新词为字母、数字或者数字开头的词，则返回-1，表示非可用词
    """
    if jieba_dict_path[1] != "" :
        if os.path.isfile(jieba_dict_path[1]):
            jieba.load_userdict(jieba_dict_path[1])

    freq = 0
    str = ",".join(jieba.cut(new_word, HMM=False)).encode("utf-8")

    if new_word.isalpha() or new_word.isalnum() or str.lstrip('0123456789') != str:
        freq = -1
        return freq

    token_list = str.split(',')
    frequency_list = []

    for item in token_list:
        if not item.isalnum():
            if item in word_dict:
                frequency_list.append(frequency_dict[item])
            else:
                frequency_list.append(int(1))
        else:
            frequency_list.append(int(1))

    pro = 1.0
    for fre in frequency_list:
        pro *= (int(fre) / jieba.total)

    for i in xrange(1, 10000):
        if (i / jieba.total) > pro:
            if frequency_counted > i:
                freq = int(math.sqrt(frequency_counted * i))
            else:
                freq = i
            break

    return freq
