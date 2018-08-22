#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

regular_chars=[u'～',u'＄',u'％',u'＊',u'＂',u'＇',u'＼',u'？',u'＞',u'＜',u'~']+\
              [u'！',u'“',u'”',u"‘",u"’",u'（', u'）', u'×', u'+', u'，']+\
              [u'—', u'-',u'。',u'/', u'：', u'；', u'《', u'=', u'》',u'？']+\
              [u'@', u'【', u'】',u'…',u'『', u'』', u'～',u'、',u'＠',u'＃']+\
              [u'￥',u'％',u'＆',u'＋',u'“',u'”',u'‘',u'’',u'｜',u'／',u'｀',u'◆',u'●']+\
              [u'!',u'"',u'\'',u'#',u'%',u'&',u',',u'/',u':',u';',u'<',u'=',u'>',u'@',u'^',u'_',u'`']

special_re_string=u'''['''+u''.join(regular_chars)+u'''\.\^\$\*\+\?\{\}\[\]\\\|\(\)+'u']'''
special_chars_patt=re.compile(special_re_string)

def get_special_chars():
    return regular_chars+list(set(u'.^$*+?{}[]\|()'))

del re