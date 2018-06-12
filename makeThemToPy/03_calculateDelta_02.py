# -*- coding: utf-8 -*-
"""@author: StrongLian
"""
import json
def ListSum(inputList):
    sumInt = 0
    for temp in inputList:
        try:
            sumInt += float(temp)
        except:
            continue
    return sumInt

if __name__ == '__main__':
    deltaDict = dict()
    #變數
    needDataList = ["ObsTime", 'Temperature', 'RH', "Precp", "StnPres"]
    specificWeatherDataJSON = "SpecificWeatherData.json" #天氣資料儲存位置
    earthquakeDataJSON = "earthquakeData.json" #地震資訊
    overgateNum = 3
    dayInterval = 3
    persent_high = 0.8
    persent_low = 0.2
    #成立條件
    gateDict = {"Precp_gate":10, #降水量 
                "Temperature_gate" : 3, #溫度
                "RH_gate" : 5,
                "StnPres_gate" : 50, #氣壓
               }
    #讀取檔案
    with open(specificWeatherDataJSON, 'r') as inputfile:
        specificWeatherDataDict =  json.load(inputfile)
    with open(earthquakeDataJSON, 'r') as inputfile:
        earthquakeDataDict =  json.load(inputfile)
    #流程
    for year in sorted(earthquakeDataDict.keys()):
        print(year)
        deltaDict[year] = dict()
        for num in sorted(earthquakeDataDict[year].keys()):
#def ():
            try: 
                deltaDict[year][num] = dict()
                #print(num, end="->")
                dateYMD = "%s-%s"%(year, earthquakeDataDict[year][num]['date'])
                dateYM = dateYMD.rsplit("-",1)[0]
                loca = earthquakeDataDict[year][num]['location']
                #額外處理
                if "桃園" in loca:
                    temp = loca.split("縣")
                    loca = temp[0] + "市" 
                print(loca, dateYMD, end=">")
                #確認有，雖多仍做
                if loca in specificWeatherDataDict[dateYM].keys():
                    #蒐集資料
                    dataListDictTemp = dict()
                    for dataType in needDataList[1:]:#["Precp", "RH", "StnPres", "Temperature"]:
                        dataListDictTemp[dataType+"List"] = list()
                    # 讀取 取前三、後三，共六
                    dateSeq = earthquakeDataDict[year][num]['dateSeq']
                    #print(dateSeq)
                    for dateLoop in dateSeq:
                        ym = dateLoop.rsplit('-',1)[0]
                        #d = "%0.2d"%(int(dateLoop.rsplit('-',1)[1]))
                        d = "%d"%(int(dateLoop.rsplit('-',1)[1]))
                        #print(ym, d)
                        for dataType in needDataList[1:]:#["Precp", "RH", "StnPres", "Temperature"]:
                            dataListDictTemp[dataType+"List"].append(specificWeatherDataDict[ym][loca][d][dataType])
                    # 運算
                    for dataType in needDataList[1:]:#["Precp", "RH", "StnPres", "Temperature"]:
                        before = ListSum(dataListDictTemp[dataType+"List"][0:dayInterval]) / dayInterval
                        after = ListSum(dataListDictTemp[dataType+"List"][-dayInterval:]) / dayInterval

                        deltaDict[year][num][dataType+"_delta"] = after - before
                else:
                    print("not in")
                print("done")
            except KeyError as e:
                #print("error", e, "[ym][loca][d][dataType]",ym,loca,d,dataType)
                print("|")
                continue
    #計算筆數
    count = 0
    count_change = 0
    for year in deltaDict.keys():
        for num in deltaDict[year].keys():
            temp = deltaDict[year][num]
            if bool(temp): # is not empty
                count += 1
                count_OverGate = 0
                for dataType in needDataList[1:]:
                    if deltaDict[year][num][dataType+"_delta"] > gateDict[dataType+"_gate"]:
                        count_OverGate += 1
                if count_OverGate > overgateNum:
                    count_change += 1
    print("共",count,"可用資料，有", count_change, "筆成立")
    persent_count = count_change/count
    if persent_count > persent_high:
        print("流言成立")
    elif persent_count < persent_low:
        print("流言破解")    
    else:
        print("流言待考究") 