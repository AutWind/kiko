import json
from jieba import analyse
import numpy as np
import pandas as pd
from pymongo import MongoClient
from apiv2 import *

# mongo
client = MongoClient('47.107.130.215', 27017)
db = client['local']
collection = db['userKeyWords']


def getAllWords():
    allWords = []
    for words in collection.find({}, {"_id": 0}):
        allWords.append(words['words'])
    return allWords


def getAllUserID():
    ids = []
    for ID in collection.find({}, {"userID": 1}):
        ids.append(ID['userID'])
    return ids


def getIDByName(name):
    return collection.find({"name": name})


def getNameByID(Id):
    return collection.find({"userID": Id})


def getKeyWordsById(Id):
    return collection.find({"userID": Id}).next()['words']


# 提取带有权重的关键字
def getRecordWithWeight(weibo):
    record = {}
    for content in weibo['tweet']:
        sentense = content['content']
        words = analyse.textrank(sentense, withWeight=True, allowPOS=('ns', 'n', 'vn', 'an', 'nr', 'nt'))
        for word in words:
            word, weight = word
            if word in record:
                record[word][0] += weight
                record[word][1] += 1
            else:
                record[word] = [0, 0]
                record[word][0] = weight
                record[word][1] = 1
    return record, len(weibo['tweet'])


# 对关键字排序
def recordSort(record):
    if len(record) == 0: return[]
    values = np.array(list(record.values()))
    df = pd.DataFrame()
    df.insert(0, 0, record.keys())
    df.insert(1, 1, values[:, 0])
    df.insert(2, 2, values[:, 1])
    df = df.sort_values(by=1, ascending=False)
    df = df.sort_values(by=2, ascending=False)
    return df[0].tolist()


# 删除字母和数字
def removeNumAndEngStopWords(words):
    newWords = []
    for word in words:
        if not (word.isdigit() or word.encode('UTF-8').isalpha() or word.encode('UTF-8').isalnum()):
            newWords.append(word)
    return newWords


# 获取一名微博用户对应的关键字列表
def getKeyWords(weibo, key_num=20):
    record, nums = getRecordWithWeight(weibo)
    words = recordSort(record)
    return weibo['_id'], weibo['nick_name'], removeNumAndEngStopWords(words)[:key_num], nums


# 已处理的微博数量
def getWeiboCount():
    count = 0
    for line in open('config/weiboCount.txt'):
        count = int(line)
    return count


# 处理完一批后修正微博数量
def resetWeiboCount(nums):
    with open('config/weiboCount.txt', 'w') as f:
        f.write(str(nums))


# 已处理的用户数量
def getAllCount():
    count = 0
    for line in open('config/wordsCount.txt'):
        count = int(line)
    return count


# 处理完一批后修正数量
def resetAllCount(nums):
    with open('config/wordsCount.txt', 'w') as f:
        f.write(str(nums))


if __name__ == '__main__':

    # 加载停用词
    analyse.set_stop_words('config/stopWords.txt')

    # 起始索引
    beginNum = getAllCount()

    # 获取微博ID
    ids = json.loads(getAllIdJson())

    # 结束索引
    endNum = len(ids)

    for index, _id in enumerate(ids[beginNum:endNum]):
        weibo = json.loads(getAllByIdJson(_id))
        if 'nick_name' not in weibo: continue
        ID, name, vector, nums = getKeyWords(weibo)
        weiboNum = getWeiboCount()
        if len(vector) > 0:
            collection.insert_one({'userID': ID, 'name': name, 'words': vector})
        resetWeiboCount(weiboNum+nums)
        resetAllCount(beginNum+1+index)
        print("{} / {}, {}".format(beginNum+1+index, endNum, weiboNum+nums))


