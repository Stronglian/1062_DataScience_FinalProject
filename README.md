# 1062_DataScience_FinalProject

## 程式功能 in makeThemToPy
 
### 00_makeStationJSON.py
抓取所有觀測站列表，生成 cityStationData.json。
並將預設第一個的設為預設觀測站。
main: 直接將所有的觀測站與內容抓下來

### 01_earthquakeCrawer.py
抓取地震中心資料，形成列表 earthquakeData.json。
main: 抓取 2011 - 2017 每月地震資料(日期、中央縣市、規模)

### 02_weatherCrawer_01.py
配合 cityStationData.json 依照 earthquakeData.json，去找對應日期與地點的天氣資料，進而生成 SpecificWeatherData.json。
並在 earthquakeData.json 中每筆地震資料，追加前後三天的日期序列。
main: 利用 earthquakeData.json 的資料跑。
RunData(earthquakeDate, locationCity, stationDict): 
GetCWBData(locationCity, station, stname, yearMon, dayList): 

### 03_calculateDelta.py
抓前三天與後三天的指定資料各自平均數，進行比較，超過設定 gate 並算入符合。


### 00_configuration_set.py (建構中)
設定所有會共同用到的參數。

##### 變數名稱 - 預設內容
##### - 檔案儲存位置
JSONFileForder = "./"

##### - 檔案儲存名稱
stationDictJson = "cityStationData.json" # 縣市，觀測站
earthquakeDataJSON = "earthquakeData.json" #地震資料
specificWeatherDataJSON = "SpecificWeatherData.json" # 特定天氣資料

##### - 觀測站
codis_URL = "https://e-service.cwb.gov.tw/HistoryDataQuery/"

##### - 地震資訊
earthquarkeTable_URL = 'https://scweb.cwb.gov.tw/Page.aspx?ItemId=20&loc=tw&adv=1#'

##### - webDriver 位置
webDriverLoaction = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'

##### - 偵測天數
dayInterval = 3 #前後三天

##### - 天氣資料設定
needDataList = ["ObsTime", 'Temperature', 'RH', "Precp", "StnPres"] #指定參數
gateDict = {"Precp_gate"       :10, #降水量 
            "Temperature_gate" : 3, #溫度
            "RH_gate"          : 5, #相對溼度
            "StnPres_gate"     : 50, #氣壓
                       }
##### - - 資料判定
persent_high = 0.8
persent_low = 0.2
overgateNum = 3

###### JSON format
  1. stationDictJson = "cityStationData.json" # 縣市，觀測站
    <pre><code>stationDictDcit = { 縣市 : { 
                                "stationNo": 主要編號, 
                               "stationName" : 對應測站名字 double URL encode , 
                                 測站編號 : 測站名字 double URL encode, ...
                                }, ...
                        }</code></pre>
  2. earthquakeDataJSON = "earthquakeData.json" #地震資料
    <pre><code>earthquakeDataDict = { 年分 : {
                                               地震編號 :{
                                               "date" : "%0.2d-%0.2d"#(month, day),
                                               "location" : 評估縣市, 
                                               "strength" : 規模
                                               }, ...
                                   }, ...
                           }</code></pre>
  3. specificWeatherDataJSON = "SpecificWeatherData.json" # 特定天氣資料
    <pre><code>specificWeatherDataDcit = { "%d-%0.02d"%(year, month) : {
    縣市 : {
    "%0.2d"%(day) : { weatherData }, ...
                                                                      }, ...
                                                             }, ...
                               }</code></pre>

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
