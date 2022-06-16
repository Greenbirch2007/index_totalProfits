
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
from selenium import webdriver
driver = webdriver.Chrome()
def use_selenium_headless(url):
    # 为Chrome配置无头模式

    # 在启动浏览器时加入配置

    driver.get(url)
    html = driver.page_source

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







def remove_list(item):
    if item == []:
        item = [""]
        result = item
    else:
        result = item
    return result

def writeinto_jsonfile(filename,list_data):
    with open(filename, 'w', encoding='utf-8') as fw:
        json.dump(list_data, fw, indent=4, ensure_ascii=False)
def list_null(list_content):
    if list_content !=[]:
        result = list_content
    else:
        result = ["null"]
    return result

if __name__ == '__main__':
    big_list = []
    sp500_forSearch = 'MSFT,AAPL,AMZN,FB,GOOGL,GOOG,JNJ,BRK.B,V,JPM,PG,UNH,MA,HD,INTC,VZ,NVDA,T,DIS,BAC,XOM,ADBE,CSCO,MRK,NFLX,PYPL,PFE,PEP,CMCSA,KO,CVX,WMT,ABBV,CRM,ABT,MCD,TMO,COST,AMGN,BMY,ACN,MDT,NKE,NEE,AVGO,LLY,UNP,AMT,TXN,C,ORCL,PM,LIN,WFC,DHR,IBM,HON,BA,QCOM,RTX,LOW,GILD,LMT,SBUX,MMM,FIS,BLK,CHTR,CVS,SPGI,MO,UPS,NOW,MDLZ,INTU,CI,AXP,PLD,CCI,D,BKNG,BDX,VRTX,CAT,ANTM,ISRG,GS,AMD,TJX,ADP,ZTS,DUK,GE,CME,CL,EQIX,SYK,TGT,REGN,SO,CB,FISV,ATVI,MS,USB,MU,CSX,GPN,MMC,TFC,AMAT,APD,ICE,ILMN,ADSK,BIIB,HUM,ECL,BSX,PNC,NOC,DE,ITW,DG,KMB,COP,SHW,NEM,PGR,NSC,MCO,ADI,AON,EW,BAX,EL,LRCX,SCHW,LHX,ROP,WM,AEP,TMUS,DD,EMR,EXC,EA,GIS,DLR,EBAY,DXCM,CNC,GD,ETN,SRE,GM,SBAC,PSX,XEL,COF,ROST,BK,FDX,ALL,ORLY,DOW,WBA,KMI,EOG,CTSH,MET,PSA,TRV,KLAC,STZ,TROW,AIG,APH,WEC,INFO,SYY,YUM,SNPS,HCA,MSCI,ES,JCI,AFL,VRSK,A,SLB,TEL,AZO,IDXX,TWTR,MNST,CMG,ZBH,CLX,VLO,PRU,CMI,KR,CDNS,PCAR,F,IQV,ED,PEG,HPQ,MAR,MPC,MCK,ALXN,PPG,WLTW,ROK,MCHP,PAYX,PH,MSI,ANSS,OTIS,RMD,AWK,FAST,WMB,SPG,TDG,XLNX,STT,WELL,AVB,BLL,FLT,CTAS,EQR,ADM,FE,HLT,TT,SWKS,O,CERN,EIX,VRSN,DLTR,GLW,MKC,VFC,PPL,SWK,DTE,EFX,ARE,CTVA,AME,KHC,ETR,FTNT,HSY,APTV,LUV,AMP,FTV,MKTX,MTD,DHI,ALGN,TSN,KEYS,BBY,FRC,CHD,CARR,LEN,CPRT,NTRS,AEE,AJG,DAL,LYB,RSG,DFS,OXY,LVS,TFX,CMS,AMCR,LH,INCY,CTXS,CDW,WY,K,AKAM,CAG,CBRE,ESS,PXD,MXIM,CAH,ODFL,WST,TTWO,KMX,FITB,FCX,PAYC,OKE,DGX,VMC,VTR,HIG,KSU,MTB,DPZ,ABC,TSCO,COO,DOV,ZBRA,HOLX,BR,PEAK,SYF,IP,BXP,IFF,EVRG,GRMN,NDAQ,MAA,MAS,VIAC,DRE,JKHY,GWW,HPE,KEY,LDOS,HRL,STE,ULTA,TIF,HES,QRVO,FMC,NUE,EXR,EXPD,WDC,GPC,MLM,ANET,OMC,WAT,ATO,SJM,BF.B,LNT,RF,STX,EXPE,CFG,XYL,NLOK,HAL,IEX,CXO,UDR,NVR,WAB,CBOE,SIVB,J,PFG,URI,ABMD,ETFC,PKI,CE,IT,IR,VAR,BKR,CHRW,HBAN,RCL,FOXA,MGM,JBHT,NTAP,XRAY,CTL,AVY,HAS,ALLE,LW,AAP,EMN,CINF,PKG,DRI,WU,CNP,PHM,RJF,HST,WYNN,RE,DISH,NI,PNW,L,FBHS,HSIC,AES,UAL,WRB,NRG,LKQ,FFIV,LNC,MYL,CPB,ALB,UHS,IRM,REG,JNPR,COG,WHR,TXT,FANG,GL,CCL,HII,SNA,WRK,TAP,PRGO,DVA,LYV,BWA,IPG,DISCK,AAL,AOS,AIZ,CF,VNO,PNR,FRT,BEN,ZION,RHI,ROL,MHK,AIV,CMA,IPGP,NWL,KIM,HWM,FLIR,PBCT,PWR,NLSN,MRO,APA,DVN,NBL,SEE,NOV,HFC,MOS,ALK,FOX,NWSA,LEG,NCLH,SLG,HBI,DXC,IVZ,TPR,HOG,PVH,RL,KSS,FLS,UNM,DISCA,LB,HRB,FTI,XRX,GPS,ADS,JWN,UAA,UA,NWS,COTY'
    list_sp500_forSearch_industry =sp500_forSearch.split(",")
    for code in list_sp500_forSearch_industry:

        industry_infos,sector_infos = getinfos_fromYhaooFinance(code)
        one_stock ={}
        one_stock["code"] = code
        one_stock["industry_infos"] = "".join(list_null(industry_infos)).split()[0]
        one_stock["sector_infos"] = "".join(list_null(sector_infos)).split()[0]
        big_list.append(one_stock)
        print(one_stock)
    writeinto_jsonfile("sp500_infos.json",big_list)



#
# if __name__ == '__main__':
#     # f_nasdap100 = [x for x in nasdap100 if x != ","]
#     f_nasdap100 = nasdap100.split(",")
#
#     for url_code in f_nasdap100:
#         url_f = 'https://finance.yahoo.com/quote/' + str(url_code) + '/financials?p=' + str(url_code)
#
#         html = call_page(url_f)
#         content = parse_stock_note(html)
#         print(content)
#         # insertDB(content)
#         print(datetime.datetime.now())
