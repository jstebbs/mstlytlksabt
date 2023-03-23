## PYTHON MODULE IMPORTS ##
import os
import time
from collections import deque

## MODULE DEPENDCIES ##
import tweepy
from dotenv import load_dotenv

## FILE IMPORT ##
from talkabout import *

load_dotenv()

# Now you can access the variables like this
consumer_key = os.getenv("API_KEY")
consumer_secret = os.getenv("API_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_SECRET")


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create API object
api = tweepy.API(auth)

# Create a queue to store the celebrities
usernames = deque()

# Read the celebrities list from the text file and add them to the queue
with open("usernames.txt", "r") as file:
    for line in file:
        username = line.strip()
        usernames.append(username)

while usernames:
    # Get the next celebrity from the front of the queue
    username = usernames.popleft()
    tweet = talkingabout(username)
    
    
    api.update_status(tweet)
    time.sleep(2*60*60) # Sleep for 1 hour
    #Delete the celebrity from the celebs.txt file
    with open("usernames.txt", "r") as file:
        lines = file.readlines()
    with open("usernames.txt", "w") as file:
        for line in lines:
            if line.strip() != username:
                file.write(line)