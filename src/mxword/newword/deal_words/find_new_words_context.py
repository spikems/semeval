# coding=utf-8
import jieba.posseg as psg

def find_context(spans, new_word,(NR_Preffix,NR_Suffix)):
    """

    :param spans: 文本列表
    :param new_word: 新词
    :return: context :一条新词上下文
    """
    tmp_newword=list(psg.cut(new_word))
    if len(tmp_newword)==1 and tmp_newword[0].flag.startswith("nr"):
        return ""
    if new_word.endswith("某") or new_word.endswith("哥") or new_word.endswith("姐"):
        return ''

    context = '   '
    try_index=3
    for span in spans:
        for line in span:
            tmp_context=line.replace(' ','').encode('utf-8')
            if tmp_context.find(new_word) >= 0 and len(line) > 10 and len(line)<100:
                for pre in NR_Preffix:
                    if tmp_context.find(pre+new_word)>0:
                        return ''
                for suf in NR_Suffix:
                    if tmp_context.find(new_word+suf)>0:
                        return ''

                if try_index>0:
                    try_index-=1
                    continue
                else:
                    return line.replace(' ', '').encode('utf-8','ignore')
    return context
