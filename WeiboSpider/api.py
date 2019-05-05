import pymongo
import json

# 122.112.218.18
myclient = pymongo.MongoClient('mongodb://122.112.218.18:27017/')
sinaDataBase = myclient.Sina
comments = sinaDataBase.Comments
information = sinaDataBase.Information
relationships = sinaDataBase.Relationships
tweets = sinaDataBase.Tweets


def getAllID():
    result = information.find()
    ids = []
    for i in range(result.count()):
        ids.append(result.next()['_id'])
    return ids


def getUserInformationByID(user_id):
    return information.find_one({'_id': user_id})


def getFollowedByID(user_id):
    follows_cursor = relationships.find({'fan_id': user_id})
    follows = []
    for i in range(follows_cursor.count()):
        follows.append(follows_cursor.next()['followed_id'])
    return follows


def getFansByID(user_id):
    fans_cursor = relationships.find({'followed_id': user_id})
    fans = []
    for i in range(fans_cursor.count()):
        fans.append(fans_cursor.next()['fan_id'])
    return fans


def getTweetsByID(user_id):
    tweets_cursor = tweets.find({'user_id': user_id})
    user_tweets = []
    for i in range(tweets_cursor.count()):
        user_tweets.append(tweets_cursor.next())
    return user_tweets


# https://weibo.com/2803301701/HsaGeeiI2
def getTweetComments(tweet_url):
    comment_cursor = comments.find({'weibo_url': tweet_url})
    comm = []
    for i in range(comment_cursor.count()):
        comm.append(comment_cursor.next())
    return comm


def getAllByID(user_id):
    user_information = getUserInformationByID(user_id)
    follows = getFollowedByID(user_id)
    fans = getFansByID(user_id)
    user_tweets = getTweetsByID(user_id)
    user_information['watch'] = follows
    user_information['fans'] = fans
    user_information['tweet'] = user_tweets
    for tweet in user_tweets:
        tweet['comments'] = getTweetComments(tweet['weibo_url'])
    return user_information


# API1 : 获取所有爬取的用户ID
def getAllIdJson():
    return json.dumps(getAllID(), ensure_ascii=False)


# API2 : 通过用户ID获取有关该用户的所有信息
def getAllByIdJson(user_id):
    user_information = getAllByID(user_id)
    return json.dumps(user_information, ensure_ascii=False)


# 示例调用
if __name__ == '__main__':
    # demo id 2803301701
    print(getAllIdJson())
    print(getAllByIdJson('2803301701'))

    result = tweets.find()
    print(result.count())
    # print(json.dumps(user_information, sort_keys=True, indent=4, ensure_ascii=False, separators=(',', ': ')))
