import os
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient

from Db import Db
from ReadMarketD import ReadMarketData

app = Flask(__name__)

db = Db()

@app.route('/')
def statistics():
    book = db.getTradableBook()
    print(book)
    return render_template('statistics.html', book=book)

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
        f = request.files['file']
        rm = ReadMarketData()
        db.clean_all_documents()
        tradables = rm.aggrigate_All_Data_in_tradables(f.stream.read())
        db.insertTradables(tradables)

        return 'file uploaded successfully'

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
