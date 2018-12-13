from pymongo import MongoClient

connection = MongoClient("mongodb://localhost:27017/")
db = connection.fake_news                     # name of db (it should be changed to real_news or fake_news
collections = db.collection_names()


for collection in collections:
    length = db[collection].find().count()

    # if collection has no tweets, ignore it and continue to the next one
    if length == 0:
        continue

    tweets = db[collection].find().batch_size(10)
    for tweet in tweets:
        positive_counter = 0
        negative_counter = 0
        neutral_counter = 0

        # take the replies of tweets
        replies_count = db[collection].find_one({'id': tweet["id"]})["replies_count"]

        # if replies of the tweet exist, then preprocess them
        if replies_count > 0:
            replies = db[collection].find_one({'id': tweet["id"]})["replies"]

            for reply in replies:
                if reply["positive"] > abs(reply["negative"]):
                    positive_counter += 1
                elif reply["positive"] < abs(reply["negative"]):
                    negative_counter += 1
                elif reply["positive"] == abs(reply["negative"]):
                    neutral_counter += 1

            # update tweet
            db[collection].update(
                {
                    "id": tweet["id"]
                },
                {
                    "$set": {
                        "replies_sentiment.positive_replies": positive_counter,
                        "replies_sentiment.negative_replies": negative_counter,
                        "replies_sentiment.neutral_replies": neutral_counter
                    }
                }
            )
