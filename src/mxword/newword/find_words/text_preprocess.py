# coding=utf-8
import string
from .special_chars_tool import special_chars_patt

def text_preprocess(text_list, seg_label):
    """
    将初始数据分割成一个一个的句子，去掉句末标点，去掉网页标签、链接之类的英文串，放入list中
    :param text_list:
    :param seg_label:
    :rtype : object
    Input: text_list      seg_label="<SENT_BR>"   以seg_label连接的句子组成的list
    Output: spans  处理后的文本list，由之前的标点符合隔开的文本片段组成的list
    例如:
    输入：湖南综艺《爸爸去哪儿》最近非常火。<SENT_BR>你看了吗？
    输出：
        湖南综艺
        爸爸去哪儿
        最近非常火
        你看了吗
    """
    spans=list()
    # special_chars = string.punctuation
    # special_chars = [unicode(char) for char in special_chars] + [u'\s']
    # chinese_chars = [u'！', u'“', u'”', u"‘", u"’", u'（', u'）', u'×', u'+', u'，',
    #                  u'—', u'——', u'。', u'/', u'：', u'；', u'《', u'=', u'》', u'？',
    #                  u'@', u'【', u'】', u'…', u'……', u'『', u'』', u'～', u'　', u'、']

    # all_punctuations = chinese_chars + special_chars
    for text in text_list:
        sentence_list = text.split(seg_label)
        for line in sentence_list:
            units=special_chars_patt.split(line)
            for unit in units:
                 if not unit.isalnum() and unit != '':
                    # 筛掉网页标签、链接等英文串,空串
                     spans.append(unit)
                     #yield unit
    return spans

