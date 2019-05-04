import pandas as pd
from apiv2 import *
from wordsAnalysis import getNameByID, getIDByName, getKeyWordsById
from preference import getPreferenceById, getUsersByPreference
from network import getNetworkById
from friends import getFriendsById

weiboIds = json.loads(getAllIdJson())


def getWeiboById(userID):
    if userID in weiboIds:
        return json.loads(getAllByIdJson(userID))
    return {'错误': '相关微博未收录'}


def getIDByCursor(name):
    cursor = getIDByName(name)
    for data in cursor:
        return data['userID']
    return ''


def getNameByCursor(Id):
    cursor = getNameByID(Id)
    for data in cursor:
        return data['name']
    return ''


def recommendOneById(Id):
    return {
        'userName': getNameByCursor(Id),
        'preference': getPreferenceById(Id)
    }


def recommendUser(goods):
    df = pd.DataFrame()
    users = getUsersByPreference(goods)
    values = []
    for net in getNetworkstats(users):
        _, stats = net
        if stats == '':
            values.append(0.)
        else:
            values.append((stats['ODC'] + stats['CC'] + stats['BC']) * stats['diameter'])
    df.insert(0, 0, users)
    df.insert(1, 1, values)
    return df.sort_values(by=1, ascending=False)[0].tolist()


def getNetworkstats(users):
    nets = []
    for user in users:
        nets.append([user, getNetworkById(user)])
    return nets


# API 1  总体统计数据
# 已处理的数据量
# 比数据库中数据量大
# 有一部分处理数据被过滤
def allCollectionStats():
    stt = {}
    for line in open('config/weiboCount.txt'):
        stt['weiboCount'] = int(line)
    for line in open('config/wordsCount.txt'):
        stt['wordsCount'] = int(line)
    for line in open('config/preferenceCount.txt'):
        stt['preferenceCount'] = int(line)
    for line in open('config/relationShipCount.txt'):
        stt['relationShipCount'] = int(line)
    for line in open('config/networkCount.txt'):
        stt['networkCount'] = int(line)
    for line in open('config/friendsCount.txt'):
        stt['friendsCount'] = int(line)
    return stt


# API 2  根据用户名查找微博
def getWeiboByName(name):
    return getWeiboById(getIDByCursor(name))


# API 3  根据用户名查找统计信息
def getOneStatistics(name):
    userID = getIDByCursor(name)
    if userID in weiboIds:
        stt = {}
        stt['keyWords'] = getKeyWordsById(userID)
        stt['preference'] = getPreferenceById(userID)
        stt['network'] = getNetworkById(userID)
        stt['friends'] = getFriendsById(userID)
        return stt
    return ''


# API 4  根据用户名为用户及用户的好友推荐商品
def recommendAll(name):
    userID = getIDByCursor(name)
    friends = getFriendsById(userID)
    users = [userID]
    for friend in list(friends.keys()):
        if friend in weiboIds and friends[friend] > 0.2:
            users.append(friend)
    result = []
    for user in users:
        result.append(recommendOneById(user))
    return result


# API 5  根据商品推荐用户
def recommendUserWithPreference(goods):
    users = recommendUser(goods)
    userList = []
    for user in users:
        userList.append({
            'name': getNameByCursor(user),
            'pref': getPreferenceById(user)
        })
    return userList


if __name__ == '__main__':
    allCollectionStats()
    getWeiboByName('三千剑姬')
    getOneStatistics('三千剑姬')
    recommendAll('三千剑姬')
    recommendUserWithPreference('西装')
