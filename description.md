#题目描述
[原文点这里](http://www.kddcup2012.org/c/kddcup2012-track1)。

##背景
capturing users’ interests and accordingly serving them with potentially interesting items (e.g. news, games, advertisements, products), is a fundamental and crucial feature social networking websites like Tencent Weibo. 

##任务描述
The prediction task involves predicting whether or not a user will follow an item that has been recommended to the user. Items can be persons, organizations, or groups and will be defined more thoroughly below. 

##数据集
The dataset represents a sampled snapshot of Tencent Weibo users’ preferences for various items –– the recommendation of items to users and the history of users’ ‘following’ history. It is of a larger scale compared to other publicly available datasets ever released. Also it provides richer information in multiple domains such as user profiles, social graph, item category, which may hopefully evoke deeply thoughtful ideas and methodology.

The users in the dataset, numbered in millions, are provided with rich information (demographics, profile keywords, follow history, etc.) for generating a good prediction model. To protect the privacy of the users, the IDs of both the users and the recommended items are anonymized as random numbers such that no identification is revealed. Furthermore, their information, when in Chinese, will be encoded as random strings or numbers, thus no contestant who understands Chinese would get advantages. Timestamps for recommendation are given for performing session analysis.

###Item
An item is a specific user in Tencent Weibo, which can be a person, an organization, or a group, that was selected and recommended to other users. Typically, celebrities, famous organizations, or some well-known groups were selected to form the ‘items set’ for recommendation. The size of this is about 6K items in the dataset. 

Items are organized in categories; each category belongs to another category, and all together they form a hierarchy. For example, an item, a vip user Dr. Kaifu LEE, represented as `science-and-technology.internet.mobile`

We can see that categories in different levels are separated by a dot ‘.’, and the category information about an item can help enhance your model prediction. For example, if a user Peter follows kaifulee, he may be interested in the other items of the category that kaifulee belongs to, and might also be interested in the items of the parent category of kaifulee’s category.

###Tweet
a “tweet” is the action of a user posting a message to the microblog system, or the posted message itself. So when one user is “tweeting“, his/her followers will see the “tweet”.

###Retweet
a user can repost a tweet and append some comments (or do nothing), to share it with more people (my followers).

###Comment
a user can add some comments to a tweet. The contents of the comments  will not be automatically pushed to his/her followers as ‘tweeting’ or ‘retweeting’,but will appear at the ‘comment history’ of the commented tweet.

###Followee/follower
If User B is followed by User A, B is a followee to A, and A is a follower to B.

#数据文件
数据集可以在[这里下载](http://pan.baidu.com/s/1kcNwE)

##训练与测试数据
* `rec_log_train.txt`: 训练数据集文件
* `rec_log_test.txt`: 测试数据集文件。没有 `UserId` 和 `ItemId` 均相同的重复记录

他俩格式相同，都是：

|  UserId |  ItemId | Result | Unix-timestamp |
|---------|---------|--------|----------------|
| 2088948 | 1760350 |     -1 |     1318348785 |

* `Result`: 取值为 `1`、`-1` 或 `0`。`1` 表示用户 `UserId` 接收了推荐的 `ItemId` 并且 follow 了它，`-1` 则相反。`0` 只出现在 `rec_log_test.txt` 中，表示未知，需要进行预测。
    
##字段的详细信息
###user_profile.txt
| UserId | Year-of-birth | Gender | Number-of-tweet |           Tag-Ids           |
|--------|---------------|--------|-----------------|-----------------------------|
| 100044 |          1899 |      1 |               5 | 831;55;198;8;450;7;39;5;111 |
| 100054 |          1987 |      2 |               6 | 0                           |

* `Year-of-birth`: 该用户是哪一年出生的
* `Gender`: 值为 `0`、`1` 或 `2`，表示“未知”、“男”或“女”
* `Number-of-tweet`: the amount of tweets the user has posted
* `Tag-Ids`: 格式为 `tag-id1;...;tag-idN`，每个 `tag-id` 代表用户的一个兴趣，`0` 表示该用户没有设置标签

###item.txt
|  ItemId | Item-Category |  Item-Keyword  |
|---------|---------------|----------------|
| 2012081 | 1.6.2.1       | 3824;6359      |
| 2263991 | 1.6.2.1       | 7931;5300;5273 |

* `Item-Category`: 格式为 `a.b.c.d`，其中 `a` 是 `b` 的父亲，以此类推
* `Item-Keyword`: 包含从用户或组织的资料中抽取的关键字，格式为 `id1;id2;…;idN`

###user_action.txt
记录了用户之间的 `@` 操作。

|  UserId | Action-Destination-UserId | Number-of-at-action | Number-of-retweet | Number-of-comment |
|---------|---------------------------|---------------------|-------------------|-------------------|
| 1000004 |                   1000004 |                   0 |                 3 |                 4 |
| 1000004 |                   1290320 |                   0 |                 3 |                 0 |

例如第二条记录的意思为，用户 `1000004` `@` 了用户 `1290320` 0 次，转推了他的微博 3 次，评论过他 0 次。

###user_sns.txt
记录了用户的 follow 历史。

| Follower-userid | Followee-userid |
|-----------------|-----------------|
|         1000002 |         1760423 |
|         1000002 |         1760426 |

###user_key_word.txt
包含从用户的 tweet/retweet/comment 中抽取的关键字。

|  UserId | Keywords |
|---------|----------|
| 1000001 | 92:1.0   |
| 1000002 | 112:1.0  |

* `Keywords`: 格式为 `kw1:weight1;kw2:weight2;…kw3:weight3`，关键字是从用户的 tweet/retweet/comment 中抽取的，权重越高表示用户对这个关键字越感兴趣。`Keywords` 的值域和 `Item-Keyword` 的值域一样

#评估方式 
Teams’ scores and ranks on the leaderboard are based on a metric calculated from the predicted results in submitted result file and the held out ground truth of a validation dataset whose instances were a fixed set sampled from the testing dataset in the beginning and, until the last day of the competition (June 1, 2012) by then the scores and associated ranks on leaderboard are based on the predicted results and that of the rest of the testing dataset. This entails that the top-3 ranked teams at the time when the competition ends are the winners. The log for forming the training dataset corresponds to earlier time than that of the testing dataset.

The evaluation metric is average precision.

##metric 的详细定义
Suppose there are m items in an ordered list is recommended to one user, who may click 1 or more or none of them to follow, then, by adapting the definition of average precision in [IR](http://en.wikipedia.org/wiki/Information_retrieval), the average precision at n for this user is

![Evaluation - KDD Cup 2012, Track 1 19-40.jpg](https://ooo.0o0.ooo/2015/10/13/561cedce3ef50.jpg "Evaluation - KDD Cup 2012, Track 1 19-40.jpg")

where if the denominator is zero, the result is set zero; P(k) means the precision at cut-off k in the item list, i.e., the ratio of number of clicked items up to the position k over the number k, and P(k) equals 0 when k -th item is not followed upon recommendation; n = 3 as this is the default number of items recommended to each user in our recommender system. For example,

1. If among the 5 items recommended to the user, the user clicked #1, #3, #4, then ap@3 = (1/1 + 2/3)/3 ≈ 0.56
2. If among the 4 items recommended to the user, the user clicked #1, #2, #4, then ap@3 = (1/1 + 2/2)/3 ≈ 0.67
3. If among the 3 items recommended to the user, the user clicked #1, #3, then ap@3 = (1/1 + 2/3)/2 ≈ 0.83

The average precision for N users at position n is the average of the average precision of each user, i.e.,

![Evaluation - KDD Cup 2012, Track 1 19-42.jpg](https://ooo.0o0.ooo/2015/10/13/561cee62beb42.jpg "Evaluation - KDD Cup 2012, Track 1 19-42.jpg")

which is exactly the metric for the result file that the teams submit for evaluation of their models.