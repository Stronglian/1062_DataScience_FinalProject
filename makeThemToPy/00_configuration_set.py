# -*- coding: utf-8 -*-
"""
@author: StrongLian

    1. 觀測時間 (LST) ObsTime - 日 
    + 測站氣壓 (hPa) StnPres
    + 海平面氣壓 (hPa) SeaPres
    + 測站最高氣壓 (hPa) StnPresMax
    + 測站最高氣壓時間 (LST) StnPresMaxTime
    + 測站最低氣壓 (hPa) StnPresMin
    + 測站最低氣壓時間 (LST) StnPresMinTime
    + 氣溫 (℃) Temperature
    + 最高氣溫 (℃) T Max
    + 最高氣溫時間 (LST) T Max Time
    + 最低氣溫 (℃) T Min
    + 最低氣溫時間 (LST) T Min Time
    + 露點溫度 (℃) Td dew point
    + 相對溼度 (%) RH
    + 最小相對溼度 (%) RHMin
    + 最小相對溼度時間 (LST) RHMinTime
    + 風速 (m/s) WS
    + 風向 (360degree) WD
    + 最大陣風 (m/s) WSGust
    + 最大陣風風向 (360degree) WDGust
    + 最大陣風風速時間 (LST) WGustTime
    + 降水量 (mm) Precp
    + 降水時數 (hr) PrecpHour
    + 10分鐘最大降水量 (mm) PrecpMax10
    + 10分鐘最大降水起始時間 (LST) PrecpMax10Time
    + 一小時最大降水量 (mm) PrecpHrMax
    + 一小時最大降水量起始時間 (LST) PrecpHrMaxTime
    + 日照時數 (hr) SunShine 
    + 日照率 (%) SunShineRate
    + 全天空日射量 (MJ/㎡) GloblRad
    + 能見度 (km) VisbMean
    + A型蒸發量 (mm) EvapA
"""

import json
import os.path

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

if __name__ == '__main__':
    #組態儲存檔名
    configJSON = "configuration.json"
    #預設內容
    # - 檔案儲存位置
    JSONFileForder = "./"
    # - 檔案儲存名稱
    stationDictJson = "cityStationData.json" # 縣市，觀測站
    earthquakeDataJSON = "earthquakeData.json" #地震資料
    specificWeatherDataJSON = "SpecificWeatherData.json" # 特定天氣資料
    # - 觀測站
    codis_URL = "https://e-service.cwb.gov.tw/HistoryDataQuery/"
    # - 地震資訊
    earthquarkeTable_URL = 'https://scweb.cwb.gov.tw/Page.aspx?ItemId=20&loc=tw&adv=1#'
    # - webDriver 位置
    webDriverLoaction = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
    # - 偵測天數
    dayInterval = 3 #day
    # - 天氣資料設定
    needDataList = ["ObsTime", 'Temperature', 'RH', "Precp", "StnPres"]
    gateDict = {"Precp_gate"       :10, #降水量 
                "Temperature_gate" : 3, #溫度
                "RH_gate"          : 5,
                "StnPres_gate"     : 50, #氣壓
                           }
    # - - 資料判定
    persent_high = 0.8
    persent_low = 0.2
    overgateNum = 3
    # - - needDateList 所有選項
    # - - 全部資料類型
    dataList = ['ObsTime',  'StnPres',  'SeaPres', 'StnPresMax', 
                'StnPresMaxTime', 'StnPresMin', 'StnPresMinTime', 
                'Temperature', 'T Max', 'T Max Time', 'T Min', 
                'T Min Time', 'Td dew point', 'RH', 'RHMin', 'RHMinTime',
                'WS', 'WD', 'WSGust', 'WDGust', 'WGustTime', 'Precp', 'PrecpHour',
                'PrecpMax10', 'PrecpMax10Time', 'PrecpHrMax', 'PrecpHrMaxTime',
                'SunShine', 'SunShineRate', 'GloblRad', 'VisbMean', 'EvapA']