#encoding=utf-8

from nltk import ngrams
from collections import Counter

def grams_count(grams_list):
    return Counter(grams_list)

def convert_grams_counter(counter_dict):
    left_counts=dict()
    right_counts=dict()
    for key in counter_dict:
        if len(key)==1:
            left_counts.setdefault(key[0],dict())
            left_counts[key[0]].setdefault(u'',0)
            left_counts[key[0]][u'']+=1
            right_counts.setdefault(key[0],dict())
            right_counts[key[0]].setdefault(u'',0)
            right_counts[key[0]][u'']+=1
            continue
        right_counts.setdefault(key[:-1],dict())
        right_counts[key[:-1]].setdefault(key[-1],0)
        right_counts[key[:-1]][key[-1]]+=1

        left_counts.setdefault(key[1:],dict())
        left_counts[key[1:]].setdefault(key[0],0)
        left_counts[key[1:]][key[0]]+=1
    return left_counts,right_counts


def generate_ngrams(in_data=u'',sep=u' ',max_tokens=5):
    """
    paras: in_data: list or string which has been cut joined with sep
    paras: sep: when content is str or unicode, this will be used
    paras: max_tokens: threshhold for ngrams

    return: all possible ngrams for len(ngrams)<=max_tokens
    """
    if not in_data:
        return None
    if isinstance(in_data,str):
        in_data=in_data.decode(u'utf8',errors='ignore')
        in_data=in_data.split(sep)
    elif isinstance(in_data,unicode):
        in_data=in_data.split(sep)
    elif isinstance(in_data,(tuple,list)) or hasattr(in_data,u'next'):
        in_data=list(in_data)
    else:
        return None

    result=[]
    for ix in range(1,max_tokens+1):
        result.extend(ngrams(in_data,ix))

    return result

if __name__=='__main__':
    string_list=[u'吃 葡萄 不 吐 葡萄 皮',u'不 吃 葡萄 倒 吐 葡萄 皮']
    grams=[]
    for elem in string_list:
        grams.extend(generate_ngrams(elem))

    counter_dict=grams_count(grams)
    left,right=convert_grams_counter(counter_dict)

    print