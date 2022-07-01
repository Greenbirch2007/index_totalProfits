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


def use_requests(url):
    time.sleep(1)
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

def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='Trust',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
        f_ls = "%s," * (30)
        print(len(f_ls[:-1].split(",")))
        cursor.executemany('insert into nikki225_NP_daily (Total_,Electrical_equipment,Chemistry,service,machine,Bank,Food,trading_company,Pharmaceuticals,construction,Non_ferrous_metal,Automobile,Ceramic_industry,Railroad_bus,insurance,Retail_business,real_estate,communication,precision_equipment,Other_manufacturing,Securities,fiber,Steel,Other_finance,oil,Pulp_paper,Fisheries,Rubber,shipbuilding,Mining,Land_transportation) values ({0})'.format(f_ls[:-1]),content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError:
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



# 可以尝试第二种解析方式，更加容易做计算
# 净收入 d1距离最近，d5最远
# 对于脚本的符合太大！所以季度和年度数据暂时不加入板块
def parse_stock_note(html):

    selector = etree.HTML(html)
    netProfits = selector.xpath('//*[@id="CONTENTS_MAIN"]/div[7]/div/div/div[6]/div[2]/table/tbody/tr[5]/td/text()')
    f_netProfits = [unified_unit_jp_fromNikkei(x) for x in netProfits]
    return f_netProfits

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

#
if __name__ == '__main__':
    Electrical_equipment_ = []
    Chemistry_ = []
    service_ = []
    machine_ = []
    Bank_ = []
    Food_ = []
    trading_company_ = []
    Pharmaceuticals_ = []
    construction_ = []
    Non_ferrous_metal_ = []
    Automobile_ = []
    Ceramic_industry_ = []
    Railroad_bus_ = []
    insurance_ = []
    Retail_business_ = []
    real_estate_ = []
    communication_ = []
    precision_equipment_ = []
    Other_manufacturing_ = []
    Securities_ = []
    fiber_ = []
    Steel_ = []
    Other_finance_ = []
    oil_ = []
    Pulp_paper_ = []
    Fisheries_ = []
    Rubber_ = []
    shipbuilding_ = []
    Mining_ = []
    Land_transportation_ = []

    resultjson = readjsonfile("nikki225_nikkei_info.json")
    for item in resultjson:
        code = item["code"]

        nikkei_url = "https://www.nikkei.com/nkd/company/kessan-q/?scode={0}&ba=1".format(code)
        industry_info = item["industry_info"]

        html = use_requests(nikkei_url)
        result =parse_stock_note(html)
        print(result)
        if result == []:
            f_result = [0]
        else:
            f_result = result[-1] - result[-2]
        print(f_result)

        if item["industry_info"] =="電気機器":
            Electrical_equipment_.append(f_result)
        elif item["industry_info"] =="化学":
            Chemistry_.append(f_result)
        elif item["industry_info"] =="サービス":
            service_.append(f_result)
        elif item["industry_info"] =="機械":
            machine_.append(f_result)
        elif item["industry_info"] =="銀行":
            Bank_.append(f_result)

        elif item["industry_info"] =="食品":
            Food_.append(f_result)


        elif item["industry_info"] =="商社":
            trading_company_.append(f_result)
        elif item["industry_info"] =="医薬品":
            Pharmaceuticals_ .append(f_result)
        elif item["industry_info"] =="建設":
            construction_ .append(f_result)
        elif item["industry_info"] =="非鉄・金属":
            Non_ferrous_metal_.append(f_result)
        elif item["industry_info"] =="自動車":
            Automobile_.append(f_result)
        elif item["industry_info"] =="窯業":
            Ceramic_industry_.append(f_result)
        elif item["industry_info"] =="鉄道・バス":
            Railroad_bus_.append(f_result)
        elif item["industry_info"] =="保険":
            insurance_.append(f_result)
        elif item["industry_info"] =="小売業":
            Retail_business_.append(f_result)
        elif item["industry_info"] =="不動産":
            real_estate_ .append(f_result)
        elif item["industry_info"] =="通信":
            communication_.append(f_result)
        elif item["industry_info"] =="精密機器":
            precision_equipment_.append(f_result)
        elif item["industry_info"] =="その他製造":
            Other_manufacturing_.append(f_result)
        elif item["industry_info"] =="証券":
            Securities_.append(f_result)
        elif item["industry_info"] =="繊維":
            fiber_.append(f_result)
        elif item["industry_info"] =="鉄鋼":
            Steel_.append(f_result)
        elif item["industry_info"] =="その他金融":
            Other_finance_.append(f_result)
        elif item["industry_info"] =="石油":
            oil_.append(f_result)
        elif item["industry_info"] =="パルプ・紙":
            Pulp_paper_.append(f_result)
        elif item["industry_info"] =="水産":
            Fisheries_.append(f_result)
        elif item["industry_info"] =="ゴム":
            Rubber_.append(f_result)
        elif item["industry_info"] =="造船":
            shipbuilding_.append(f_result)
        elif item["industry_info"] =="鉱業":
            Mining_.append(f_result)
        elif item["industry_info"] =="陸運":
            Land_transportation_.append(f_result)



    Total_ = [count_list_item(Electrical_equipment_ ),count_list_item(Chemistry_ ),count_list_item(service_ ),count_list_item(machine_ ),count_list_item(Bank_ ),count_list_item(Food_ ),count_list_item(trading_company_ ),count_list_item(Pharmaceuticals_ ),count_list_item(construction_ ),count_list_item(Non_ferrous_metal_ ),count_list_item(Automobile_ ),count_list_item(Ceramic_industry_ ),count_list_item(Railroad_bus_ ),count_list_item(insurance_ ),count_list_item(Retail_business_ ),count_list_item(real_estate_ ),count_list_item(communication_ ),count_list_item(precision_equipment_ ),count_list_item(Other_manufacturing_ ),count_list_item(Securities_ ),count_list_item(fiber_ ),count_list_item(Steel_ ),count_list_item(Other_finance_ ),count_list_item(oil_ ),count_list_item(Pulp_paper_ ),count_list_item(Fisheries_ ),count_list_item(Rubber_ ),count_list_item(shipbuilding_ ),count_list_item(Mining_ ),count_list_item(Land_transportation_ )]

    Total_ = sum([x for x in Total_ if x !=None])
    f_tuple =(Total_,count_list_item(Electrical_equipment_ ),count_list_item(Chemistry_ ),count_list_item(service_ ),count_list_item(machine_ ),count_list_item(Bank_ ),count_list_item(Food_ ),count_list_item(trading_company_ ),count_list_item(Pharmaceuticals_ ),count_list_item(construction_ ),count_list_item(Non_ferrous_metal_ ),count_list_item(Automobile_ ),count_list_item(Ceramic_industry_ ),count_list_item(Railroad_bus_ ),count_list_item(insurance_ ),count_list_item(Retail_business_ ),count_list_item(real_estate_ ),count_list_item(communication_ ),count_list_item(precision_equipment_ ),count_list_item(Other_manufacturing_ ),count_list_item(Securities_ ),count_list_item(fiber_ ),count_list_item(Steel_ ),count_list_item(Other_finance_ ),count_list_item(oil_ ),count_list_item(Pulp_paper_ ),count_list_item(Fisheries_ ),count_list_item(Rubber_ ),count_list_item(shipbuilding_ ),count_list_item(Mining_ ),count_list_item(Land_transportation_ ))
    f_tuple_ = (0 if x == None else x for x in f_tuple)
    print(f_tuple)
    insertDB([f_tuple])

    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='Trust',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    engine_js_op = create_engine('mysql+pymysql://root:123456@localhost:3306/Trust')
    cursor = connection.cursor()
    Total_dt_sql = "select Total_ from nikki225_NP_daily;"
    Total_dt_= pd.read_sql_query(Total_dt_sql, engine_js_op)
    Total_dt_list = list(Total_dt_["Total_"])


    time_sql = "select  LastTime from nikki225_NP_daily;"
    time_num = pd.read_sql_query(time_sql, engine_js_op)
    LastTime_list = list(time_num["LastTime"])

    line = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width='1000px', height='300px'))
            .add_xaxis(LastTime_list)
            .add_yaxis("NP", Total_dt_list)
            .set_global_opts(title_opts=opts.TitleOpts(title="nikki225_NP_daily", subtitle="nikki225_NP_daily"),
                             datazoom_opts=opts.DataZoomOpts(is_show=True))
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )
    line.render('nikki225_NP_daily.html')
    line.render_notebook()

    connection.close()

#


# create table nikki225_NP_daily (id int not null primary key auto_increment,Total_  text,  Electrical_equipment text,Chemistry text,service text,machine text,Bank text,Food text,trading_company text,Pharmaceuticals text,construction text,Non_ferrous_metal text,Automobile text,Ceramic_industry text,Railroad_bus text,insurance text,Retail_business text,real_estate text,communication text,precision_equipment text,Other_manufacturing text,Securities text,fiber text,Steel text,Other_finance text,oil text,Pulp_paper text,Fisheries text,Rubber text,shipbuilding text,Mining text,Land_transportation text, LastTime timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP) engine=InnoDB  charset=utf8;
