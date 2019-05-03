from apiv2 import *
from pymongo import MongoClient

# mongo
client = MongoClient('47.107.130.215', 27017)
db = client['local']
collection = db['userRelationShip']


# 已处理的用户数量
def getAllCount():
    count = 0
    for line in open('config/relationShipCount.txt'):
        count = int(line)
    return count


# 处理完一批后修正数量
def resetAllCount(nums):
    with open('config/relationShipCount.txt', 'w') as f:
        f.write(str(nums))


# 获取微博用户社交关系
def getRelationShip(weibo):
    owner = weibo['_id']
    fans = weibo['fans']
    tweets = weibo['tweet']
    comments = []
    for tweet in tweets:
        comment = tweet['comments']
        for c in comment:
            comments.append({'comment_user_id': c['comment_user_id'], 'content': c['content']})
    return {'owner': owner, 'fans': fans, 'comments': comments}


# 获取微博用户社交网络
def getUserNetwork(weibo):
    pass


if __name__ == '__main__':

    # 起始索引
    beginNum = getAllCount()

    # 获取微博ID
    ids = json.loads(getAllIdJson())

    # 结束索引
    endNum = len(ids)

    for index, _id in enumerate(ids[beginNum:endNum]):
        weibo = json.loads(getAllByIdJson(_id))
        collection.insert_one(getRelationShip(weibo))
        resetAllCount(beginNum+1+index)
        print("{} / {}".format(beginNum+1+index, endNum))
