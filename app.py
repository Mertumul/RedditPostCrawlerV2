from flask import Flask, request, jsonify
import requests
import json
from pymongo import MongoClient
from bson import json_util
from flask_cors import CORS, cross_origin

'''
Bu Flask uygulamasi, "/redditCheck" yoluna gelen GET isteklerini işleyen bir API sunar. İstek yapildiğinda, 
MongoDB veritabanindaki "BrandDefance" adli koleksiyondan verileri alir ve son eklenen belgeleri geri döner.

'''
# Flask uygulaması oluşturulur ve CORS (Kaynaklar Arası Kaynak Paylaşımı) ayarları yapılır.
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5000"}, "POST": {"origins": "*"}})

# Bir MongoClient oluşturulur ve "BrandDefance" adlı veritabanına bağlantı yapılır. Ayrıca "post" adlı bir koleksiyon ve "appseed_db" adlı başka bir veritabanı da tanımlanır.
mongoClient = MongoClient()
db = mongoClient['reddit_posts']
collection = db['posts']
appSeedDb = mongoClient['appseed_db']


# /redditCheck" yoluna gelen GET istekleri için bir işlev (fonksiyon) tanımlanır.
@app.route('/redditCheck')
# İşlev içinde, MongoDB'de sorgu yapılır ve son eklenen belgeler "_id" alanına göre ters sıralanır.Sorgu sonucunda veri bulunursa, sonuçlar "json_util.dumps()" yöntemiyle JSON formatına dönüştürülür ve geri döndürülür.Veri bulunmazsa, "Error" yanıtı döndürülür.
def nvdnist():
    myquery = collection.find().sort("_id", -1)
    if (myquery):
        json_str = json_util.dumps(myquery)
        print("deneme:", json_str)
        return json_str
    else:
        return 'Error'


if __name__ == '__main__':
    app.run(debug=True, port=8001)
