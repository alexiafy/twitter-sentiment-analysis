from pymongo import MongoClient


connection = MongoClient("mongodb://localhost:27017/")
db = connection.real_news                     # name of db (it should be changed to real_news or fake_news

collections = db.collection_names()


for collection in collections:
    db[collection].update({}, {"$unset": {"sentiment_score": 1}}, multi=True)
    db[collection].update({}, {"$unset": {"language_score": 1}}, multi=True)
    db[collection].update({}, {"$unset": {"intensity_score": 1}}, multi=True)
    db[collection].update({}, {"$unset": {"positive_replies": 1}}, multi=True)
    db[collection].update({}, {"$unset": {"neutral_replies": 1}}, multi=True)
    db[collection].update({}, {"$unset": {"negative_replies": 1}}, multi=True)

