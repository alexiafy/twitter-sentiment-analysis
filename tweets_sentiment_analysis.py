import subprocess
import shlex
from pymongo import MongoClient


connection = MongoClient("mongodb://localhost:27017/")
db = connection.fake_news                     # name of db (it should be changed to real_news or fake_news

collections = db.collection_names()


def RateSentiment(sentiString):
    '''
    Compute sentiment analysis of text with SentiStrength
    '''

    # open a subprocess using shlex to get the command line string into the correct args list format
    p = subprocess.Popen(shlex.split("java -jar C:/Users/User/SentiStrength/SentiStrength.jar stdin sentidata "
                                     "C:/Users/User/SentiStrength/SentiStrength_Data/"),
                                     stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # communicate via stdin the string to be rated. Note that all spaces are replaced with +
    # can't send string in Python 3, must send bytes
    b = bytes(sentiString.replace(" ", "+"), 'utf-8')
    stdout_byte, stderr_text = p.communicate(b)

    # convert from byte
    stdout_text = stdout_byte.decode("utf-8")

    # replace the tab with a space between the positive and negative ratings. e.g. 1    -5 -> 1 -5
    stdout_text = stdout_text.rstrip().replace("\t", " ")

    # split results
    stdout_text = stdout_text.splitlines()
    for item in stdout_text:
        results = item.split(" ")
        positive = int(results[0])
        negative = int(results[1])

    if sentiString == "":
        positive = 1
        negative = -1


    return positive, negative


def tweets_update_sentiment():
    '''
    Update tweet's JSON with positive and
    negative sentiment
    '''

    # take the text of the tweet
    text = tweet["text_tokenized_without_stopwords"]
    # convert from list to str
    text = ' '.join(text)
    # compute the sentiment strength
    pos, neg = RateSentiment(text)

    # update tweet
    db[collection].update(
        {
            "id": tweet["id"]
        },
        {
            "$set": {
                "positive": pos,
                "negative": neg
            }
        }
    )


def replies_update_sentiment():
    '''
    Update reply's JSON with positive and
    negative sentiment
    '''

    # take the reply of the tweet
    text = reply["text_tokenized_without_stopwords"]

    # convert from list to str
    text = ' '.join(text)

    # compute the sentiment strength
    pos1, neg1 = RateSentiment(text)

    # update reply
    db[collection].update(
        {
            "id": tweet["id"],
            "replies.id": reply["id"]
        },
        {
            "$set": {
                "replies.$.positive": pos1,
                "replies.$.negative": neg1
            }
        }
    )


for collection in collections:
    tweets = db[collection].find().batch_size(10)
    counter_tweets = 1                 # counter for preprocessed tweets
    counter_replies = 1                # counter for preprocessed replies

    for tweet in tweets:
        tweets_update_sentiment()
        print('Processing', tweet["id"], 'tweet', '[' + str(counter_tweets) + ']')
        counter_tweets += 1

        # take the replies of tweets
        replies_count = db[collection].find_one({'id': tweet["id"]})["replies_count"]
        # if replies of the tweet exist, then preprocess them
        if replies_count > 0:
            replies = db[collection].find_one({'id': tweet["id"]})["replies"]

            for reply in replies:
                replies_update_sentiment()
                print('Processing', reply["id"], 'reply', '[' + str(counter_replies) + ']')
                counter_replies += 1
