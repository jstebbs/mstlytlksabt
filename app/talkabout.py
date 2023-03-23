import os

import tweepy
import nltk
from nltk.corpus import stopwords
from dotenv import load_dotenv

load_dotenv()

# Authenticate with the Twitter API
consumer_key = os.getenv("API_KEY")
consumer_secret = os.getenv("API_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_SECRET")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


def talkingabout(username):
# Retrieve tweets from a user
#username = "@KylieJenner"
    tweets = api.user_timeline(screen_name=username, count=2000)




    new_stopwords = ["it","and","the","http","https", "co", "com", "org", "net", "&amp;", "rt", "-", "new","--"]

    stpwrd = nltk.corpus.stopwords.words('english')
    stpwrd.extend(new_stopwords)


    text = " ".join([tweet.text for tweet in tweets])
    text = text.lower()
    text = " ".join([word for word in text.split() if word not in stpwrd])

    from sklearn.decomposition import LatentDirichletAllocation
    from sklearn.feature_extraction.text import CountVectorizer

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(text.split())
    feature_names = vectorizer.get_feature_names_out()


    lda = LatentDirichletAllocation(n_components=3, random_state=0)
    lda.fit(X)
    topics = lda.components_
    top_words = vectorizer.get_feature_names_out()

    from collections import Counter
    import heapq

    word_counts = Counter(text.split())
    top_words = heapq.nlargest(3, word_counts, key=word_counts.get)
    top_words_str = ', '.join(["'" + word + "'" for word in top_words[:-1]]) + ', and ' + "'" + top_words[-1] + "'"
    text = f".{username} mostly talks about\n {top_words_str}."
    return text

    #for topic in topics:
        #print(" ".join([top_words[i] for i in topic.argsort()[:-3 - 1:-1]]))
