import requests, json
from bs4 import BeautifulSoup

import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

from flask import Flask, render_template, request
from datetime import datetime, timezone, timedelta


app = Flask(__name__)

@app.route("/")
def index():
    X = "作者:徐维骏2023/12/06 sexual hentai Heaven  <br>"
    X += "<a href=/db>課程網頁</a><br>"
    X += "<a href=/tcyang?nick=tcyang>個人介紹及系統時間</a><br>"
    X += "<a href=/account>表單傳值</a><br>"
    X += "<br><a href=/read>讀取Firestore資料</a><br>"
    X += "<br><a href=/read2>人選之人─造浪者</a><br>"
    X += "<br><a href=/addbooks>海王</a><br>"
    X += "<br><a href=/search>演员关键子</a><br>"
    X += "<br><a href=/movie>讀取開眼電影即將上映影片，寫入Firestore</a><br>"
    X += "<br><a href=/searchroad>Accident</a><br>"

    return X

@app.route("/db")
def db():
    return "<a href='https://drive.google.com/drive/folders/1JGHLQWpzT2QxSVPUwLxrIdYowijWy4h1'>海青班資料庫管理課程</a>"

@app.route("/tcyang", methods=["GET", "POST"])
def tcyang():
    tz = timezone(timedelta(hours=+8))
    now = str(datetime.now(tz))
    user = request.values.get("nick")
    return render_template("Skhsu.html", datetime=now, name=user)

@app.route("/account", methods=["GET", "POST"])
def account():
    if request.method == "POST":
        user = request.form["user"]
        pwd = request.form["pwd"]
        result = "您輸入的帳號是：" + user + "; 密碼為：" + pwd 
        return result
    else:
        return render_template("account.html")

@app.route("/read")
def read():
    Result = ""
    db = firestore.client()     
    collection_ref = db.collection("徐维骏")    
    docs = collection_ref.get()    
    for doc in docs:         
        Result += "文件內容：{}".format(doc.to_dict()) + "<br>"    
    return Result

@app.route("/read2")
def read2():
    Result = ""
    db = firestore.client()     
    collection_ref = db.collection("人選之人─造浪者")    
    docs = collection_ref.order_by("birth").get()    
    for doc in docs: 
        x = doc.to_dict()        
        Result += "演员："+ x["name"] + ",在录音中" + x["role"] + ",出生" + str(x["birth"]) + "<br>"    
    return Result

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        keyword = request.form["keyword"]
        Result = "您輸入的关键字：" + keyword

        Result += "<br>"
        db = firestore.client()     
        collection_ref = db.collection("人選之人─造浪者")    
        docs = collection_ref.order_by("birth").get()    
        for doc in docs:         
            x = doc.to_dict()
            if keyword in x["name"]:
                Result += "演员："+ x["name"] + ",在录音中" + x["role"] + ",出生" + str(x["birth"]) + "<br>"   
        return Result
    else:
        return render_template("search.html")

@app.route("/addbooks")
def addbooks():
    Result = ""
    db = firestore.client()
    collection_ref = db.collection("圖書精選")
    docs = collection_ref.order_by("anniversary").get()
    for doc in docs:
        x = doc.to_dict()
        Result += "书名：<a href="+ x["url"] + ">" + x["title"] + "</a><br>"
        Result += "作者："+ x["author"] + "<br>"
        Result += str(x["anniversary"]) + "周年" + "<br>"
        Result += "<img src=" + x["cover"] + "></img><br><br>"
    return Result

@app.route("/movie")
def movie():
    url = "http://www.atmovies.com.tw/movie/next/"
    Data = requests.get(url)
    Data.encoding = "utf-8"
    sp = BeautifulSoup(Data.text, "html.parser")
    result=sp.select(".filmListAllX li")
    lastUpdate = sp.find("div", class_="smaller09").text[5:]

    for item in result:
        picture = item.find("img").get("src").replace(" ", "")
        title = item.find("div", class_="filmtitle").text
        movie_id = item.find("div", class_="filmtitle").find("a").get("href").replace("/", "").replace("movie", "")
        hyperlink = "http://www.atmovies.com.tw" + item.find("div", class_="filmtitle").find("a").get("href")
        show = item.find("div", class_="runtime").text.replace("上映日期：", "")
        show = show.replace("片長：", "")
        show = show.replace("分", "")
        showDate = show[0:10]
        showLength = show[13:]
        doc = {
            "title": title,
            "picture": picture,
            "hyperlink": hyperlink,
            "showDate": showDate,
            "showLength": showLength,
            "lastUpdate": lastUpdate
        }
        db = firestore.client()
        doc_ref = db.collection("電影").document(movie_id)
        doc_ref.set(doc)

    return "近期上映電影已爬蟲及存檔完畢，網站最近更新日期為：" + lastUpdate

@app.route("/searchroad", methods=["POST","GET"])
def searchroad():
    if request.method == "POST":
        Road = request.form["Road"]
        Result = "請輸入欲查詢的路名：" + Road
        url = "https://datacenter.taichung.gov.tw/swagger/OpenData/db36e286-1d2b-4784-99b9-3b0790dd9652"
        Data = requests.get(url)
        Data.encoding = "utf-8"
        JsonData = json.loads(Data.text)
        for item in JsonData:
            if Road in item["路口名稱"]:
                Result += item["路口名稱"] + "：發生" + item["總件數"] + "件，主因是" + item["主要肇因"] + "<br>"
                if Result == "":
                    Result = "抱歉，查無相關資料！"
        return Result
    else:
        return render_template("road.html")

if __name__ == "__main__":
    app.run(debug=True)
