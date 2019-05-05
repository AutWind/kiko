# kiko
## 数据流向  
原始微博 -> 微博爬虫 -> MongoDB_1 -> 数据挖掘 -> MongoDB_2 -> Flask -> Web
## 快速开始 
>修改*WeiboSpider/setting.py*,启动爬虫  

>修改各文件头部*Pymongo*所指向的*MongoDB*实例  

>依次启动*wordsAnalysis.py*,*preference.py*,*relationShip.py*,*network.py*,*friends.py*  

>启动*app.py*,访问*ip:5000*
## 快速使用  
1. __登陆__  
邮箱和账号硬编码在代码中，邮箱：123@qq.com，密码：123。
![Image text](https://github.com/aftercloud/kiko/blob/master/image/0.png)
2. __主页__  
显示*MongoDB*中文档的条目数，关键词数目是指用户偏好在数据库中的文档的数量，增量式更新。
![Image text](https://github.com/aftercloud/kiko/blob/master/image/1.png)
3. __原始微博__  
输入微博用户名，如果该用户的微博数据已被爬虫采集，显示采集到的原始数据，否者为空。
![Image text](https://github.com/aftercloud/kiko/blob/master/image/2.png)
4. __微博属性__  
将用户微博中提取到的关键字、计算出的偏好、社交网络属性可视化。  
由于爬虫策略及数据集规模，“好友”可能未收录在数据库中，因此只给出了其在数据库内部的编号。
![Image text](https://github.com/aftercloud/kiko/blob/master/image/3.png)
5. __推荐用户__  
根据选定的商品类别，推荐偏好中包含该类别的用户，按社交网络属性降序排列。
![Image text](https://github.com/aftercloud/kiko/blob/master/image/4.png)
6. __推荐商品__  
根据用户推荐其可能感兴趣的商品。  
进一步的，待数据集扩充后，系统会返回该用户好友的推荐信息。
![Image text](https://github.com/aftercloud/kiko/blob/master/image/5.png)
## 算法流程  
### 用户偏好
将微博用户视作一篇文档，从其所有微博中提取关键字，按计算出的权重取前20个。将代表用户的关键字和预先建立的偏好目录中的偏好项两两计算相似度，取相似度最高的10个偏好项作为用户的偏好。  
### 社交网络
以微博用户为根节点，以其粉丝列表为方向，以广度优先的方式建立该用户的社交网络，计算该网络中的相关属性。  
### 好友关系
对微博用户的微博中的评论计算情感极性，根据计算出的情感极性判定评论用户和微博用户的亲近程度，情感极性的范围为[-1., 1.]。  
## 第三方库  
|库名|说明|
|-|-|
|flask|后端|
|pymongo|MongoDB|
|scrapy|爬虫框架|
|jieba_fast|中文分词|
|synonyms|中文同义词|
|numpy|数组|
|pandas|数据组织|
|snownlp|中文情感分析|
|networkx|网络构建|
## 其他说明
>*app.py*中没有设置服务器，请根据使用需要（并发能力）自行设置

