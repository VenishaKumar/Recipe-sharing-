from pymongo import MongoClient

def connect_db():
  client=MongoClient(host='localhost',port=27017 ,username='',password='',)
  db=client['recepie']
  return db