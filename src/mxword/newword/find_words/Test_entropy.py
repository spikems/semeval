#encoding=utf-8
from New_Version_20140725.find_words.generate_suffix_dict import generate_right_suffix_dict,generate_left_suffix_dict
from New_Version_20140725.find_words.calculate_entropy import calculate_right_entropy,calculate_left_entropy

slist = [u'吃 葡萄 不 吐 葡萄 皮',
         u'不 吃 葡萄 倒 吐 葡萄 皮']

tuple1 = generate_right_suffix_dict(slist)
right_suffix_dict = tuple1[0]
total_words_count = tuple1[1]
left_suffix_dict = generate_left_suffix_dict(slist)
unknown_words = calculate_right_entropy(right_suffix_dict,3) #{}
calculate_left_entropy(left_suffix_dict,unknown_words)
# for word in unknown_words.keys:
#     print  word,':[',unknown_words[word][0],',',unknown_words[word][1],',',unknown_words[word][2],',',unknown_words[word][3],']'


# print total_words_count
# print_suffix_dict(right_suffix_dict)
# print
# print
# print_suffix_dict(left_suffix_dict)