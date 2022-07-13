# -*- coding:utf-8 -*-
import datetime
import re
import time

import pymysql
import requests
from requests.exceptions import RequestException
import csv
from lxml import etree
import json
# 1 各大指数制作json文件,代码,板块 。。。
# 2 保证都有效。财务数据模型再整理!每3天做一次采集!
# 3 指数,也就是市场的整体收益状况就有一个足够的把握。这个是除了技术之外的最最核心的基金交易的依据。

from selenium import webdriver
import time

import pymysql
import requests
from lxml import etree

from sqlalchemy import create_engine
import pandas as pd
from pyecharts.charts import Line
from pyecharts import options as opts
from pyecharts.globals import ThemeType
driver = webdriver.Chrome()
def use_selenium_headless(url):
    # 为Chrome配置无头模式

    # 在启动浏览器时加入配置

    driver.get(url)
    html = driver.page_source
    return html


def unified_unit_us_fromSina(string_item):
    # result --->"亿"
    try:

        string_item = "".join(string_item.split(","))
        if "亿" in string_item:
            int_string_item= (10**8)*float(string_item.split("亿")[0])
        elif "万" in string_item:
            int_string_item =(10**4)* float(string_item.split("万")[0])
        f_string = int_string_item/10**8
        return f_string
    except:
        pass

def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='Trust',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
        f_ls = "%s," * (38)
        print(len(f_ls[:-1].split(",")))
        cursor.executemany('insert into nasdap100_NP_daily (Total_,Internet_,Consumer_,Software_Infrastructure_,Semiconductors_,Telecom_,Semiconductor_,Drug_,Entertainment_,Communication_,Beverages_Non_Alcoholic_,Software_Application_,Biotechnology_,Electronic_,Discount_,Staffing_,null_,Credit_,Information_,Pharmaceutical_,Specialty_,Confectioners_,Auto_,Railroads_,Restaurants_,Medical_,Apparel_,Packaged_,Computer_,Farm_,Diagnostics_,Industrial_,Consulting_,Real_,Utilities_Regulated_,Lodging_,Travel_,Airlines_) values ({0})'.format(f_ls[:-1]),content)
        connection.commit()
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError:
        pass

def unified_unit_jp_fromNikkei(string_item):
    # 単位：百万円  34,848
    # result --->"亿"
    string_item = float("".join("{0}".format(string_item).split(",")))
    f_string = string_item/100
    return f_string
def readjsonfile(filename):
    with open(filename, 'r', encoding='utf-8') as fw:
        s = json.load(fw)
        return s



# 可以尝试第二种解析方式，更加容易做计算
# 净收入 d1距离最近，d5最远
# 对于脚本的符合太大！所以季度和年度数据暂时不加入板块
def parse_stock_note(html):

    selector = etree.HTML(html)
    MarketValue = selector.xpath('//*[@id="quote_detail_wrap"]/table/tbody/tr[2]/td[3]/text()')
    f_MarketValue = ["".join(re.findall('市值:(.*?)亿', MarketValue[0].split()[0]))]
    NetAsserts = selector.xpath('/html/body/div[2]/div[7]/div[2]/table[2]/tbody/tr[31]/td[1]/text()')
    f_NetAsserts = [unified_unit_us_fromSina("".join(x.split())) for x in NetAsserts]

    return f_NetAsserts,f_MarketValue

def count_list_item(list_content):
    try:
        float_list = []
        for item in list_content:
            float_list.append(float(item))
        print(float_list)

        result = sum(float_list)
        return result
    except:
        pass


def writeinto_detail(filename,data):
    with open(filename,"a",newline="",encoding="utf-8") as f:
        csv_out = csv.writer(f,delimiter=",")
        csv_out.writerow(data)
def writeintoTSV_file(filename,data):
    with open(filename,'a', newline='\n', encoding="utf-8") as f_output:
        tsv_output = csv.writer(f_output, delimiter='\t')
        tsv_output.writerow(data)

#
if __name__ == '__main__':
    industry_infos = []

    resultjson = readjsonfile("nasdap100_infos.json")
    for item in resultjson:
        url_f = "https://quotes.sina.com.cn/usstock/hq/balance.php?s={0}".format(item["code"])

        html = use_selenium_headless(url_f)
        f_NetAsserts,f_MarketValue = parse_stock_note(html)
        print(f_NetAsserts,f_MarketValue)

        f_result = [item["code"]] + [item["industry_infos"]] + [item["sector_infos"]] + f_NetAsserts + f_MarketValue
        print(f_result)
        time.sleep(1)
        writeintoTSV_file("nasdap100_MV_NA.tsv", f_result)






