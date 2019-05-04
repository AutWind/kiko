from relationShip import *
from snownlp import SnowNLP
from pymongo import MongoClient

# mongo
client = MongoClient('47.107.130.215', 27017)
db = client['local']
collection = db['userFriends']


def getFriendsById(Id):
    cursor = collection.find({"userID": Id})
    for data in cursor:
        return data['friends']
    return ''


def getComments(userID):
    return getRelationShipByUserID(userID)['comments']


def generateFriends(user, comments):
    friends = {}
    for comment in comments:
        if comment['content'] == '':
            comment['content'] = ' '
        if comment['comment_user_id'] in friends:
            friends[comment['comment_user_id']] += (SnowNLP(comment['content']).sentiments * 2. - 1.)
        else:
            friends[comment['comment_user_id']] = (SnowNLP(comment['content']).sentiments * 2. - 1.)
    return {
        'userID': user,
        'friends': friends
    }


# 已处理的用户数量
def getAllCount():
    count = 0
    for line in open('config/friendsCount.txt'):
        count = int(line)
    return count


# 处理完一批后修正数量
def resetAllCount(nums):
    with open('config/friendsCount.txt', 'w') as f:
        f.write(str(nums))


if __name__ == '__main__':

    # 起始索引
    beginNum = getAllCount()

    # 获取微博ID
    ids = getAllRelationShipID()

    # 结束索引
    endNum = len(ids)

    for index, _id in enumerate(ids[beginNum:endNum]):
        friends = generateFriends(_id, getComments(_id))
        if len(friends['friends']) == 0:
            continue
        collection.insert_one(friends)
        resetAllCount(beginNum + 1 + index)
        print("{} / {}".format(beginNum + 1 + index, endNum))
