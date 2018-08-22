# -*- coding: utf-8 -*-
def print_words(new_words_list):
    """
    格式化输出新词识别结果
    :param new_words_list: 新词列表 [word,frequency,IG,IS]
    """
    print "-----------------------------------------------------"
    print "新词".center(15), "词频".center(15), "互信息".center(15), "信息熵 ".center(15)
    print "（Token）".center(15), "（Frequency）".center(15), "（IG）".center(14), "（IS）".center(14)
    print "-----------------------------------------------------"

    if len(new_words_list) > 0:
        for word_to_add in new_words_list:
            print '   ',word_to_add[0].encode('utf-8', 'ignore').ljust(10),'\t', str("%d" % (word_to_add[1])).rjust(6), ("%.3f" % (round(word_to_add[2], 3))
                    ).rjust(14), ("%.3f" % (round(word_to_add[3], 3))).rjust(12)
        print "-----------------------------------------------------"
        print "\t\t\t共识别出", len(new_words_list), '个新词'
