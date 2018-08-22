# encoding=utf-8
from deal_words.calculate_frequency_in_dict import calculate_words_dict_frequency
from deal_words.find_new_words_context import find_context
from deal_words.load_jieba_dict import load_jieba_frequency
from deal_words.load_jieba_dict import load_jieba_words
import jieba
import jieba.posseg as psg

class deal_new_words_for_dict(object):
    def __init__(self, newwords=list(), spans=list(), jieba_dict_path = (jieba.get_abs_path_dict(),u'')):
        """
        :param newwords: 新词数组
        :param spans:处理后的源数据
        """
        self.newwords = newwords
        self.spans = spans
        self.jieba_dict_path = jieba_dict_path
        self.new_words = []
        self.frequency = dict()
        self.new_words_dic_frequency = dict()
        self.context_dict = dict()

    def deal(self,(NR_Preffix,NR_Suffix), findContext = False):

        for word in self.newwords:
            self.new_words.append(word[0].encode('utf-8'))
            self.frequency[word[0].encode('utf-8')] = word[1]

        freq_dict = load_jieba_frequency(self.jieba_dict_path)
        word_dict = load_jieba_words(self.jieba_dict_path)

        index = 0
        context = ' '
        while len(self.new_words) > index:

            new_word = self.new_words[index]
            freq = calculate_words_dict_frequency(new_word, self.frequency[new_word], freq_dict,word_dict)
            if findContext:
                context = find_context(self.spans, new_word,(NR_Preffix,NR_Suffix))
            if freq == -1 or context=='':
                self.new_words.remove(new_word)
                continue
            index += 1
            self.new_words_dic_frequency[new_word] = freq
            self.context_dict[new_word] = context

