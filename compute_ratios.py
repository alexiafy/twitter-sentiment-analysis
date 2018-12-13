from pymongo import MongoClient

connection = MongoClient("mongodb://localhost:27017/")
db = connection.fake_news                     # name of db (it should be changed to real_news or fake_news
collections = db.collection_names()


def ratio_pn():
    if tweet["replies_sentiment"]["positive_replies"] > 0 and tweet["replies_sentiment"]["negative_replies"] > 0:
        pn = tweet["replies_sentiment"]["positive_replies"] / tweet["replies_sentiment"]["negative_replies"]
    else:
        pn = -1

    # update tweet
    db[collection].update(
        {
            "id": tweet["id"]
        },
        {
            "$set": {
                "ratios.pn": round(pn, 4)
            }
        }
    )


def ratio_rpn():
    if tweet["replies_sentiment"]["positive_replies"] > 0 and tweet["replies_sentiment"]["negative_replies"] > 0:
        rpn = min(tweet["replies_sentiment"]["positive_replies"], tweet["replies_sentiment"]["negative_replies"]) / max(
        tweet["replies_sentiment"]["positive_replies"], tweet["replies_sentiment"]["negative_replies"])
    else:
        rpn = -1

    # update tweet
    db[collection].update(
        {
            "id": tweet["id"]
        },
        {
            "$set": {
                "ratios.rpn": round(rpn, 4)
            }
        }
    )


def ratio_pnpnt():
    if tweet["replies_sentiment"]["positive_replies"] > 0 and tweet["replies_sentiment"]["negative_replies"] > 0:
        pnt = (tweet["replies_sentiment"]["positive_replies"] + tweet["replies_sentiment"]["negative_replies"])/tweet["replies_count"]
        pnpnt = tweet["ratios"]["pn"] * pnt
        if pnpnt < 0:
            print(pnpnt)
            print(pnt)
            print(tweet["ratios"]["pn"])
    else:
        pnpnt = -1

    # update tweet
    db[collection].update(
        {
            "id": tweet["id"]
        },
        {
            "$set": {
                "ratios.pnpnt": round(pnpnt, 4)
            }
        }
    )
    if pnpnt>0 and pnpnt!=-1:
        print(round(pnpnt, 4))


for collection in collections:
    print(collection)
    length = db[collection].find().count()

    # if collection has no tweets, ignore it and continue to the next one
    if length == 0:
        continue

    tweets = db[collection].find().batch_size(10)
    for tweet in tweets:
        # take the replies of tweets
        replies_count = db[collection].find_one({'id': tweet["id"]})["replies_count"]
        # if replies of the tweet exist, then preprocess them
        if replies_count > 0:
            #ratio_pn()
            #ratio_rpn()
            ratio_pnpnt()
