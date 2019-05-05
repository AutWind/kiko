import pymongo
import json

# 122.112.218.18
myclient = pymongo.MongoClient('mongodb://122.112.218.18:27017/')
sinaData1Base = myclient.SinaData
sinaData2Base = myclient.SinaData2
sinaData3Base = myclient.SinaData3


def getAllID():
    ids = []
    result = sinaData1Base.Information.find()
    for i in range(result.count()):
        ids.append(result.next()['_id'])
    result = sinaData2Base.Information.find()
    for i in range(result.count()):
        ids.append(result.next()['_id'])
    result = sinaData3Base.Information.find()
    for i in range(result.count()):
        ids.append(result.next()['_id'])
    return ids


def getUserInformationByID(user_id):
    database, result = sinaData1Base, sinaData1Base.Information.find_one({'_id': user_id})
    if result is None:
        database, result = sinaData2Base, sinaData2Base.Information.find_one({'_id': user_id})
        if result is None:
            database, result = sinaData3Base, sinaData3Base.Information.find_one({'_id': user_id})
    return database, result


def getFollowedByID(database, user_id):
    follows = []
    follows_cursor = database.Relationships.find({'fan_id': user_id})
    for i in range(follows_cursor.count()):
        follows.append(follows_cursor.next()['followed_id'])
    return follows


def getFansByID(database, user_id):
    fans = []
    fans_cursor = database.Relationships.find({'followed_id': user_id})
    for i in range(fans_cursor.count()):
        fans.append(fans_cursor.next()['fan_id'])
    return fans


def getTweetsByID(database, user_id):
    user_tweets = []
    tweets_cursor = database.Tweets.find({'user_id': user_id})
    for i in range(tweets_cursor.count()):
        user_tweets.append(tweets_cursor.next())
    return user_tweets


# https://weibo.com/2803301701/HsaGeeiI2
def getTweetComments(database, tweet_url):
    comm = []
    comment_cursor = database.Comments.find({'weibo_url': tweet_url})
    for i in range(comment_cursor.count()):
        comm.append(comment_cursor.next())
    return comm


def getAllByID(user_id):
    database, user_information = getUserInformationByID(user_id)
    # follows = getFollowedByID(user_id)
    fans = getFansByID(database, user_id)
    user_tweets = getTweetsByID(database, user_id)
    # user_information['watch'] = follows
    user_information['fans'] = fans
    user_information['tweet'] = user_tweets
    for tweet in user_tweets:
        tweet['comments'] = getTweetComments(database, tweet['weibo_url'])
    return user_information


# API1 : 获取所有爬取的用户ID
def getAllIdJson():
    return json.dumps(getAllID(), ensure_ascii=False)


# API2 : 通过用户ID获取有关该用户的所有信息
def getAllByIdJson(user_id):
    user_information = getAllByID(user_id)
    return json.dumps(user_information, ensure_ascii=False)


# API1 Json规整输出
def getAllIdStandardJson():
    return json.dumps(getAllID(), ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))


# API2 Json规整输出
def getAllByIdStandardJson(user_id):
    user_information = getAllByID(user_id)
    return json.dumps(user_information, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))


# 示例调用
if __name__ == '__main__':
    print(getAllIdJson())
    print(getAllIdStandardJson())
    print(getAllByIdJson('5508156613'))
    print(getAllByIdStandardJson('5508156613'))
    print("目前爬取用户数(有些用户微博正在爬取ing~):", len(getAllIdJson()))
    print("目前爬取微博数:", sinaData1Base.Tweets.find().count()+sinaData2Base.Tweets.find().count()+sinaData3Base.Tweets.find().count())
