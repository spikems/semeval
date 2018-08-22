# encoding=utf-8
import time
from find_words.text_preprocess import text_preprocess
from find_words.generate_suffix_dict import generate_right_suffix_dict,generate_left_suffix_dict, print_suffix_dict
from find_words.calculate_entropy import calculate_right_entropy,calculate_left_entropy
from find_words.calculate_mutual_information import calculate_IG
from find_words.find_unknown_words import find_unknown_word

class WordsFinder(object):
    def __init__(self, text_list, max_tokens=5, freq_cut=9, freq_IS_IG_product_cut=30, IS_IG_product_cut=20,
                 IG_cut=11.5):
        """
        :type self: object
        :rtype : object
        :param text_list: 用于新词识别的文本list
        :param max_tokens: 用于组成新词的最大词条数N（N-gram）
        :param freq_cut: 最小词频
        :param freq_IS_IG_product_cut: （freq，IS，IG，0.1）的最小积，用于灵活筛选新词
        :param IS_IG_product_cut: （IS，IG）的最小积，用于灵活筛选新词
        :param IG_cut: 最小IG （词的凝固程度）
        """
        super(WordsFinder, self).__init__()
        self.text_list = text_list
        self.spans = list()
        self.max_tokens = max_tokens
        self.freq_cut = freq_cut
        self.freq_IS_IG_product_cut = freq_IS_IG_product_cut
        self.IS_IG_product_cut = IS_IG_product_cut
        self.IG_cut = IG_cut
        self.unknown_words = dict()  #{word: [freq, IG, LIS, RIS}
        self.result = list()  #(word, freq, IG, minIS)
        self.retall = list()
        self.total_words_count = 0

    def find_words(self):
        """
        """
        start = time.time()
        self.spans = text_preprocess(text_list=self.text_list, seg_label="<SENT_BR>")
        end = time.time()
        print "------------ prep done -----------------------------", end - start, 's'

        tuple1 = generate_right_suffix_dict(textList=self.spans, max_Token=self.max_tokens)
        right_suffix_dict = tuple1[0]
        self.total_words_count = tuple1[1]
        left_suffix_dict = generate_left_suffix_dict(textList=self.spans,max_Token=self.max_tokens)
        start = time.time()
        print "------------ generate suffix dict done -------------------", start - end, 's'

        unknown_words = calculate_right_entropy(suffix_dict=right_suffix_dict, freq_cut=self.freq_cut) #{}
        # for word in unknown_words.keys:
        #     print  word,':[',unknown_words[word][0],',',unknown_words[word][1],',',unknown_words[word][2],',',unknown_words[word][3],']'
        self.unknown_words = unknown_words
        end = time.time()
        print "------------ calculate right entropy done ----------", end - start, 's'

        calculate_left_entropy(left_suffix_dict,unknown_words)
        start = time.time()
        print "------------ calculate left entropy done -----------", start - end, 's'

        calculate_IG(unknown_words=self.unknown_words, total_words_count=self.total_words_count)
        end = time.time()
        print "------------ calculate MutualInformation done ------", end - start, 's'

        self.result, self.retall = find_unknown_word(unknown_words=self.unknown_words,freq_IS_IG_product_cut=self.freq_IS_IG_product_cut,
                    IS_IG_product_cut=self.IS_IG_product_cut, IG_cut=self.IG_cut)
        start = time.time()
        print "------------ select New Words ----------------------", start - end, 's'
