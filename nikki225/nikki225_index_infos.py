
#nasdap 100

# 1 各大指数制作json文件,代码,板块 。。。
# 2 保证都有效。财务数据模型再整理!每3天做一次采集!
# 3 指数,也就是市场的整体收益状况就有一个足够的把握。这个是除了技术之外的最最核心的基金交易的依据。
#! -*- coding:utf-8 -*-

import json
import datetime
import re
import time

import pymysql
import requests
from lxml import etree
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

from selenium.webdriver import PhantomJS

def use_selenium_headless(url):
    ch_options = PhantomJS("C:\\Python310\\Scripts\\phantomjs.exe") # windows
    ch_options.get(url)
    html = ch_options.page_source
    ch_options.close()
    return html



def use_requests(url):
    response = requests.get(url)
    return response.text






def getinfos_fromYhaooFinance(code):
    url = "https://finance.yahoo.com/quote/{0}/profile?p={0}".format(code)
    html = use_selenium_headless(url)
    selector = etree.HTML(html)
    industry_infos = selector.xpath('//*[@id="Col1-0-Profile-Proxy"]/section/div[1]/div/div/p[2]/span[4]/text()')
    sector_infos = selector.xpath('//*[@id="Col1-0-Profile-Proxy"]/section/div[1]/div/div/p[2]/span[2]/text()')
    return industry_infos,sector_infos





def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='ForLynne',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    try:
        cursor.executemany('insert into spplusnas_industry_infos (code,title_zh_cn,industry_infos,sector_infos,infos_zh_cn) values (%s,%s,%s,%s,%s)', content)
        connection.commit()
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError :
        pass


def writeinto_jsonfile(filename,list_data):
    with open(filename, 'w', encoding='utf-8') as fw:
        json.dump(list_data, fw, indent=4, ensure_ascii=False)
def list_null(list_content):
    if list_content !=[]:
        result = list_content
    else:
        result = ["null"]
    return result
def writeinto_detail(filename,data):
    with open(filename,"a",newline="",encoding="utf-8") as f:
        csv_out = csv.writer(f,delimiter=",")
        csv_out.writerow(data)

#
if __name__ == '__main__':
    big_list = []
    nasdap100 = 'AAPL,MSFT,AMZN,GOOG,GOOGL,FB,INTC,CMCSA,PEP,CSCO,ADBE,NVDA,NFLX,TSLA,COST,PYPL,AMGN,AVGO,TXN,CHTR,SBUX,QCOM,GILD,MDLZ,TMUS,FISV,BKNG,INTU,ADP,ISRG,VRTX,MU,CSX,BIIB,AMAT,AMD,ATVI,EXC,MAR,LRCX,WBA,ADI,ROST,ADSK,REGN,ILMN,CTSH,XEL,JD,MNST,MELI,NXPI,BIDU,KHC,SIRI,PAYX,EA,LULU,EBAY,CTAS,WDAY,ORLY,VRSK,WLTW,CSGP,PCAR,KLAC,SPLK,NTES,MCHP,VRSN,ANSS,IDXX,CERN,ALXN,ASML,SNPS,FAST,DLTR,CPRT,XLNX,CDNS,ALGN,SGEN,WDC,UAL,SWKS,CDW,CHKP,ULTA,INCY,TCOM,BMRN,EXPE,MXIM,CTXS,TTWO,FOXA,AAL,NTAP,FOX,LBTYK,LBTYA'
    list_nas100_industry =nasdap100.split(",")
    for code in list_nas100_industry:

        industry_infos,sector_infos = getinfos_fromYhaooFinance(code)
        one_stock ={}
        one_stock["code"] = code
        one_stock["industry_infos"] = "".join(list_null(industry_infos)).split()[0]
        one_stock["sector_infos"] = "".join(list_null(sector_infos)).split()[0]
        big_list.append(one_stock)
        print(one_stock)
    writeinto_jsonfile("nasdap100_infos.json",big_list)



