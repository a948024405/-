import os, io, collections
import pandas as pd
from surprise import Dataset, KNNBaseline, SVD, accuracy, Reader
from surprise.model_selection import cross_validate, train_test_split
from sqlalchemy import create_engine
from mysqlConfig import *

engine = create_engine("mysql+pymysql://{}:{}@{}/{}?charset={}".format(username, password, '127.0.0.1:3306', database,'utf8'))
con = engine.connect()#创建连接
# 协同过滤方法

# 载入movielens-100k数据集，一个经典的公开推荐系统数据集，有选项提示是否下载。
# data = Dataset.load_builtin('ml-100k')
# file_path = 'ml-100k/ml-100k/u.data'
reader = Reader(line_format='user item rating', sep='\t')
sql_data = 'select * from data_df'
sql_item = 'select * from item_df'
data3 = pd.read_sql(sql_data,con=con)
data = Dataset.load_from_df(data3[['user','item','rating']],reader=reader)
data_df = pd.read_sql(sql_data,con=con)
item_df = pd.read_sql(sql_item,con=con)
# 每列都转换为字符串类型
data_df = data_df.astype(str)
item_df = item_df.astype(str)
# 电影id到电影标题的映射
item_dict = { item_df.loc[x, 'mid']: item_df.loc[x, 'mtitle'] for x in range(len(item_df)) }

#基于用户的协同过滤算法：
# 使用协同过滤算法时的相似性度量配置
# user-based
user_based_sim_option = {'name': 'pearson_baseline', 'user_based': True}
# item-based
item_based_sim_option = {'name': 'pearson_baseline', 'user_based': False}

# 为用户推荐n部电影，基于用户的协同过滤算法，先获取10个相似度最高的用户，把这些用户评分高的电影加入推荐列表。
def get_similar_users_recommendations(uid, n=10):
    # 获取训练集，这里取数据集全部数据
    trainset = data.build_full_trainset()
#     print(trainset.ur)
    # 考虑基线评级的协同过滤算法
    algo = KNNBaseline(sim_option = user_based_sim_option)
    # 拟合训练集
    algo.fit(trainset)

    # 使用get_neighbors方法得到10个最相似的用户
    neighbors = algo.get_neighbors(int(uid), k=10)
    neighbors_uid = ( algo.trainset.to_raw_uid(x) for x in neighbors )

    recommendations = set()
    #把评分为5的电影加入推荐列表
    for user in neighbors_uid:
        if len(recommendations) > n:
            break
        item = data_df[data_df['user']==str(user)]
        item = item[item['rating']=='5']['item']
        for i in item:
            recommendations.add(item_dict[i])
#     print('\nrecommendations for user %d:')%inner_id
    for i, j in enumerate(list(recommendations)):
        if i >= 10:
            break
        print(j)
#给id为1的用户推荐10部电影：
get_similar_users_recommendations('1', 10)