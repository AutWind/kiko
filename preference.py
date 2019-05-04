from recv2 import getTop10
from wordsAnalysis import getAllUserID, getKeyWordsById
from pymongo import MongoClient

# mongo
client = MongoClient('47.107.130.215', 27017)
db = client['local']
collection = db['userPreference']


def getUsersByPreference(preference):
    users = []
    for user in collection.find({'pref': preference}, {'userID': 1}):
        users.append(user['userID'])
    return users


def getPreferenceById(Id):
    return collection.find({"userID": Id}).next()['pref']


# 已处理的用户数量
def getAllCount():
    count = 0
    for line in open('config/preferenceCount.txt'):
        count = int(line)
    return count


# 处理完一批后修正数量
def resetAllCount(nums):
    with open('config/preferenceCount.txt', 'w') as f:
        f.write(str(nums))


if __name__ == '__main__':

    # 起始索引
    beginNum = getAllCount()

    # 获取微博ID
    ids = getAllUserID()

    # 结束索引
    endNum = len(ids)
    for index, _id in enumerate(ids[beginNum:endNum]):
        words = getKeyWordsById(_id)
        pref = getTop10(words, 'work2vec/bag.txt')
        collection.insert_one({'userID': _id, 'pref': pref})
        resetAllCount(beginNum+1+index)
        print("{} / {}".format(beginNum+1+index, endNum))
