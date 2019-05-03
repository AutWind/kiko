from langconv import *
import jieba
import synonyms
from process_wiki import remove_words

def diff_to_simple(input,output):
    '''
    将 输入文件中的繁体字转化为简体中文 并 写入文件中
    :param input:  繁体文字路径
    :param output: 简体文字路径
    :return:
    '''
    with open(input, 'r', encoding='utf-8') as f:
        with open(output, 'w', encoding='utf-8') as of:
            text = f.readlines()
            for oneline in text:
                for i in range(100):
                    text = text + oneline
                of.write(diff_to_simple(oneline))

def dts(sentence):
    sentence = Converter('zh-hans').convert(sentence)
    return sentence

def fenci(filename,outfilename):
    with open(filename,'r',encoding='utf-8') as f:
        with open(outfilename, 'w', encoding='utf-8') as of:
            text = f.readlines()
            for oneline in text:
                fenci = ' '.join(jieba.cut(oneline, cut_all=False))
                of.write(fenci)






if __name__ == '__main__':
    # filename = 'work2vec/wiki.txt'
    # out_put = 'work2vec/wiki_simple.txt'
    # diff_to_simple(filename,out_put)


    # 将普通的未处理的文本分词
    #fenci('work2vec/wiki_simple.txt','work2vec/wiki_simple_fenci.txt')
    # 将分好词的文本去除无用词
    #remove_words('work2vec/wiki_simple_fenci.txt','work2vec/wiki_simple_fenci_re.txt')

    # 测试近义词库 -- test 1 --
    a = synonyms.compare('知识改变命运','奋斗决定人生',seg=True)
    b = synonyms.compare('知识改变命运', '奋斗决定人生', seg=True)
    c = synonyms.compare('知识改变命运', '奋斗决定人生', seg=True)
    d = synonyms.compare('知识改变命运', '奋斗决定人生', seg=True)
    e = synonyms.compare('知识改变命运', '奋斗决定人生', seg=True)
    f = synonyms.compare('知识改变命运', '奋斗决定人生', seg=True)
    g = synonyms.compare('知识改变命运', '奋斗决定人生', seg=True)
    h = synonyms.compare('知识改变命运', '奋斗决定人生', seg=True)
    i = synonyms.compare('知识改变命运', '奋斗决定人生', seg=True)
    j = synonyms.compare('知识改变命运', '奋斗决定人生', seg=True)
    k = synonyms.compare('知识改变命运', '奋斗决定人生', seg=True)
    l = synonyms.compare('知识改变命运', '奋斗决定人生', seg=True)
    print(a,b,c,d,e,f,g,h,i,j,k,l)