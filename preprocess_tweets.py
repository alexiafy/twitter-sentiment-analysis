from pymongo import MongoClient
from nltk.corpus import stopwords
import re
from nltk.stem.snowball import SnowballStemmer


connection = MongoClient("mongodb://localhost:27017/")
db = connection.fake_news                     # name of db (it should be changed to real_news or fake_news

collections = db.collection_names()


stop_words = set(stopwords.words('english'))
stemmer = SnowballStemmer("english")


def clean_text(text):
    """
    clean_text is a method that uses regex to help in tokenization.
    :param text: It takes as input a string
    :return: returns a string
    """

    text = text.lower()
    text = re.sub(r"i'm", "i am", text)
    text = re.sub(r"he's", "he is", text)
    text = re.sub(r"she's", "she is", text)
    text = re.sub(r"it's", "it is", text)
    text = re.sub(r"that's", "that is", text)
    text = re.sub(r"what's", "what is", text)
    text = re.sub(r"where's", "where is", text)
    text = re.sub(r"how's", "how is", text)
    text = re.sub(r"\'ll", " will", text)
    text = re.sub(r"\'ve", " have", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"\'d", " would", text)
    text = re.sub(r"n't", " not", text)
    text = re.sub(r"won't", "will not", text)
    text = re.sub(r"shouldn't", "should not", text)
    text = re.sub(r"can't", "cannot", text)
    #text = re.sub(r"[-()\"/;:<>{}`+=~|.!?,]", "", text)
    text = re.sub(r"plz", "please", text)
    text = re.sub(r"evryday", "everyday", text)
    text = re.sub(r"dnt", "do not", text)
    text = re.sub(r"pls", "please", text)
    text = re.sub(r"lst", "list", text)
    text = re.sub(r"abt", "about", text)
    text = re.sub(r"im", "i am", text)
    text = re.sub(r" u ", " you ", text)
    text = re.sub(r" n ", " and ", text)
    text = re.sub(r"gv", "give", text)
    text = re.sub(r"jan", "january", text)
    text = re.sub(r"feb", "february", text)
    text = re.sub(r"mar", "march", text)
    text = re.sub(r"apr", "april", text)
    text = re.sub(r"jun", "june", text)
    text = re.sub(r"jul", "july", text)
    text = re.sub(r"aug", "august", text)
    text = re.sub(r"sep", "september", text)
    text = re.sub(r"oct", "october", text)
    text = re.sub(r"nov", "november", text)
    text = re.sub(r"dec", "december", text)
    # text = re.sub(r"1st", "first", text)
    # text = re.sub(r"2nd", "second", text)
    # text = re.sub(r"3rd", "third", text)
    # text = re.sub(r"4th", "fourth", text)
    # text = re.sub(r"5th", "fifth", text)
    text = re.sub(r"jst", "just", text)
    text = re.sub(r"knw", "know", text)
    return str(text)


def preprocess_tweet():
    '''
    Preprocess tweet
    '''

    # clean text
    text_cleaned = clean_text(tweet['text'])
    # tokenization
    tokens = text_cleaned.split()
    # remove words starting with http prefix (urls), @ prefix (mentions), # prefix (hashtags)
    tokens = [token for token in tokens if not token.startswith('http')
              if not token.startswith('#') if not token.startswith('@')]

    # remove stopwords
    clean_tokens = [w for w in tokens if not w in stop_words]

    # update tweet
    db[collection].update(
        {
            "id": tweet["id"]
        },
        {
            "$set": {
                "text_tokenized": tokens,
                "text_tokenized_without_stopwords": clean_tokens
            }
        }
    )


def preprocess_reply():
    '''
    Preprocess reply
    '''

    # clean text
    text_cleaned = clean_text(reply['text'])
    # tokenization
    tokens = text_cleaned.split()
    # remove words starting with http prefix (urls), @ prefix (mentions), # prefix (hashtags)
    tokens = [token for token in tokens if not token.startswith('http')
              if not token.startswith('#') if not token.startswith('@')]

    # remove stopwords
    clean_tokens = [w for w in tokens if not w in stop_words]

    # update reply
    db[collection].update(
        {
            "id": tweet["id"],
            "replies.id": reply["id"]
        },
        {
             "$set": {
                 "replies.$.text_tokenized": tokens,
                 "replies.$.text_tokenized_without_stopwords": clean_tokens
             }
        }
    )


for collection in collections:
    tweets = db[collection].find().batch_size(10)
    counter_tweets = 1                 # counter for preprocessed tweets
    counter_replies = 1                # counter for preprocessed replies

    for tweet in tweets:
        preprocess_tweet()
        print('Preprocessing', collection, 'tweet', '[' + str(counter_tweets) + ']')
        counter_tweets += 1

        # take the replies of tweets
        replies_count = db[collection].find_one({'id': tweet["id"]})["replies_count"]
        # if replies of the tweet exist, then preprocess them
        if replies_count > 0:
            replies = db[collection].find_one({'id': tweet["id"]})["replies"]

            for reply in replies:
                preprocess_reply()
                print('Preprocessing', collection, 'reply', '[' + str(counter_replies) + ']')
                counter_replies += 1






