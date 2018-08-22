﻿#coding=utf-8
import os
import jieba
import jieba.posseg as psg


special_newwords = []  # 特殊新词list


class pair:
    def __init__(self, word, flag):
        self.word = word
        self.flag = flag


def get_special_newwords(in_fn, code=u"UTF-8"):    # 加载特殊新词
    """
    加载特殊新词
    :param in_fn: 特殊新词的词典文件
    :param code: 词典文件的编码
    :return: 词典文件中的新词序列,list
    """
    global special_newwords
    with open(in_fn) as f:
        for line in f:
            if not line:
                continue
            else:
                word = line.decode(code, "ignore").strip()
                if word not in (None, u"") and word not in special_newwords:
                    special_newwords.append(word)
    f.close()
    return special_newwords


cur_path = os.path.dirname(os.path.abspath(__file__))
special_usedict_path = os.path.join(cur_path, u"userdict/userdict_special")
#usedict_path = os.path.join(cur_path, u"userdict/userdict")
#jieba.load_userdict(usedict_path)
jieba.load_default_userdict()
get_special_newwords(special_usedict_path, u"UTF-8")


def norm_cut_find(newwords, text):    # 查找文本中所含的特殊新词及其在text中的位置，可能出现多次出现的情况
    """
    查找文本中所含的特殊新词及其在text中的位置，可能出现多次出现的情况
    :param newwords: 特殊新词的序列，list或tuple或set
    :param text: 带查找的文本
    :return: dict {index1:special_word_1 .... indexN:special_word_N}
    """
    if newwords == [] or not newwords:
        return None
    else:
        found_terms = {}
        for word in newwords:
            tmp_index = 0
            found_index = text.find(word, tmp_index)
            while found_index >= 0:
                if found_index not in found_terms:
                    found_terms[found_index] = word
                else:
                    if len(found_terms[found_index]) < len(word):
                        found_terms[found_index] = word
                tmp_index += found_index + len(word)
                found_index = text.find(word, tmp_index)
        return found_terms


def add_special_word(word):    # 添加新词，新词仅在本次任务中有效
    """
    添加新词，新词仅在本次任务中有效
    :param word: 待添加的新词，unicode
    """
    global special_newwords
    if isinstance(word, str):
        special_newwords.append(word.strip().decode(u"UTF-8", u"ignore"))
    elif isinstance(word, unicode):
        special_newwords.append(word.strip())


def add_special_words(words):     # 添加一组新词，新词仅在本次任务中有效
    """
    添加一组新词，新词仅在本次任务中有效
    :param words: 待添加的新词序列，list或tuple或set
    """
    for word in words:
        add_special_word(word.strip())


def save_special_word(word):     # 添加新词到特殊新词词典文件userdict_special中，以后其他程序可用
    """
    添加新词到特殊新词词典文件userdict_special中，以后其他程序可用
    :param word: 需要添加的特殊新词
    :return: 成功添加到userdict_special的新词的个数
    """
    global special_usedict_path
    raw_lines = list(line for line in open(special_usedict_path).readlines())
    if isinstance(word, unicode):
        t_word = word.encode("UTF-8", "ignore")
    elif isinstance(word, str):
        t_word = word
    else:
        return 0
    tmp_line = t_word + u"\n".encode("UTF-8", "ignore")
    if tmp_line in raw_lines:
        return 0
    else:
        fw = open(special_usedict_path, 'a')
        fw.write(tmp_line)
        fw.close()
        return 1


def save_special_words(words):     # 添加一组新词到特殊新词词典文件userdict_special中，以后其他程序可用
    """
    添加一组新词到特殊新词词典文件userdict_special中，以后其他程序可用，词典中已存在的就不再添加
    :param words: 需要添加的特殊新词的序列
    :return: 成功添加的新词的个数
    """
    global special_usedict_path
    if not words:
        return 0
    count = 0
    raw_lines = list(line for line in open(special_usedict_path).readlines())
    fw = open(special_usedict_path, 'a')
    for word in words:
        if isinstance(word, unicode):
            t_word = word.encode("UTF-8", "ignore")
        elif isinstance(word, str):
            t_word = word
        else:
            continue
        tmp_line = t_word + u"\n".encode("UTF-8", "ignore")
        if tmp_line in raw_lines:
            continue
        else:
            count += 1
            fw.write(tmp_line)
    fw.close()
    return count


def del_special_word(word):      # 删除新词，仅当前程序有效，不更改userdict_special文件
    """
    删除新词，仅当前程序有效，不更改userdict_special文件
    :param word: 特殊新词
    :return: 成功删掉的词的个数
    """
    global special_newwords
    t_word=word
    if isinstance(word, str):
        t_word=word.decode(u"UTF-8", u"ignore")
    if t_word in special_newwords:
        special_newwords.remove(t_word)
        return 1
    else:
        return 0


def del_special_words(words):     # 删除一组新词，仅当前程序有效，不更改userdict_special文件
    """
    删除一组新词，仅当前程序有效，不更改userdict_special文件
    :param words: 特殊新词的序列
    :return: 成功删掉的词的个数
    """
    return sum(del_special_word(word) for word in words)


def del_word_from_special_userdict(word):     # 从userdict_special文件中删除新词，影响后续程序的使用

    """
    从userdict_special文件中删除新词
    :param word: 待删除新词
    :return: 是否从文件中删除了当前新词
    """
    global special_usedict_path
    raw_lines = list(line for line in open(special_usedict_path).readlines())
    if isinstance(word, unicode):
        t_word = word.encode("UTF-8", "ignore")
    elif isinstance(word, str):
        t_word = word
    else:
        return 0
    tmp_line = t_word + u"\n".encode("UTF-8", "ignore")
    if tmp_line in raw_lines:
        raw_lines.remove(tmp_line)
        fw = open(special_usedict_path, 'w')
        fw.write("\n")
        fw.writelines(raw_lines)
        fw.close()
        return 1
    else:
        return 0


def del_words_from_special_userdict(words):    # 从userdict_special文件中删除一组新词

    """
     从userdict_special文件中删除一组新词
    :param words: 待删除的新词的序列，list或tuple或set()
    :return: 成功从文件中给删除的新词个数
    """
    global special_usedict_path
    raw_lines = list(line for line in open(special_usedict_path).readlines())
    fw = open(special_usedict_path, 'w')
    count = 0
    for word in words:
        if isinstance(word, unicode):
            t_word = word.encode("UTF-8", "ignore")
        elif isinstance(word, str):
            t_word = word
        else:
            continue
        tmp_line = t_word + u"\n".encode("UTF-8", "ignore")
        if tmp_line in raw_lines:
            raw_lines.remove(tmp_line)
            count += 1
    fw.write("\n")
    fw.writelines(raw_lines)
    fw.close()
    return count


def norm_cut(text, newwords=None):    # 切词，对应jieba.cut,但是能识别出special_newwords在中的特殊词汇
    """
    切词，对应jieba.cut,但是能识别出special_newwords在中的特殊词汇
    :param text: 待切分文本，unicode
    :param newwords: 扩展的新词序列，list或tuple或set
    """
    global special_newwords
    if not newwords: newwords = []
    if isinstance(text, str):
        text = text.decode(u"UTF-8", u"ignore")
    if isinstance(newwords,tuple) or isinstance(newwords,set) or isinstance(newwords,list):
        found_terms = norm_cut_find(newwords=list(newwords) + special_newwords, text=text)
    else:
        found_terms=norm_cut_find(newwords=special_newwords,text=text)
    text_cut = jieba.cut(text)
    if found_terms is None or found_terms == {}:
        for item in text_cut:
            yield item
    else:
        current_text = text
        sorted_found_index = sorted(found_terms.keys())
        for index in sorted_found_index:
            current_text = current_text.replace(found_terms[index], u" ")
        index = 0
        for word in jieba.cut(current_text):
            if index not in found_terms:
                yield word
                index += len(word)
            else:
                yield found_terms[index]
                index += len(found_terms[index])


def norm_seg(text, newwords=None, new_flag="nz"):    # 带词性切词，对应jieba.posseg.cut,但是能识别出special_newwords在中的特殊词汇,同时，这些特殊新词的词性默认为nz
    """

    :param text:待切分文本，unicode
    :param newwords:扩展的新词序列，list或tuple或set
    :param new_flag:新词词性
    """
    global special_newwords
    if isinstance(text,str):
        text=text.decode("UTF-8","ignore")
    if not newwords: newwords = []
    if isinstance(newwords,tuple) or isinstance(newwords,set) or isinstance(newwords,list):
        found_terms = norm_cut_find(newwords=list(newwords) + special_newwords, text=text)
    else:
        found_terms=norm_cut_find(newwords=special_newwords,text=text)
    if found_terms is None or found_terms == {}:
        for item in jieba.posseg.cut(text):
            yield item
    else:
        current_text = text
        sorted_found_index = sorted(found_terms.keys())
        for index in sorted_found_index:
            current_text = current_text.replace(found_terms[index], " ")
        psg_list = list(jieba.posseg.cut(current_text))
        index = 0
        for item in psg_list:
            word = item.word
            if index not in found_terms:
                yield item
                index += len(word)
            else:
                yield pair(found_terms[index], new_flag)
                index += len(found_terms[index])
