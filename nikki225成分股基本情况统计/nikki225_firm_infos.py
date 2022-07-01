

import datetime
import time

import pymysql
import requests
from lxml import etree
import json
from queue import Queue
import threading
from requests.exceptions import RequestException
import csv




import datetime
import re
import time

import pymysql
import requests
from lxml import etree
from selenium import webdriver
from requests.exceptions import RequestException


def call_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None
def readjsonfile(filename):
    with open(filename, 'r', encoding='utf-8') as fw:
        s = json.load(fw)
        return s
# 正则和lxml混用
def parse_html(html):  # 正则专门有反爬虫的布局设置，不适合爬取表格化数据！



    selector = etree.HTML(html)
    last_price = selector.xpath('//*[@id="CONTENTS_MAIN"]/div[5]/dl[1]/dd/text()')
    firm_name = selector.xpath('//*[@id="basicInformation"]/div/div[2]/div/div/table/tbody/tr[1]/td/text()')
    firm_url = selector.xpath('//*[@id="basicInformation"]/div/div[2]/div/div/table/tbody/tr[2]/td/a/@href')
    shares_number = selector.xpath('//*[@id="basicInformation"]/div/div[2]/div/div/table/tbody/tr[13]/td/text()')
    employees_num = selector.xpath('//*[@id="basicInformation"]/div/div[2]/div/div/table/tbody/tr[20]/td/text()')
    average_age = selector.xpath('//*[@id="basicInformation"]/div/div[2]/div/div/table/tbody/tr[21]/td/text()')
    average_salary_annually = selector.xpath('//*[@id="basicInformation"]/div/div[2]/div/div/table/tbody/tr[22]/td/text()')
    average_salary_firstMonth = selector.xpath('//*[@id="basicInformation"]/div/div[2]/div/div/table/tbody/tr[23]/td/text()')
    f_last_price = "".join(last_price[0].split(","))
    f_shares_number="".join(re.findall("\d",shares_number[0].split()[0]))
    f_employees_num = "".join(re.findall("\d", employees_num[0].split()[0]))
    f_average_age = average_age[0].split("歳")[0].split()[0]
    f_average_salary_annually = "".join(re.findall("\d", average_salary_annually[0].split()[0]))
    f_average_salary_firstMonth = "".join(re.findall("\d", average_salary_firstMonth[0].split()[0]))
    market_value = float(f_last_price)*float(f_shares_number)/100000000

    result = [f_last_price,firm_name[0],f_average_salary_firstMonth,f_average_salary_annually,f_average_age,f_employees_num,market_value,f_shares_number,firm_url[0]]
    return result



def writeintoTSV_file(filename,data):
    with open(filename,'a', newline='\n', encoding="utf-8") as f_output:
        tsv_output = csv.writer(f_output, delimiter='\t')
        tsv_output.writerow(data)



if __name__=="__main__":
    json_list =[]
    url_list= []
    resultjson = readjsonfile("nikki225_nikkei_info.json")
    for item in resultjson:
        code = item["code"]

        nikkei_url = "https://www.nikkei.com/nkd/company/gaiyo/?scode={0}&ba=1".format(code)
        nikkei_url_page = item["nikkei_url"]
        industry_info = item["industry_info"]
        html = call_page(nikkei_url)
        result =parse_html(html)
        f_result = [code]+[nikkei_url_page]+[industry_info]+result
        print(f_result)
        time.sleep(1)
        writeintoTSV_file("nikki225_firm_infos.tsv", f_result)


