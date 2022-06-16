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


def use_selenium_headless(url):
    # 为Chrome配置无头模式

    # 在启动浏览器时加入配置
    driver = webdriver.Chrome()
    driver.get(url)
    html = driver.page_source
    driver.quit()
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
    netProfits = selector.xpath('/html/body/div[2]/div[7]/div[2]/table[2]/tbody/tr[17]/td/text()')
    f_netProfits = [unified_unit_us_fromSina("".join(x.split())) for x in netProfits]
    return f_netProfits





def writeinto_detail(filename,data):
    with open(filename,"a",newline="",encoding="utf-8") as f:
        csv_out = csv.writer(f,delimiter=",")
        csv_out.writerow(data)

#
if __name__ == '__main__':
    _table_title = ["code", "industry_infos","sector_infos", "firstone", "firstone_1", "firstone_2", "firstone_3", "firstone_4"]
    writeinto_detail("nasdap100_year.tsv", _table_title)
    resultjson = readjsonfile("nasdap100_infos.json")
    for item in resultjson:


        url_f = "https://quotes.sina.com.cn/usstock/hq/income.php?s={0}&t=quarter".format(item["code"])

        html = use_selenium_headless(url_f)
        content = parse_stock_note(html)
        stock_info = [item["code"],item["industry_infos"],item["sector_infos"]]
        result_list = stock_info+content
        print(result_list)
        writeinto_detail("nasdap100_year.tsv", result_list)



