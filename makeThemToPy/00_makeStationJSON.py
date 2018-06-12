# -*- coding: utf-8 -*-
"""@author: StrongLian
"""
import urllib 
from bs4 import BeautifulSoup
from selenium import webdriver
import json
import time
#select 點擊
def multiselect_set_selections(driver, element_id, labels):
    el = driver.find_element_by_id(element_id)
    for option in el.find_elements_by_tag_name('option'):
        if option.text in labels:
            option.click()
    return
#主要流程
def Crawler_station(driver, base_url):
    stationDict = dict()
    #取得
    driver.get(base_url)#+"index.jsp")
    time.sleep(5) #等五秒，網站有點 LAG
    # 全名列表，換"測站所在縣市用"， labels
    cityHoleNameList = list()
    # 用於設定主要測站
    cityFirst = True
    #撈文章列表
    page_html    = driver.page_source
    page_soup    = BeautifulSoup(page_html,'html.parser')
    page_findTAG = page_soup.find_all('select')
    # 縣市列表，建表
    for temp in page_findTAG[0].find_all('option'):
        cityHoleNameList.append(temp.text)
        stationDict[str(temp.text[:3])] = dict()
    for city in cityHoleNameList:
        multiselect_set_selections(driver, "stationCounty", city)
        # 撈新頁面
        page_html    = driver.page_source
        page_soup    = BeautifulSoup(page_html,'html.parser')
        page_findTAG = page_soup.find_all('select')
        # 取得觀測站名稱及編號
        for stationStr in page_findTAG[1].find_all('option'):
            #print(stationStr)
            valueStr = str(stationStr).split('"')[1]
            nameStr = stationStr.text.split(" ")[0]
            code = urllib.parse.quote(urllib.parse.quote(nameStr))
            stationDict[city[:3]][valueStr] = code
            if cityFirst:
                stationDict[city[:3]]["stationNo"] =valueStr
                stationDict[city[:3]]["stationName"] = code
                cityFirst = False
        cityFirst = True 
    return stationDict
if __name__ == '__main__':
    #變數
    base_url = "https://e-service.cwb.gov.tw/HistoryDataQuery/"
    stationDictJson = "cityStationData.json"
    webDriverLoaction = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
    #開啟模擬器
    driver = webdriver.Chrome(webDriverLoaction)
    
    stationDict = Crawler_station(driver, base_url)
    #關閉模擬器
    driver.quit() #driver.close()
    #開啟
    with open(stationDictJson, 'w') as outfile:
        json.dump(stationDict, outfile, sort_keys=True)