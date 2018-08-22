# coding=utf-8
from math import log


def find_unknown_word(unknown_words,freq_IS_IG_product_cut,IS_IG_product_cut,IG_cut):
        """
        sort the unknown_words, and return the words satissify 'Thresholds'
        :rtype : object
        :param unknown_words:
        :param freq_IS_IG_product_cut: （freq，IS，IG，0.1）的乘积阈值，方便灵活筛选新词
        :param IS_IG_product_cut: IS、IG乘积阈值，方便灵活筛选新词
        :param IG_cut: IG阈值
        Input: unknown_words,freq_IS_IG_product_cut,IS_IG_product_cut,IG_cut
        Output: result
        """
        result = []
        result2 = []
        for key in sorted(unknown_words):
            try:
               tmp_freq = unknown_words[key][0]
               tmp_ig = unknown_words[key][1]
               tmp_is = min(unknown_words[key][2], unknown_words[key][3])
               if key.encode('utf-8').isalpha() or key.encode('utf-8').isalnum() or key.encode('utf-8').isdigit():
               #if key.isalpha() or key.isalnum() or key.isdigit():
                   continue

               #key = key.strip()
               key.strip(u'  ．　\n\t')

               if tmp_freq * 0.1 * tmp_ig * tmp_is >= freq_IS_IG_product_cut and len(key) >= 2 and tmp_ig * tmp_is >= IS_IG_product_cut and tmp_ig >= IG_cut:
                   result.append((key, unknown_words[key][0], unknown_words[key][1],
                       min(unknown_words[key][2], unknown_words[key][3])))
               else:
                   #save to result2 anyway
                   result2.append((key, tmp_freq, tmp_ig, unknown_words[key][2], unknown_words[key][3]))
            except:
                print 'except: %s: type=%s, freq = %s, ig=%s, is=%s'%(key.encode('utf-8'), type(key), tmp_freq, tmp_ig, tmp_is)

            #print '%s\t%s\t%s\t%s\t%s'%(key.encode('utf-8'), tmp_freq, tmp_ig, unknown_words[key][2], unknown_words[key][3])
        #keys_tp = unknown_words.keys()
        #for ix in xrange(len(keys_tp)):
        #    keys_tp[ix]=keys_tp[ix].encode('utf-8', errors='ignore')

        result.sort(key=lambda d: log(d[1]) * d[2] * d[3], reverse=True)
        result2.sort(key=lambda d: log(d[1]) * d[2] * d[3], reverse=True)

        return result, result2
