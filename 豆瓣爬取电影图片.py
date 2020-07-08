from selenium import webdriver
browser = webdriver.Chrome()
import pandas as pd
item_df = pd.read_csv('ml-100k/ml-100k/u.item', sep='|', encoding='ISO-8859-1', header=None, names=['mid','mtitle']+[x for x in range(22)])
item_df = item_df.astype(str)
import requests
import time
import random

for i in item_df.mtitle.values.tolist()[287:537]:

    browser.get('https://www.douban.com/search?q='+i+'')
    try:
        url = browser.find_element_by_xpath('//*[@id="content"]/div/div[1]/div[3]/div[2]/div/div[1]/a/img')
        resposne = requests.get(url.get_attribute('src'))
        with open('static/images/'+i+'.jpg','wb') as f:
            f.write(resposne.content)
            f.close()
        print('图片',i,'.jpg保存成功')
        time.sleep(random.randint(3,5))
    except:
        time.sleep(random.randint(3,5))
    # break
    # print(url)