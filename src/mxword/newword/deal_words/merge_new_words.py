# coding=utf-8
def merge(result, dic_set, useless_word_dict, token_list, newwords):
    """
     将result中的新词添加进newwords中，会过滤掉结巴词典中已经存在的词、数字字母词、含无用词根的词。
    :param result:（word, freq, IG, minIS)
    :param dic_set: 结巴词典中的词
    :param useless_word_dict: 无用词根词典
    :param token_list: 记录newwords中已经存在的词
    :param newwords:
    """
    for word_to_add in result:  # 待添加的新词
        if word_to_add[0].encode('utf-8') not in dic_set and not word_to_add[0].isdigit():  #不在结巴词典里，非数字
            contain_useless_words = 0
            for uselessWord in useless_word_dict:
                if word_to_add[0].find(uselessWord) >= 0:
                    contain_useless_words += 1
                    break
            if contain_useless_words:
                continue
            if word_to_add[0] in token_list:  #在newwords里
                for item in newwords:
                    if item[0] == word_to_add[0]:
                        newwords.append((
                            item[0], item[1] + word_to_add[1], max(item[2], word_to_add[2]), max(item[3], word_to_add[3])))
                        newwords.remove(item)
            else:  #不在newords里
                newwords.append(word_to_add)
                token_list.append(word_to_add[0])
