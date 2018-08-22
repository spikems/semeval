# coding=utf-8
from math import log

def calculate_IG(unknown_words,total_words_count):
        """
        calculate MutualInformation
        IG(电影院)=min( p(电影院)/(p(电)·p(影院)) , p(电影院)/(p(电影)·p(院)))
        Input: unkown_words,total_words_count
        Output: unkown_words中的IG  #{word: [freq, IG, LIS, RIS}
        """
        for word in unknown_words:
            if not unknown_words[word][1]:
                ig = 1000000.0
                for pos in xrange(1, len(word)):
                    if word[:pos] in unknown_words and word[pos:] in unknown_words:
                        rate = float(unknown_words[word][0]) / (
                            float(unknown_words[word[:pos]][0]) * float(unknown_words[word[pos:]][0]))
                        ig = min(ig, rate * total_words_count)
                unknown_words[word][1] = log(ig)
