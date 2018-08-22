# encoding=utf-8
from scipy.stats import entropy

def calculate_right_entropy(suffix_dict=dict(), freq_cut=3):
    """
    计算右邻字的信息熵
    :rtype : object
    :param suffix_dict:
    后缀词典 {word1：{suffix1:n1,suffix2:n2，...},word2:{suffix1:k1,suffix2:k2，...},
              .........}
    :param freq_cut: 词频
    """
    unknown_words = dict()  #{word:[freq,IG,LIS,RIS]}
    word_list = suffix_dict.keys()
    for word in word_list:
        suffix_dic = suffix_dict[word]
        suffix_list = suffix_dic.keys()
        suffix_sum = 0
        for suffix in suffix_list:
            suffix_sum += suffix_dic[suffix] #该词总词频
        if suffix_sum < freq_cut:
            continue
        probability_list = []
        for suffix in suffix_list:
            p = float(suffix_dic[suffix]) / float(suffix_sum)  #该词该后缀后缀的概率
            probability_list.append(p)
        tmp_entropy = entropy(probability_list) #计算熵
        unknown_words[word] = [suffix_sum, None, None, tmp_entropy]  #{word: [freq, IG, LIS, RIS}
    return unknown_words


def calculate_left_entropy(suffix_dict=dict(),unknown_words=dict()):
    """
    计算左邻字的信息熵
    :param unknown_words:
    :rtype : object
    :param suffix_dict:
    后缀词典 {word1：{suffix1:n1,suffix2:n2，...},word2:{suffix1:k1,suffix2:k2，...},
              .........}
    :param freq_cut: 词频
    """
    word_list = unknown_words.keys()
    for word in word_list:
        if not word in suffix_dict:
            print '%s'%word
            continue
        suffix_dic = suffix_dict[word]
        suffix_list = suffix_dic.keys()
        suffix_sum = 0
        for suffix in suffix_list:
            suffix_sum += suffix_dic[suffix] #该词总词频
        probability_list = []
        for suffix in suffix_list:
            p = float(suffix_dic[suffix]) / float(suffix_sum)  #该词该后缀后缀的概率
            probability_list.append(p)
        tmp_entropy = entropy(probability_list) #计算熵
        infor_list=unknown_words[word]
        infor_list[2]=tmp_entropy
        unknown_words[word] = infor_list  #{word: [freq, IG, LIS, RIS}
