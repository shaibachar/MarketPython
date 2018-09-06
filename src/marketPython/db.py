import sys
import datetime
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime

class Db(object):
    # TODO: export the url and db name to configuration class
    def __init__(self):
        client = MongoClient('mongodb://mongodb:27017/marketData')
        # use marketData database
        self.db = client.marketData

    def clean_marketData(self):
        # clean all table
        self.db.marketData.drop()

    def clean_book(self):
        # clean all table
        self.db.book.drop()

    def clean_all_documents(self):
        self.clean_marketData()
        self.clean_book()

    def insertTradables(self, tradables):
        print("going to insert ",len(tradables)," to DB")
        try:
            if tradables:
                toInsert = []
                for i in range(len(tradables)):
                    toInsert.append(tradables[i].__dict__)
                try:
                    result = self.db.marketData.insert_many(toInsert)
                except ValueError as v:
                    print("tradable:",toInsert,v)
                # update book

                for i in range(len(tradables)):
                    current_tradable = self.db.book.find_one(
                        {'tradableId': tradables[i].tradableId})

                    if current_tradable:
                        new_tradable_date = datetime.strptime(tradables[i].updated, '%d/%m/%Y')
                        current_tradable_date = datetime.strptime(current_tradable['updated'], '%d/%m/%Y')
                        if new_tradable_date > current_tradable_date:
                            self.db.book.delete_one({'tradableId': tradables[i].tradableId})
                            self.db.book.insert(tradables[i].__dict__)    
                        else:
                            # keep the old tradable
                            pass
                    else:
                        self.db.book.insert(tradables[i].__dict__)

                return result
            else:
                pass
        except Exception as e:
            print(e)

    def countMarketDocuments(self):
        # print count on tasks
        results = self.db.marketData.find()
        count = results.count()
        print("marketData count:", count)
        return count

    def countBookDocuments(self):
        # print count on tasks
        results = self.db.book.find()
        count = results.count()
        print("book count:", count)
        return count

    def selectTradableById(self, tradableId):
        selected = self.db.marketData.find_one({'tradableId': tradableId})
        return selected

    def selectAllTradables(self):
        selected = self.db.marketData.find()
        return selected

    def getTradableBook(self):
        selected = self.db.book.find()
        return selected

    def getTradableIdFromBook(self, tradableId):
        selected = self.db.book.find({'tradableId': tradableId})
        return selected
