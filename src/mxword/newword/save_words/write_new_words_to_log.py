#encoding=utf-8
from datetime import date
def write_to_log(new_words, new_words_dic_frequency, context_dict, file_words_count, result_file_path):
        """

        :param new_words: 新词列表
        :param new_words_dic_frequency: 新词-词频词典，此词频为待添加如词典的词频
        :param context_dict: 上下文词典
        :param file_words_count: 单个文件最多可写入的新词个数
        :param result_file_path: 新词结果文件
        新词结果文件的每行格式：新词 空格 词频 空格 n 空格 上下文
        """
        file_len = file_words_count-1
        for index,new_word in enumerate(new_words):
            if index%file_len == 0:
                result_file_name = result_file_path + date.today().strftime("%Y%m%d")+'0%d.log'%((index-index%file_len)/file_len)
                fobje = open(result_file_name, 'w')

                if new_words_dic_frequency[new_word] == 0:
                    continue

                fobje.writelines(new_word)
                fobje.writelines(" %d n "%(new_words_dic_frequency[new_word]))
                fobje.writelines(context_dict[new_word])
                fobje.writelines('\n')
                continue
            new_word=(new_words[index])
            if new_words_dic_frequency[new_word]==0:
                    continue
            # print "[", index, "] ", new_word, " ", new_words_dic_frequency[new_word],' ',context_dict[new_word]
            fobje.writelines(new_word)
            fobje.writelines(" %d n "%(new_words_dic_frequency[new_word]))
            fobje.writelines(context_dict[new_word])
            fobje.writelines('\n')
            if index % file_len == file_len:
                fobje.close()
