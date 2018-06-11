# 1062_DataScience_FinalProject

###### JSOH format
  1. stationDictJson = "cityStationData.json" # 縣市，觀測站
    <pre><code>
   stationDictDcit = { 縣市 : { "stationNo": 主要編號, 
                               "stationName" : 對應測站名字 double URL encode , 
                                 測站編號 : 測站名字 double URL encode, ...
                                }, ...
                        }

    </code></pre>
  2. earthquakeDataJSON = "earthquakeData.json" #地震資料
   - earthquakeDataDict = { 年分 : { 地震編號 :{ "date" : "%0.2d-%0.2d"#(month, day),
                                               "location" : 評估縣市, 
                                               "strength" : 規模
                                               }, ...
                                   }, ...
                           }
  3. specificWeatherDataJSON = "SpecificWeatherData.json" # 特定天氣資料
   - specificWeatherDataDcit = { "%d-%0.02d"%(year, month) : { 縣市 : { "%0.2d"%(day) : { weatherData }, ...
                                                                      }, ...
                                                             }, ...
                               }
###### 參考資料
 1. 地震中心
  - https://scweb.cwb.gov.tw/Page.aspx?ItemId=20&loc=tw&adv=1
 2. 觀測資料查詢
  - https://e-service.cwb.gov.tw/HistoryDataQuery/
 3. JSON viewer
  - http://jsonviewer.stack.hu/
 4. selenium button click
  - https://pythonspot.com/selenium-click-button
 5. pyhton print flush。想弄單行輸出
  -  http://www.revotu.com/python3-print-function-keyword-arguments.html
  - http://www.revotu.com/how-to-flush-output-of-python-print.html
  - https://stackoverflow.com/questions/5598181/python-multiple-prints-on-the-same-line
 6. python dict
  - http://www.runoob.com/python/python-dictionary.html
 7. What is the correct way to select an option using Selenium's Python WebDriver
  - https://sqa.stackexchange.com/questions/1355/what-is-the-correct-way-to-select-an-option-using-seleniums-python-webdriver
 8. beautifulsoup find_all
  - https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/
 9. json dump save
  - http://kuma-uni.blogspot.com/2012/06/jsonpythonjson.html
  - https://docs.python.org/2/library/json.html
  - https://stackoverflow.com/questions/7100125/storing-python-dictionaries
