# -*- coding: utf-8 -*-
"""
@author: StrongLian
"""
import pandas
import json
import os.path
# 定義月份最大天
def YMtoMonDays(year, mon, d = 0): # ****-**
    year = int(year)
    mon = int(mon) + d
    if mon < 1:
        mon = mon + 12
    elif mon > 12:
        mon = mon - 12
    monthMaxDayList = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if mon != 2:
        days = monthMaxDayList[mon-1]
    else:
        if year%4 != 0:
            days = 28
        elif (year%4 == 0) and (year%100 != 0):
            days = 29
        elif (year%100 == 0) and (year%400 != 0):
            days = 28
        elif (year%400 == 0):
            days = 29
    return days
def GetCWBData(locationCity, station, stname, yearMon, dayList): #no, name, timeYM,timeD 
    #return
    doOrNot = True
    # 重複資料重複使用
    if yearMon in temp_df_dict.keys():
        if station in temp_df_dict[yearMon].keys():
            monthTable = temp_df_dict[yearMon][station]
            doOrNot = False
    else:
        temp_df_dict[yearMon] = dict()
    if doOrNot:
        # 資料表網址
        search_url = base_url+"MonthDataController.do?command=viewMain&station="+station+"&stname="+stname+"&datepicker="+yearMon
        # 抓資料表
        df = pandas.read_html(search_url)
        monthTable = df[1][1:]
        #清除標頭亂碼
        header = []
        for te in monthTable.iloc[0]:
            temp = te.split(')')[-1]
            #print(temp)
            header.append(temp)
        #設定 header
        #monthTable.columns = monthTable.iloc[0]
        monthTable.columns = header
        # 重設標頭
        monthTable = monthTable.reindex(monthTable.index.drop(1))
        
        #儲存
        temp_df_dict[yearMon][station] = monthTable
    ##### OLD
    #存進dict
    # 確認dict["年月"]存在
    if yearMon not in data_dict.keys():
        data_dict[yearMon] = dict()
    # 確認dict["地點"]存在 
    if yearMon not in data_dict[yearMon].keys():
        data_dict[yearMon][locationCity] = dict()
    # 依照指定日期存資料
    for d in dayList:
        #確認dict["日"]存在
        if d not in data_dict[yearMon][locationCity].keys():
            data_dict[yearMon][locationCity][d] = dict()
        #儲存資料
        for dayType in needDataList[1:]:
            #print(d, type(d))
            data_dict[yearMon][locationCity][d][dayType] = monthTable[dayType][d+1]    
    return 
def RunData(earthquakeDate, locationCity, stationDict):
    #例外處理
    if "桃園" in locationCity:
        temp = locationCity.split("縣")
        locationCity = temp[0] + "市" 
    # 日期清單
    dateSeq = list()
    # 取得時間
    temp = earthquakeDate.split("-")
    year = "%0.2d"%(int(temp[0]))
    month = "%0.2d"%(int(temp[1]))
    day = "%0.2d"%(int(temp[2]))
    # 取得觀測站名稱及編號
    station = stationDict[locationCity]["stationNo"]
    stname = stationDict[locationCity]["stationName"]
    #日期設置 - 當月份
    startDay = int(day) - dayInterval
    endDay = int(day) + dayInterval
    #開始有跨月問題: 
    #若不跨月
    if (int(day) - dayInterval > 0 ) and (int(day) + dayInterval <=  YMtoMonDays(year, month)):
        # dict 對應名稱，對網頁也是
        yearMon = "%s-%0.2d"%(year, int(month))
        dayList = list(range(startDay, endDay+1))
        # 擷取資料
        GetCWBData(locationCity, station, stname, yearMon, dayList)
        for d in dayList:
            dateSeq.append(yearMon + '-' + str(d))
    # 跨月不跨年
    else:
        #print(year,"-",month)
        yearMonList = list()
        dayListList = list()
        if (int(day) - dayInterval <= 0 ): #print("往過去跨月")
            #原本月份 - 未來
            yearMon = "%s-%0.2d"%(year, int(month))
            dayList = list(range(1, endDay+1))
            
            yearMonList.append(yearMon)
            dayListList.append(dayList)
            #新月份 - 過去
                #跨年與否
            if month == "01":
                month_n = 12
                year_n = "%0.2d"%(int(year)-1)
            else:
                month_n = int(month) - 1
                year_n = year
            yearMon_n = "%s-%0.2d"%(year_n, month_n)
            monthMaxDay_n = YMtoMonDays(year, month, -1)
            dayList_n = list(range(monthMaxDay_n + startDay, monthMaxDay_n+1))
            
            yearMonList.append(yearMon_n)
            dayListList.append(dayList_n)
        elif (int(day) + dayInterval > YMtoMonDays(year, month)): #print("往未來跨月")
            #原本月份 - 過去
            yearMon = "%s-%0.2d"%(year, int(month))
            dayList = list(range(startDay, YMtoMonDays(year, month)+1))
            
            yearMonList.append(yearMon)
            dayListList.append(dayList)
            #新月份 - 未來
                #跨年與否
            if month == "12":
                month_n = 1
                year_n = "%0.2d"%(int(year)+1)
            else:
                month_n = int(month) + 1
                year_n = year
            yearMon_n = "%s-%0.2d"%(year_n, month_n)
            dayList_n = list(range(1, endDay - YMtoMonDays(year, month) + 1))
            
            yearMonList.append(yearMon_n)
            dayListList.append(dayList_n)
        
        #print(yearMonList)
        #print(dayListList)    
        #執行撈取
        for i in range(len(yearMonList)):
            GetCWBData(locationCity, station, stname, yearMonList[i], dayListList[i])
    
        for i in range(len(yearMonList)):
            yearMon_t = yearMonList[i]
            dayList_t = dayListList[i]
            for d in dayList_t:
                dateSeq.append(yearMon_t + '-' + str(d))
    return dateSeq
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
    #變數
    base_url = "https://e-service.cwb.gov.tw/HistoryDataQuery/"
    specificWeatherDataJSON = "SpecificWeatherData.json" #天氣資料儲存位置
    earthquakeDataJSON = "earthquakeData.json"
    stationDictJson = "cityStationData.json"
    inputDataJSON = "SpecificWeatherData.json"
    # - 欲抓取天氣資料
    needDataList = ["ObsTime", 'Temperature', 'RH', "Precp", "StnPres"]
    # - 時間區間寬度
    dayInterval = 3
    # 
    data_dict = dict()
    # 單一次 data frame 儲存使用
    temp_df_dict = dict()
    #檔案讀取
    with open(stationDictJson, 'r') as inputfile:
        stationDict =  json.load(inputfile)
    with open(earthquakeDataJSON, 'r') as inputfile:
        earthquakeDataDict =  json.load(inputfile)
    #爬蟲流程
    for year in sorted(earthquakeDataDict.keys()):
        print(year)
        for num in sorted(earthquakeDataDict[year].keys()):
            temp = earthquakeDataDict[year][num]
            #print(num, temp, flush = False)
            print("\r\r\r\r\r"+num, end="", flush = False)
            locationCity = temp['location']
            earthquakeDate = "%s-%s"%(year, temp['date'])
            #print(earthquakeDate, locationCity)
            #正式
            dateSeq = RunData(earthquakeDate, locationCity, stationDict)
            earthquakeDataDict[year][num]['dateSeq'] = dateSeq
        print(" -Done")
    updateAndSaveJSON(inputDataJSON, data_dict)
    # 更新地震的 date Sequence
    with open(earthquakeDataJSON, 'w') as outfile:
        json.dump(earthquakeDataDict, outfile)