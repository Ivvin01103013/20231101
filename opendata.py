import requests, json
url = "https://datacenter.taichung.gov.tw/swagger/OpenData/db36e286-1d2b-4784-99b9-3b0790dd9652"
Data = requests.get(url)
#print(Data.text)
JsonData = json.loads(Data.text)
Result = ""
Road = input("請輸入欲查詢的路名：")
for item in JsonData:
	if Road in item["路口名稱"]:
		Result += item["路口名稱"] + "：發生" + item["總件數"] + "件，主因是" + item["主要肇因"] + "\n\n"
if Result == "":
	Result = "抱歉，查無相關資料！"
print(Result)
