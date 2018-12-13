from pymongo import MongoClient
import re

connection = MongoClient("mongodb://localhost:27017/")
db = connection.real_news                     # name of db (it should be changed to real_news or fake_news
collections = db.collection_names()


# get controversial words from txt file
file = open('input/controversial_words.txt', 'r')
text = file.read()
words = text.split(",")


def sentiment_score():
    counter_replies = 1                # counter for processed replies
    pos_counter = 0
    neg_counter = 0

    # count positive and negative replies
    for reply in replies:
        counter_replies += 1

        positive = reply["positive"]       # take the positive value
        negative = reply["negative"]       # take the negative value

        if positive > abs(negative):
            pos_counter += 1
        elif positive < abs(negative):
            neg_counter += 1

    # division with zero. If pos_counter + neg_counter == 0, the tweet has neutral sentiment and
    # we can ignore it
    if (pos_counter + neg_counter) > 0:
        # calculate sentiment score
        if 1.5*pos_counter < neg_counter:
            senti_score = abs((pos_counter - neg_counter)/(pos_counter + neg_counter))
        else:
            senti_score = 1 - abs((pos_counter - neg_counter)/(pos_counter + neg_counter))
    else:
        senti_score = -1

    # update tweet
    db[collection].update(
        {
            "id": tweet["id"]
        },
        {
            "$set": {
                "scores.sentiment_score": round(senti_score, 4)
            }
        }
    )

    return senti_score


def language_score():
    contr_counter = 0

    # count replies with at least one controversy word
    for reply in replies:
        contr_word_exists = False
        reply_text = reply["text"].lower()

        # check if at least one controversy word is included
        for word in words:
            if re.search(r"\b" + re.escape(word) + r"\b", reply_text):
                contr_word_exists = True
        if contr_word_exists:
            contr_counter += 1

    # calculate language score
    lang_score = contr_counter/tweet["replies_count"]

    # update tweet
    db[collection].update(
        {
            "id": tweet["id"]
        },
        {
            "$set": {
                "scores.language_score": round(lang_score, 4)
            }
        }
    )

    return lang_score


def topic_intensity_score(avg_fav, avg_replies, avg_retweets, tweet):

    fav = tweet["favorite_count"]
    replies = tweet["replies_count"]
    retweets = tweet["retweet_count"]

    intensity_score = (fav/avg_fav + replies/avg_replies + retweets/avg_retweets)/3

    # update tweet
    db[collection].update(
        {
            "id": tweet["id"]
        },
        {
            "$set": {
                "scores.intensity_score": round(intensity_score, 4)
            }
        }
    )

    return intensity_score


def compute_parameters():
    tweets = db[collection].find()
    fav_sum = 0
    replies_sum = 0
    retweets_sum = 0
    counter = 0

    # count the sum of favorites, replies and retweets of ALL tweets (??)
    for tweet in tweets:
        fav_sum += tweet["favorite_count"]
        replies_sum += tweet["replies_count"]
        retweets_sum += tweet["retweet_count"]
        counter += 1

    # calculate average of favorites, replies and retweets of all tweets of the collection
    avgFav = fav_sum/counter
    avgReplies = replies_sum/counter
    avgRetweets = retweets_sum/counter

    return avgFav, avgReplies, avgRetweets


for collection in collections:
    length = db[collection].find().count()

    # if collection has no tweets, ignore it and continue to the next one
    if length == 0:
        continue

    print(collection)
    avg_fav, avg_replies, avg_retweets = compute_parameters()

    tweets = db[collection].find().batch_size(10)
    counter_tweets = 1                 # counter for preprocessed tweets

    for tweet in tweets:
        #print('Processing collection:', collection, 'Tweet id: ', tweet["id"], '[' + str(counter_tweets) + ']')
        counter_tweets += 1

        # take the replies of tweets
        replies_count = db[collection].find_one({'id': tweet["id"]})["replies_count"]
        # if replies of the tweet exist, then preprocess them
        if replies_count > 0:
            replies = db[collection].find_one({'id': tweet["id"]})["replies"]
            SS = round(sentiment_score(), 4)
            #LS = round(language_score(), 4)
            #TI = round(topic_intensity_score(avg_fav, avg_replies, avg_retweets, tweet), 4)

    file.close()










