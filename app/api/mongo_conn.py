'''
Created on 20171029

@author: zhou
'''


from pymongo import MongoClient

def Mongo_Conn():
    client = MongoClient('mongodb://robot:robot@ds115546.mlab.com:15546/robotdb')
    db = client.robotdb
    return db

def Mongo_dailysentence():
    client = MongoClient('mongodb://daily:daily@ds133296.mlab.com:33296/dailysentence')
    db = client.dailysentence
    return db