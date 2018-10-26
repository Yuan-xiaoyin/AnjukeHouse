import requests
from lxml import etree
import re
import pymongo
from settings import *
from multiprocessing import Pool
import time
import pandas as pd

class Crawl():
    # 初始化函数
    def __init__(self,MONGO_URL,MONGO_DB):
        self.base_url='https://chengdu.anjuke.com/sale/{}/p{}/'
        self.headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'}
        self.mongo_url=MONGO_URL
        self.mongo_db=MONGO_DB
    # 获取页面
    def get_page(self,url):
        try:
            response=requests.get(url=url,headers=self.headers)
            if response.status_code==STATUS_CODE:
                html=response.text
                return html
        except:
            print('页面加载错误:',url)
    def parse_page(self,html):
        house_list=[]
        html_text=etree.HTML(html)
        message_list=html_text.xpath('//div[@class="sale-left"]/ul/li')
        # print(message_list)
        for message in message_list:
        # address=html_text.xpath('//div[@class="sale-left"]/ul/li/div[2]/div[2]/span[2]/text()')
        # print(address)
            proportion=message.xpath('./div[2]/div[2]/span[2]/text()')[0]#房屋的面积
            price=message.xpath('./div[3]/span[1]/strong/text()')[0]#房屋的价格
            price_det=message.xpath('./div[3]/span[1]/text()')[0]#房屋价格的单位（万）
            unit_price=message.xpath('./div[3]/span[2]/text()')[0]#房屋的平均价格
            built_year=message.xpath('./div[2]/div[2]/span[4]/text()')[0]#哪年修建的房屋
            addresses=message.xpath('./div[2]/div[3]/span/text()')[0].strip()
            house_info=re.findall('^(.*?)\s\s.*\s(.*?)$',addresses,re.S)
            house_name=house_info[0][0]#小区名字
            house=house_info[0][1]
            house_area=re.findall('^(.*?)-',house)[0]#小区所属区域
            house_address=re.findall('-(.*?)$',house)[0]#小区地址
            # 方便输出为表单可以进行下面的拼接
            # b='{} {} {} {} {} {} {}'
            # house_message=b.format(house_area,house_name,house_address,proportion,price+price_det,unit_price,built_year)
            # print(house_message)
            house_message={
                "区域":house_area,
                "小区名称":house_name,
                "小区地址":house_address,
                "房屋面积":proportion,
                "房屋总价":price+price_det,
                "房屋均价":unit_price,
                "修建年份":built_year
            }
            if house_message:
                house_list.append(dict(house_message))
        return house_list
    def save_to_mongo(self,house_list):
        # 连接数据库
        client=pymongo.MongoClient(self.mongo_url)
        db=client[self.mongo_db]
        if db['anjuku'].insert(house_list):
            print('插入到Mongo数据库成功:',house_list)
        else:
            print('插入数据库失败:',house_list)
    #   保存为csv文件，当然这里可以有很多种方式，我这里为了学习pandas就用了pandas来保存
    def save_to_csv(self,house_list):
        name = ["区域", "小区名称", "小区地址", "房屋面积", "房屋总价", "房屋均价", "修建年份"]
        # 创建对象
        test = pd.DataFrame(columns=name, data=house_list)
        # 要添加一个mode属性，a表示追加写入的方式
        test.to_csv('D:/Anjuke.csv',mode='a')
        print('插入成功:', house_list)
    def main(self,pages):
        try:
            for area in AREA_LIST:
                for page in pages:
                    # 构造完整的url
                    url=self.base_url.format(area,page)
                    print(url)
                    time.sleep(1)
                    html=self.get_page(url)
                    if html:
                        house_list=self.parse_page(html)
                        if house_list:
                            self.save_to_mongo(house_list)
        except TypeError:
            print('页面下载完毕!')
if __name__=='__main__':
    spider=Crawl(MONGO_URL,MONGO_DB)
    # 在settings中配置了抓取的起始页和终止页，这里仅抓取了每个区的前十页
    try:
        pages=[str(pages) for pages in range(START_PAGE,END_PAGE)]
        pool=Pool(processes=4)
        pool.map(spider.main(pages),pages)
    except TypeError:
        print('页面下载完毕!')
        pass






