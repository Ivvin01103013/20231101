import requests
url = "https://datacenter.taichung.gov.tw/swagger/OpenData/db36e286-1d2b-4784-99b9-3b0790dd9652"
Data = requests.get(url)
print(Data.text)
