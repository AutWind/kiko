from relationShip import *
import networkx as nx
from pymongo import MongoClient

# mongo
client = MongoClient('47.107.130.215', 27017)
db = client['local']
collection = db['userNetwork']


def getNetworkById(Id):
    cursor = collection.find({"userID": Id})
    for data in cursor:
        return data['statistics']
    return ''


def getMoreFans(fans):
    mf = []
    network = []
    for fan in fans:
        if fan in ids:
            newFans = getRelationShipByUserID(fan)['fans']
            for newFan in newFans:
                network.append([fan, newFan, 1])
            mf += newFans
    return list(set(mf)), network


def getUserNetwork(userID):
    user = getRelationShipByUserID(userID)
    owner = user['owner']
    fans = [owner]
    network = []
    count = -1
    while True:
        if count >= 200 or len(fans) == 0:
            break
        count += len(fans)
        fans, newNet = getMoreFans(fans)
        network += newNet
    return {
        'userID': userID,
        'network': network
    }


def getNetworkStatistics(network):
    userID = network['userID']
    G = nx.DiGraph()
    G.add_weighted_edges_from(network['network'])
    return {
        'ODC': nx.out_degree_centrality(G)[userID],
        'CC': nx.closeness_centrality(nx.Graph(G), u=userID),
        'BC': nx.betweenness_centrality(nx.Graph(G))[userID],
        'diameter': nx.diameter(nx.Graph(G))
    }


# 已处理的用户数量
def getAllCount():
    count = 0
    for line in open('config/networkCount.txt'):
        count = int(line)
    return count


# 处理完一批后修正数量
def resetAllCount(nums):
    with open('config/networkCount.txt', 'w') as f:
        f.write(str(nums))


if __name__ == '__main__':

    # 起始索引
    beginNum = getAllCount()

    # 获取微博ID
    ids = getAllRelationShipID()

    # 结束索引
    endNum = len(ids)

    for index, _id in enumerate(ids[beginNum:endNum]):
        network = getUserNetwork(_id)
        if len(network['network']) == 0:
            continue
        network['statistics'] = getNetworkStatistics(network)
        collection.insert_one(network)
        resetAllCount(beginNum + 1 + index)
        print("{} / {}".format(beginNum + 1 + index, endNum))
