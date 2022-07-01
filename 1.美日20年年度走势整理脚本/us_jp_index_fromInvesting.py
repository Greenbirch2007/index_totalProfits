# MT5 默认是东二区时间，  所以MT5的时间加上7 就是 可以处理的时间了


import pandas as pd
import datetime
import csv




def writeinto_detail(filename, data):
    with open(filename, "a", newline="", encoding="utf-8") as f:
        csv_out = csv.writer(f, delimiter=",")
        csv_out.writerow(data)



def fromDT_year_writeInto_tsvfile(excelfilename,_year):
    df = pd.read_excel(excelfilename)
    df['year'] = df['date_'].dt.strftime('%Y')
    _year_list   = []
    for i1,i2,i3 in zip(range(len(df['year'].values.tolist())+1),df['year'].values.tolist(),df["price_"].values.tolist()):
        if i2 == _year:
            one_dict= {}
            one_dict["ID"] =i1
            one_dict["price_"] = i3
            _year_list.append(one_dict)
    print(_year_list)
    # 排序排序
    _year_list.sort(key=lambda x: x['ID'],reverse=True)
    f_year_list = [(float(x["price_"])/float(_year_list[0]["price_"]))-1 for x in _year_list]
    print(_year_list)
    print(f_year_list)
    for one_item in f_year_list:
        writeinto_detail(_year+".tsv", [one_item])


if __name__ == "__main__":
    excelfilename = "中信标普300指数_2000_2022.xlsx"
    fromDT_year_writeInto_tsvfile(excelfilename, "2022")
    fromDT_year_writeInto_tsvfile(excelfilename, "2021")
    fromDT_year_writeInto_tsvfile(excelfilename, "2020")
    fromDT_year_writeInto_tsvfile(excelfilename, "2019")
    fromDT_year_writeInto_tsvfile(excelfilename, "2018")
    fromDT_year_writeInto_tsvfile(excelfilename, "2017")
    fromDT_year_writeInto_tsvfile(excelfilename, "2016")
    fromDT_year_writeInto_tsvfile(excelfilename, "2015")
    fromDT_year_writeInto_tsvfile(excelfilename, "2014")
    fromDT_year_writeInto_tsvfile(excelfilename, "2013")
    fromDT_year_writeInto_tsvfile(excelfilename, "2012")
    fromDT_year_writeInto_tsvfile(excelfilename, "2011")
    fromDT_year_writeInto_tsvfile(excelfilename, "2010")
    fromDT_year_writeInto_tsvfile(excelfilename, "2009")
    fromDT_year_writeInto_tsvfile(excelfilename, "2008")
    fromDT_year_writeInto_tsvfile(excelfilename, "2007")
    fromDT_year_writeInto_tsvfile(excelfilename, "2006")
    fromDT_year_writeInto_tsvfile(excelfilename, "2005")
    fromDT_year_writeInto_tsvfile(excelfilename, "2004")
    fromDT_year_writeInto_tsvfile(excelfilename, "2003")
    fromDT_year_writeInto_tsvfile(excelfilename, "2002")
    fromDT_year_writeInto_tsvfile(excelfilename, "2001")
    fromDT_year_writeInto_tsvfile(excelfilename, "2000")
