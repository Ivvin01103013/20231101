import firebase_admin
from firebase_admin import credentials
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

docs = [
{
  "title": "小王子【70周年精裝紀念版】",
  "author": "安東尼‧聖修伯里",
  "cover": "https://www.books.com.tw/img/001/066/04/0010660414.jpg",
  "url": "https://www.books.com.tw/products/0010660414",
  "anniversary": 70
},

{
  "title": "最後14堂星期二的課【20週年紀念版】",
  "author": "米奇‧艾爾邦",
  "cover": "https://www.books.com.tw/img/001/079/06/0010790676.jpg",
  "url": "https://www.books.com.tw/products/0010790676",
  "anniversary": 20
},

{
  "title": "撒哈拉歲月【三毛逝世30週年紀念版】",
  "author": "三毛",
  "cover": "https://www.books.com.tw/img/001/089/77/0010897794.jpg",
  "url": "https://www.books.com.tw/products/0010897794",
  "anniversary": 30
},

{
  "title": "靜宜求學趣",
  "author": "(您的姓名)",
  "cover": "(網路照片網址)",
  "url": "(您的個人網頁網址)",
  "anniversary": (您的年齡)
}

]

collection_ref = db.collection("圖書精選")
for doc in docs:
  collection_ref.add(doc)
