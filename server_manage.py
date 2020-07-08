import io
import json
from mysqlConfig import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from flask import request, session
import flask
from flask import render_template
import pymysql
import random
import numpy as np
import  time
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']
app = flask.Flask(__name__)
app.secret_key='djskla'

engine = create_engine(
    "mysql+pymysql://{}:{}@{}/{}?charset={}".format(username, password, '127.0.0.1:3306', database, 'utf8'))
con = engine.connect()  # 创建连接

sql_data = 'select * from data_df'
sql_item = 'select * from item_df'
global data_df
data_df = pd.read_sql(sql_data,con=con)
item_df = pd.read_sql(sql_item,con=con)
# 每列都转换为字符串类型
data_df = data_df.astype(str)
item_df = item_df.astype(str)
item_dict = { item_df.loc[x, 'mid']: item_df.loc[x, 'mtitle'] for x in range(len(item_df)) }
best_item=[]
#基于统计的推荐算法,评分最高的前100个做随机推荐
data_df['rating'] = data_df['rating'].astype(int)
grouped = data_df.groupby('item').agg(np.mean)
grouped = grouped.sort_values(by='rating',ascending=False)
for i in grouped.index[:100]:
    best_item.append((i,item_dict[i],round(float(grouped[grouped.index==i].values.tolist()[0][0]),1),'../static/images/'+item_dict[i]+'.jpg'))
@app.route("/")
def index():
    random_best = []
    while 1 :
        if len(random_best) < 10:
            a = random.choice(best_item)
            if a in random_best:
                pass
            else:
                random_best.append(a)
        else:
            break
    print(random_best)
    return render_template('main2.html',random_best=random_best )
@app.route("/submit",methods=['GET','POST'])
def submit():
    # print('***********')
    id = request.args['id']
    rating = request.args['rat']
    stamp = round(time.time())
    global data_df
    s = pd.Series(['1700', id, rating, stamp], index=data_df.columns)
    data_df = data_df.append(s, ignore_index=True)
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True, port=8777)