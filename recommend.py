from wordsAnalysis import getAllWords
from gensim.models import word2vec
import gensim
import logging
import synonyms
import re
import jieba_fast
import jieba_fast.analyse
import codecs
from sklearn.cluster import KMeans
from sklearn.externals import joblib
import numpy
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

save_model_name = 'Cut.model'  #训练后的模型文件

def write_file(filename):
    '''
    这个函数是将前端传递给我们的二维关键词数组模型写入到文件中
    :param filename:
    :return:
    '''
    all_word = ''
    words = getAllWords()
    for i in words:
        for word in i:
            all_word = all_word + ' '+word
    with open(filename,'w') as f:
        f.write(all_word)


def model_train(train_file_name, save_model_file):  # model_file_name为训练语料的路径,save_model为保存模型名
    '''
    这个函数的作用是 加载 train_file_name 里的语料 训练之后将模型装载到save_model_file里面
    :param train_file_name: 需要进行训练的语料
    :param save_model_file: 需要进行保存的模型文件名
    :return:
    '''
    # 模型训练，生成词向量

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    sentences = word2vec.Text8Corpus(train_file_name)  # 加载语料
    model = gensim.models.Word2Vec(sentences, size=200,workers=8)  # 训练skip-gram模型; 默认window=5
    model.save(save_model_file)
    model.wv.save_word2vec_format(save_model_name + ".bin", binary=True)   # 以二进制类型保存模型以便重用


def remove(inputfile,outputfile):
    '''
    将带有特殊字符的文件标准化  该文件只实现了去除逗号并替换为空格
    :param inputfile:  输入文件名
    :param outputfile:   输出文件名
    :return: none
    '''

    with open(inputfile,'r',encoding='utf8') as f:
        text = f.read()
        str_out = ''.join(text).replace(',',' ')  # 去掉标点符号
        with open(outputfile,'w',encoding='utf8') as f2:
            f2.write(str_out)


def getTop10(Allwords,Allbag_file):
    '''

    :param Allwords:    用户的二维关键字数组
    :param Allbag_file: 商品类别文件
    :return: 前十个关键词类别
    '''
    user_words = Allwords
    all_bag = []
    with open(Allbag_file,'r') as f:
        text = f.read()
        all_bag = text.split(',')

    bag_num = dict()
    bag_len = len(all_bag)
    for i in range(bag_len):
        num = 0
        for word in user_words:
            num = num + synonyms.compare(word,all_bag[i])/bag_len
        bag_num[all_bag[i]] = num

    test_dict = sorted(bag_num.items(), key=lambda e: e[1], reverse=True)[:10]

    re_list = []
    for one in test_dict:
        re_list.append(one[0])
    return re_list











if __name__ == '__main__':
    #write_file('words.txt')
    #model_train('work2vec/wiki_simple_fenci_re.txt','wiki.model')
    # 加载训练好的模型文件
    # model = word2vec.Word2Vec.load(save_model_name)
    words = ['篮球','足球','化妆品']
    result = getTop10(words,'work2vec/bag.txt')
    print(result)

