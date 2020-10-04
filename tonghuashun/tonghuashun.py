from fake_useragent import UserAgent
import requests
from lxml import etree
import pymongo
import time

# 数据存储
def saveMongo(datas):
    client = pymongo.MongoClient('127.0.0.1',27017)
    db = client['tonghuashun']['stock']
    db.insert_many(datas)
    client.close()


# url数据解析
def getData(e):
    datas = []
    i = 1

    while True:
        information = e.xpath('//tbody/tr[{}]/td/text()'.format(i))
        if information==[]:
            return datas
        codeName = e.xpath('//tbody/tr[{}]/td/a/text()'.format(i))

        item = {
            'number': information[0],  # 序号
            'code': codeName[0],  # 代码
            'name': codeName[1],  # 名称
            'current_price': information[1],  # 现价
            'quote_change( %)': information[2],  # 涨跌幅( %)
            'ups_and_downs': information[3],  # 涨跌
            'rate_of_increase( %)': information[4],  # 涨速( %)
            'change_hands( %)': information[5],  # 换手( %)
            'quantity_ratio': information[6],  # 量比
            'amplitude( %)': information[7],  # 振幅( %)
            'turnover': information[8],  # 成交额
            'qutstanding_shares': information[9],  # 流通股
            'circulation_market_value': information[10],  # 流通市值
            'ratio': information[11],  # 市盈率
        }
        datas.append(item)
        i += 1


if __name__ == '__main__':
    start = time.time()
    print('开始爬取...')
    i = 1
    while True:
        url= 'http://q.10jqka.com.cn/index/index/board/all/field/zdf/' \
          'order/desc/page/{}/ajax/1/'.format(i)
        res = requests.get(url,headers={'User-Agent': UserAgent().random}).text
        e = etree.HTML(res)
        page = e.xpath('//span[@class="page_info"]/text()')[0].split('/')
        if int(page[0])<=int(page[1]):
            saveMongo(getData(e))
            print('第%s页爬取完毕...'%i)
            i += 1
        else:
            end = time.time()
            print('本次爬取结束,总用时：%s'%(end-start))
            break







