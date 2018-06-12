# -*- coding: utf-8 -*-
"""
@author: StrongLian
"""
from selenium import webdriver
import time
import json
import pandas
import os.path
#select 點擊
def multiselect_set_selections(driver, element_id, labels):
    el = driver.find_element_by_id(element_id)
    for option in el.find_elements_by_tag_name('option'):
        if option.text in labels:
            option.click()
    return
def updateAndSaveJSON(nameJSON, dictJSON):
    #更新與儲存
    if os.path.exists(nameJSON):
        with open(nameJSON, 'r') as inputfile:
            inputDataDict =  json.load(inputfile)
        #更新
        for key_i in inputDataDict.keys():
            if key_i in dictJSON.keys():
                inputDataDict[key_i].update(dictJSON[key_i])
        inputDataDict.update(dictJSON)
        #儲存
        with open(nameJSON, 'w') as outfile:
            json.dump(inputDataDict, outfile, sort_keys=True)
    else:
        with open(nameJSON, 'w') as outfile:
            json.dump(dictJSON, outfile, sort_keys=True)
    return
def Crawler_earthquakeList(year, month):
    earthquakeDataDict = dict()
    year = str(year)
    month = str(month)
    #換 網頁的年月
    multiselect_set_selections(driver,"ctl03_ddlYear",year)
    multiselect_set_selections(driver,"ctl03_ddlMonth",month)
    #按"送出"
    el = driver.find_element_by_id('ctl03_btnSearch')
    el.click()
    #撈 page
    page_html = driver.page_source
    df = pandas.read_html(page_html)
    #網頁表格位置
    try:
        monthTable = df[2]
    except:
        monthTable = df[1]
    monthTable.columns = monthTable.iloc[0]
    # 重設標頭
    earthquakeTable = monthTable.reindex(monthTable.index.drop(0))
    for i in range(1, len(earthquakeTable["地震編號"])+1):
        if earthquakeTable["地震編號"][i] == "小區域":
            continue
        #設定 dict 儲存空間
        if year not in earthquakeDataDict.keys():
            earthquakeDataDict[year]={}
        #時間格式
        month_split = earthquakeTable["臺灣時間"][i].split('月', 1)
        month = month_split[0]
        day_split = month_split[1].split('日', 1)
        day = day_split[0]
        #位置格式, 台 -> 臺
        locate = earthquakeTable["震央位置"][i][:3]
        if "台" in locate:
            temp = locate.split("台")
            #print(temp)
            locate = "臺"+temp[1]
        # 儲存
        earthquakeDataDict[year][earthquakeTable["地震編號"][i]]={"date":"%0.2d-%s"%(int(month), day),
                                                   "location":locate,
                                                   "strength":earthquakeTable["規模"][i]}
    return earthquakeDataDict
if __name__ == '__main__':
    #全域變數
    earthquakeDataJSON = "earthquakeData.json"
    DATA_URL = 'https://scweb.cwb.gov.tw/Page.aspx?ItemId=20&loc=tw&adv=1#'
    webDriverLoaction = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
    #變數
    earthquakeDataDict_all = dict()
    #開啟模擬器
    driver = webdriver.Chrome(webDriverLoaction)
    driver.get(DATA_URL)
    time.sleep(5) #等五秒，網站有點 LAG
    for year in range (2011, 2017+1):
        #設定 dict 儲存空間
        yearStr = str(year)
        if yearStr not in earthquakeDataDict_all.keys():
            earthquakeDataDict_all[yearStr]=dict()
        for month in range (1,13):
            monthStr = str(month)
            temp = Crawler_earthquakeList(yearStr, monthStr)
            earthquakeDataDict_all[yearStr].update(temp[yearStr])
    driver.quit() #driver.close()
    updateAndSaveJSON(earthquakeDataJSON, earthquakeDataDict_all)