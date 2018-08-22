#coding=UTF-8
import jieba
txt=u"国民上仙霍建华来成都啦"
#for tem in jieba.cut(txt):
#    print tem

from jieba.norm import norm_seg
for tem in norm_seg(txt):
    print tem.word,tem.flag

