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
    netProfits = selector.xpath('/html/body/div[2]/div[7]/div[2]/table[2]/tbody/tr[17]/td/text()')
    f_netProfits = [unified_unit_us_fromSina("".join(x.split())) for x in netProfits]
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
    industry_infos = []

    Internet_ = []
    Consumer_ = []
    Software_Infrastructure_ = []
    Semiconductors_ = []
    Telecom_ = []
    Semiconductor_ = []
    Drug_ = []
    Entertainment_ = []
    Communication_ = []
    Beverages_Non_Alcoholic_ = []
    Software_Application_ = []
    Biotechnology_ = []
    Electronic_ = []
    Discount_ = []
    Staffing_ = []
    null_ = []
    Credit_ = []
    Information_ = []
    Pharmaceutical_ = []
    Specialty_ = []
    Confectioners_ = []
    Auto_ = []
    Railroads_ = []
    Restaurants_ = []
    Medical_ = []
    Apparel_ = []
    Packaged_ = []
    Computer_ = []
    Farm_ = []
    Diagnostics_ = []
    Industrial_ = []
    Consulting_ = []
    Real_ = []
    Utilities_Regulated_ = []
    Lodging_ = []
    Travel_ = []
    Airlines_ = []

    _table_title = ["code", "industry_infos","sector_infos", "firstone", "firstone_1", "firstone_2", "firstone_3", "firstone_4"]
    resultjson = readjsonfile("nasdap100_infos.json")
    for item in resultjson:
        url_f = "https://quotes.sina.com.cn/usstock/hq/income.php?s={0}&t=quarter".format(item["code"])

        html = use_selenium_headless(url_f)
        content = parse_stock_note(html)
        if item["industry_infos"] =="Internet":
            Internet_.append(content[0])
        elif item["industry_infos"] =="Consumer":
            Consumer_.append(content[0])
        elif item["industry_infos"] =="Software—Infrastructure":
            Software_Infrastructure_.append(content[0])
        elif item["industry_infos"] =="Semiconductors":
            Semiconductors_.append(content[0])
        elif item["industry_infos"] =="Telecom":
            Telecom_.append(content[0])

        elif item["industry_infos"] =="Semiconductor":
            Semiconductor_.append(content[0])


        elif item["industry_infos"] =="Drug":
            Drug_.append(content[0])
        elif item["industry_infos"] =="Entertainment":
            Entertainment_.append(content[0])
        elif item["industry_infos"] =="Communication":
            Communication_.append(content[0])
        elif item["industry_infos"] =="Beverages—Non-Alcoholic":
            Beverages_Non_Alcoholic_.append(content[0])
        elif item["industry_infos"] =="Software—Application":
            Software_Application_.append(content[0])
        elif item["industry_infos"] =="Biotechnology":
            Biotechnology_.append(content[0])
        elif item["industry_infos"] =="Electronic":
            Electronic_.append(content[0])
        elif item["industry_infos"] =="Discount":
            Discount_.append(content[0])
        elif item["industry_infos"] =="Staffing":
            Staffing_.append(content[0])
        elif item["industry_infos"] =="null":
            null_.append(content[0])
        elif item["industry_infos"] =="Credit":
            Credit_.append(content[0])
        elif item["industry_infos"] =="Information":
            Information_.append(content[0])
        elif item["industry_infos"] =="Pharmaceutical":
            Pharmaceutical_.append(content[0])
        elif item["industry_infos"] =="Specialty":
            Specialty_.append(content[0])
        elif item["industry_infos"] =="Confectioners":
            Confectioners_.append(content[0])
        elif item["industry_infos"] =="Auto":
            Auto_.append(content[0])
        elif item["industry_infos"] =="Railroads":
            Railroads_.append(content[0])
        elif item["industry_infos"] =="Restaurants":
            Restaurants_.append(content[0])
        elif item["industry_infos"] =="Medical":
            Medical_.append(content[0])
        elif item["industry_infos"] =="Apparel":
            Apparel_.append(content[0])
        elif item["industry_infos"] =="Packaged":
            Packaged_.append(content[0])
        elif item["industry_infos"] =="Computer":
            Computer_.append(content[0])
        elif item["industry_infos"] =="Farm":
            Farm_.append(content[0])
        elif item["industry_infos"] =="Diagnostics":
            Diagnostics_.append(content[0])
        elif item["industry_infos"] =="Industrial":
            Industrial_.append(content[0])
        elif item["industry_infos"] =="Consulting":
            Consulting_.append(content[0])
        elif item["industry_infos"] =="Real":
            Real_.append(content[0])
        elif item["industry_infos"] =="Utilities—Regulated":
            Utilities_Regulated_.append(content[0])
        elif item["industry_infos"] =="Lodging":
            Lodging_.append(content[0])
        elif item["industry_infos"] =="Travel":
            Travel_.append(content[0])
        elif item["industry_infos"] =="Airlines":
            Airlines_.append(content[0])

    Total_ = [count_list_item(Internet_),count_list_item(Consumer_),count_list_item(Software_Infrastructure_),count_list_item(Semiconductors_),count_list_item(Telecom_),count_list_item(Semiconductor_),count_list_item(Drug_),count_list_item(Entertainment_),count_list_item(Communication_),count_list_item(Beverages_Non_Alcoholic_),count_list_item(Software_Application_),count_list_item(Biotechnology_),count_list_item(Electronic_),count_list_item(Discount_),count_list_item(Staffing_),count_list_item(null_),count_list_item(Credit_),count_list_item(Information_),count_list_item(Pharmaceutical_),count_list_item(Specialty_),count_list_item(Confectioners_),count_list_item(Auto_),count_list_item(Railroads_),count_list_item(Restaurants_),count_list_item(Medical_),count_list_item(Apparel_),count_list_item(Packaged_),count_list_item(Computer_),count_list_item(Farm_),count_list_item(Diagnostics_),count_list_item(Industrial_),count_list_item(Consulting_),count_list_item(Real_),count_list_item(Utilities_Regulated_),count_list_item(Lodging_),count_list_item(Travel_),count_list_item(Airlines_)]
    Total_ = sum([x for x in Total_ if x !=None])
    f_tuple = (Total_,count_list_item(Internet_),count_list_item(Consumer_),count_list_item(Software_Infrastructure_),count_list_item(Semiconductors_),count_list_item(Telecom_),count_list_item(Semiconductor_),count_list_item(Drug_),count_list_item(Entertainment_),count_list_item(Communication_),count_list_item(Beverages_Non_Alcoholic_),count_list_item(Software_Application_),count_list_item(Biotechnology_),count_list_item(Electronic_),count_list_item(Discount_),count_list_item(Staffing_),count_list_item(null_),count_list_item(Credit_),count_list_item(Information_),count_list_item(Pharmaceutical_),count_list_item(Specialty_),count_list_item(Confectioners_),count_list_item(Auto_),count_list_item(Railroads_),count_list_item(Restaurants_),count_list_item(Medical_),count_list_item(Apparel_),count_list_item(Packaged_),count_list_item(Computer_),count_list_item(Farm_),count_list_item(Diagnostics_),count_list_item(Industrial_),count_list_item(Consulting_),count_list_item(Real_),count_list_item(Utilities_Regulated_),count_list_item(Lodging_),count_list_item(Travel_),count_list_item(Airlines_))
    print(f_tuple)
    insertDB([f_tuple])
    driver.close()
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='Trust',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    engine_js_op = create_engine('mysql+pymysql://root:123456@localhost:3306/Trust')
    cursor = connection.cursor()
    Total_dt_sql = "select Total_ from nasdap100_NP_daily;"
    Total_dt_= pd.read_sql_query(Total_dt_sql, engine_js_op)

    Total_dt_list = list(Total_dt_["Total_"])


    time_sql = "select  LastTime from nasdap100_NP_daily;"
    time_num = pd.read_sql_query(time_sql, engine_js_op)
    LastTime_list = list(time_num["LastTime"])

    line = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width='1000px', height='300px'))
            .add_xaxis(LastTime_list)
            .add_yaxis("NP", Total_dt_list)
            .set_global_opts(title_opts=opts.TitleOpts(title="nasdap100_NP_daily", subtitle="nasdap100_NP_daily"),
                             datazoom_opts=opts.DataZoomOpts(is_show=True))
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )
    line.render('nasdap100_NP_daily.html')
    line.render_notebook()



    connection.close()

#


# create table nasdap100_NP_daily (id int not null primary key auto_increment,Total_  text,Internet_  text,Consumer_  text,Software_Infrastructure_  text,Semiconductors_  text,Telecom_  text,Semiconductor_  text,Drug_  text,Entertainment_  text,Communication_  text,Beverages_Non_Alcoholic_  text,Software_Application_  text,Biotechnology_  text,Electronic_  text,Discount_  text,Staffing_  text,null_  text,Credit_  text,Information_  text,Pharmaceutical_  text,Specialty_  text,Confectioners_  text,Auto_  text,Railroads_  text,Restaurants_  text,Medical_  text,Apparel_  text,Packaged_  text,Computer_  text,Farm_  text,Diagnostics_  text,Industrial_  text,Consulting_  text,Real_  text,Utilities_Regulated_  text,Lodging_  text,Travel_  text,Airlines_  text,LastTime timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP) engine=InnoDB  charset=utf8;
