from pymongo import MongoClient
import re
from nltk.stem.snowball import SnowballStemmer

connection = MongoClient("mongodb://localhost:27017/")
db = connection.real_news                     # name of db (it should be changed to real_news or fake_news
collections = db.collection_names()

stemmer = SnowballStemmer("english")


def controversy_lexicon():
    '''
        count controversial words from Mejova controversy lexicon
    '''

    file = open('input/controversial_words.txt', 'r')
    text = file.read()
    words = text.split(", ")

    controversy_replies = 0

    for reply in replies:
        reply_text = reply["text_tokenized"]

        # check if at least one controversy word is included
        reply_tokens = [stemmer.stem(token) for token in reply_text]
        words = [stemmer.stem(token) for token in words]
        result = any(elem in words for elem in reply_tokens)

        if result:
            controversy_replies += 1

    # update tweet
    db[collection].update(
        {
            "id": tweet["id"]
        },
        {
            "$set": {
                "language_scores.controversy_replies": controversy_replies,
                "language_scores.controversy_score": controversy_replies/tweet["replies_count"]
            }
        }
    )
    file.close()


def bias_lexicon():
    '''
            count bias words from Mejova controversy lexicon
        '''

    file = open('input/bias-lexicon.txt', 'r')
    text = file.read()
    words = text.split("\n")

    bias_replies = 0

    for reply in replies:
        reply_text = reply["text_tokenized"]

        # check if at least one controversy word is included
        reply_tokens = [stemmer.stem(token) for token in reply_text]
        words = [stemmer.stem(token) for token in words]
        result = any(elem in words for elem in reply_tokens)

        if result:
            bias_replies += 1

    # update tweet
    db[collection].update(
        {
            "id": tweet["id"]
        },
        {
            "$set": {
                "language_scores.bias_replies": bias_replies,
                "language_scores.bias_score": bias_replies/tweet["replies_count"]
            }
        }
    )
    file.close()


def skepticism_lexicon():
    '''
            count bias words from Mejova controversy lexicon
        '''

    file = open('input/skepticism_words.txt', 'r')
    text = file.read()
    words = text.split(", ")

    skepticism_replies = 0

    for reply in replies:
        reply_text = reply["text_tokenized"]

        # check if at least one controversy word is included
        reply_tokens = [stemmer.stem(token) for token in reply_text]
        words = [stemmer.stem(token) for token in words]
        result = any(elem in words for elem in reply_tokens)

        if result:
            skepticism_replies += 1

    # update tweet
    db[collection].update(
        {
            "id": tweet["id"]
        },
        {
            "$set": {
                "language_scores.skepticism_replies": skepticism_replies,
                "language_scores.skepticism_score": skepticism_replies/tweet["replies_count"]

            }
        }
    )
    file.close()


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
            replies = db[collection].find_one({'id': tweet["id"]})["replies"]
            #controversy_lexicon()
            bias_lexicon()
            #skepticism_lexicon()
