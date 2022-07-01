
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
from selenium import webdriver
# 读取txt文件，请求页面－－>如果报错就下一个；没有报错就取值。最终加总即可
from selenium.webdriver import PhantomJS


def use_requests(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None




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
    f_string = string_item/1000
    return f_string
def readjsonfile(filename):
    with open(filename, 'r', encoding='utf-8') as fw:
        s = json.load(fw)
        return s

#

# 可以尝试第二种解析方式，更加容易做计算
# 净收入 d1距离最近，d5最远
# 对于脚本的符合太大！所以季度和年度数据暂时不加入板块

#
def parse_stock_note(html):
    selector = etree.HTML(html)
    netProfits = selector.xpath('//*[@id="CONTENTS_MAIN"]/div[7]/div/div/div[6]/div[2]/table/tbody/tr[5]/td/text()')
    f_netProfits = [unified_unit_jp_fromNikkei(x) for x in netProfits]
    return f_netProfits
















def writeinto_detail(filename,data):
    with open(filename,"a",newline="",encoding="utf-8") as f:
        csv_out = csv.writer(f,delimiter=",")
        csv_out.writerow(data)

#


def readDatafile(filename):
    line_list = []
    with open(filename,"r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip("\n")
            line_list.append(line)
    return line_list





if __name__ == '__main__':
    resultjson = readjsonfile("nikki225_nikkei_info.json")
    _table_title = ["code","industry_info", "firstone_3",  "firstone_2","firstone_1","firstone",]
    writeinto_detail("nikki225_quarter.tsv", _table_title)
    for item in resultjson:
        code = item["code"]

        nikkei_url = "https://www.nikkei.com/nkd/company/kessan-q/?scode={0}&ba=1".format(code)
        industry_info = item["industry_info"]
        html = use_requests(nikkei_url)
        result =parse_stock_note(html)
        f_result = [code]+[industry_info]+result
        writeinto_detail("nikki225_quarter.tsv", f_result)
        print(f_result)





