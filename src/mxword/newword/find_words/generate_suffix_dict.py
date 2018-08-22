# encoding=utf-8
"""
samples：
    ['吃 葡萄 不 吐 葡萄 皮',
    '不 吃 葡萄 倒 吐 葡萄 皮']

right_suffix_dict:
 吃 :{ 葡萄 : 2      }
 不 :{ 吐 : 1      吃 : 1      }
 吐 :{ 葡萄 : 2      }
 倒 :{ 吐 : 1      }
 倒吐 :{ 葡萄 : 1      }
 不吃葡萄 :{ 倒 : 1      }
 皮 :{  : 2      }
 吐葡萄 :{ 皮 : 2      }
 不吐葡萄 :{ 皮 : 1      }
 吐葡萄皮 :{  : 2      }
 葡萄皮 :{  : 2      }
 葡萄倒吐 :{ 葡萄 : 1      }
 吃葡萄倒 :{ 吐 : 1      }
 葡萄倒 :{ 吐 : 1      }
 葡萄 :{ 倒 : 1      不 : 1      皮 : 2      }
 不吃 :{ 葡萄 : 1      }
 不吐 :{ 葡萄 : 1      }
 倒吐葡萄 :{ 皮 : 1      }
 葡萄不 :{ 吐 : 1      }
 葡萄不吐 :{ 葡萄 : 1      }
 吃葡萄不 :{ 吐 : 1      }
 吃葡萄 :{ 倒 : 1      不 : 1      }

left_suffix_dict:
 吃 :{  : 1      不 : 1      }
 不 :{  : 1      葡萄 : 1      }
 吐 :{ 倒 : 1      不 : 1      }
 倒 :{ 葡萄 : 1      }
 倒吐 :{ 葡萄 : 1      }
 不吃葡萄 :{  : 1      }
 皮 :{ 葡萄 : 2      }
 吐葡萄 :{ 倒 : 1      不 : 1      }
 不吐葡萄 :{ 葡萄 : 1      }
 吐葡萄皮 :{ 倒 : 1      不 : 1      }
 葡萄皮 :{ 吐 : 2      }
 葡萄倒吐 :{ 吃 : 1      }
 吃葡萄倒 :{ 不 : 1      }
 葡萄倒 :{ 吃 : 1      }
 葡萄 :{ 吐 : 2      吃 : 2      }
 不吃 :{  : 1      }
 不吐 :{ 葡萄 : 1      }
 倒吐葡萄 :{ 葡萄 : 1      }
 葡萄不 :{ 吃 : 1      }
 葡萄不吐 :{ 吃 : 1      }
 吃葡萄不 :{  : 1      }
 吃葡萄 :{  : 1      不 : 1      }

"""

def generate_right_suffix_dict(textList=[], max_Token=3):
    """
    :rtype : object
    :param textList: spans 以空格隔开的被切分的文本段列表
    :param max_Token: 最大词项
    :return: suffix_dict后缀词典
    """
    total_words_count = 0
    suffix_dict = dict()  #{word:{suffix:frequency,}}

#    for rowN in xrange(0, len(textList)):     #第rowN行
#        rowItems = textList[rowN].split(' ')  #'吃,葡萄,不,吐,葡萄,皮'
    for row in textList:
        rowItems = row.split(' ')  #'吃,葡萄,不,吐,葡萄,皮'
        total_words_count += len(rowItems)
        start = 0
        while start<len(rowItems):
            for wordlen in xrange(1, max_Token+1):#该行取start到start+wordlen-1位置的wordlen段形成新词
                if (start + wordlen <= len(rowItems)): #文本够长度
                    tmp_word_items = rowItems[start:start + wordlen] #新词组合项
                    tmp_word = ''.join(tmp_word_items) #新词
                    #tmp_word_conj = ' '.join(tmp_word_items) #新词对应原文
                    if tmp_word not in suffix_dict: #未处理过的新词
                        if start + wordlen >= len(rowItems):#该词在句末
                            suffix_dict[tmp_word] = {'': 1} #该词的右邻字为''
                        else: #该词在句中
                            suffix_dict[tmp_word] = {rowItems[start + wordlen]: 1} #添加右邻字
                            continue
                    else:#处理过的新词
                        tmp_suffix_dict = suffix_dict[tmp_word]
                        if start + wordlen >= len(rowItems):#该词在句末
                            if '' in tmp_suffix_dict:#已存在‘’
                                tmp_suffix_dict[''] += 1
                                suffix_dict[tmp_word] = tmp_suffix_dict
                            else:
                                tmp_suffix_dict[''] = 1
                                suffix_dict[tmp_word] = tmp_suffix_dict
                        else: #该词在句中
                            suffix = rowItems[start + wordlen]
                            tmp_suffix_dict = suffix_dict[tmp_word]
                            if suffix in tmp_suffix_dict:#suffix已存在
                                tmp_suffix_dict[suffix] += 1
                                suffix_dict[tmp_word] = tmp_suffix_dict
                            else:#suffix不存在
                                tmp_suffix_dict[suffix] = 1
                                suffix_dict[tmp_word] = tmp_suffix_dict
            start += 1
    return tuple([suffix_dict, total_words_count])


def generate_left_suffix_dict(textList=[], max_Token=3):
    """
    :rtype : object
    :param textList: spans 以空格隔开的被切分的文本段列表
    :param max_Token: 最大词项
    :return: suffix_dict后缀词典
    """
    suffix_dict = dict()  #{word:{suffix:frequency,}}
    #for rowN in xrange(0, len(textList)):     #第rowN行
    #   rowItems = textList[rowN].split(' ')  #'吃,葡萄,不,吐,葡萄,皮'
    for row in textList:
        rowItems = row.split(' ')  #'吃,葡萄,不,吐,葡萄,皮'
 
        start = 0
        while start<len(rowItems):
            for wordlen in xrange(1, max_Token+1):#该行取start到start+wordlen-1位置的wordlen段形成新词
                if (start + wordlen <= len(rowItems)): #文本够长度
                    tmp_word_items = rowItems[start:start + wordlen] #新词组合项
                    tmp_word = ''.join(tmp_word_items) #新词
                    #tmp_word_conj = ' '.join(tmp_word_items) #新词对应原文
                    if tmp_word not in suffix_dict: #未处理过的新词
                        if start==0:#该词在句首
                            suffix_dict[tmp_word] = {'': 1} #该词的左邻字为''
                        else: #该词在句中
                            suffix_dict[tmp_word] = {rowItems[start-1]: 1} #添加左邻字
                            continue
                    else:#处理过的新词
                        tmp_suffix_dict = suffix_dict[tmp_word]
                        if start == 0:#该词在句首
                            if '' in tmp_suffix_dict:#已存在‘’
                                tmp_suffix_dict[''] += 1
                                suffix_dict[tmp_word] = tmp_suffix_dict
                            else:
                                tmp_suffix_dict[''] = 1
                                suffix_dict[tmp_word] = tmp_suffix_dict
                        else: #该词在句中
                            suffix = rowItems[start - 1]
                            tmp_suffix_dict = suffix_dict[tmp_word]
                            if suffix in tmp_suffix_dict:#suffix已存在
                                tmp_suffix_dict[suffix] += 1
                                suffix_dict[tmp_word] = tmp_suffix_dict
                            else:#suffix不存在
                                tmp_suffix_dict[suffix] = 1
                                suffix_dict[tmp_word] = tmp_suffix_dict
            start += 1
    return suffix_dict

def print_suffix_dict(suffix_dict=dict()):
    print 'size:%d'%len(suffix_dict.keys())
    for word in suffix_dict:
        print '',word,':{',
        suf_dic = suffix_dict[word]
        suffix_list = suf_dic.keys()
        for suffix in suffix_list:
            print suffix,':',suf_dic[suffix],'    ',
        print "}"


if __name__ == '__main__':
    spans = ['吃 葡萄 不 吐 葡萄 皮','不 吃 葡萄 倒 吐 葡萄 皮']
    max_tokens = 3

    tuple1 = generate_right_suffix_dict(textList=spans, max_Token=max_tokens)
    right_suffix_dict = tuple1[0]
    total_words_count = tuple1[1]
    left_suffix_dict = generate_left_suffix_dict(textList=spans,max_Token=max_tokens)
    print "================"
    print_suffix_dict(right_suffix_dict)
    print "================"
    print_suffix_dict(left_suffix_dict)
    print "================"




