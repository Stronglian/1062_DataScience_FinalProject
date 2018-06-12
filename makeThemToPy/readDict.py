# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 01:29:13 2018

@author: Strong
"""

import json

stationDictJson = "cityStationData.json" # 縣市，觀測站
earthquakeDataJSON = "earthquakeData.json" #地震資料
specificWeatherDataJSON = "SpecificWeatherData.json" # 特定天氣資料


with open(specificWeatherDataJSON, 'r') as inputfile:
    inputDataDict =  json.load(inputfile)
    