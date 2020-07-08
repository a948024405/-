import pymysql
import pandas as pd
from sqlalchemy import create_engine
from mysqlConfig import *

#创建数据库及表
db = pymysql.connect(host='localhost',
                     port = 3306,
                    user = username,
                    password = password,
                    charset = 'utf8')


cursor = db.cursor()
cursor.execute('CREATE DATABASE if not exists '+database+'  DEFAULT CHARACTER SET utf8;')
db.close()


engine = create_engine("mysql+pymysql://{}:{}@{}/{}?charset={}".format(username, password, '127.0.0.1:3306', database,'utf8'))
con = engine.connect()#创建连接
data_df = pd.read_csv('ml-100k/ml-100k/u.data', sep='\t', header=None, names=['user','item','rating','timestamp'])
item_df = pd.read_csv('ml-100k/ml-100k/u.item', sep='|', encoding='ISO-8859-1', header=None, names=['mid','mtitle']+[x for x in range(22)])
# 每列都转换为字符串类型
data_df = data_df.astype(str)
item_df = item_df.astype(str)
data_df.to_sql(name='data_df', con=con, if_exists='append', index=False)

item_df.to_sql(name='item_df', con=con, if_exists='append', index=False)

print('数据库储存成功')