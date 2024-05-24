import feedparser
from tweepy import errors
import tweepy
import re
import os

# API keys
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")


# Keywords and their different forms in your language
KEYWORD_REGEX = re.compile(r'\bvantaalaismie\w*', re.IGNORECASE)

# List of RSS feed URLs
RSS_URLS = [
    'https://feeds.yle.fi/uutiset/v1/recent.rss?publisherIds=YLE_UUTISET',
    'http://aamulehti.fi/uutiset/pirkanmaa/rss.xml',
    'http://www.hs.fi/rss/teasers/etusivu.xml',
    'https://www.is.fi/rss/uutiset.xml',
    'https://www.iltalehti.fi/rss/uutiset.xml',
    'https://feeds.kauppalehti.fi/rss/main',
    'https://feeds.kauppalehti.fi/rss/klnyt',
    'https://www.ts.fi/rss.xml',
    'https://www.talouselama.fi/api/feed/v2/rss/te'    
]

# File to store tweeted article URLs
TWEETED_URLS_FILE = 'tweeted_urls.txt'

# Hashtag to include in tweets
HASHTAG = '#Vantaalaismies'

def authenticate_twitter():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)

def load_tweeted_urls():
    if not os.path.exists(TWEETED_URLS_FILE):
        return set()
    with open(TWEETED_URLS_FILE, 'r') as file:
        return set(line.strip() for line in file)

def save_tweeted_url(url):
    with open(TWEETED_URLS_FILE, 'a') as file:
        file.write(f"{url}\n")

def match_keyword(title):
    return KEYWORD_REGEX.search(title) is not None

def fetch_and_tweet():
    twitter_api = authenticate_twitter()
    tweeted_urls = load_tweeted_urls()

    for rss_url in RSS_URLS:
        feed = feedparser.parse(rss_url)
        for entry in feed.entries:
            if entry.link not in tweeted_urls and match_keyword(entry.title):
                tweet_text = f"{entry.title} {entry.link} {HASHTAG}"
                try:
                    twitter_api.update_status(tweet_text)
                    print(f"Tweeted: {tweet_text}")
                    save_tweeted_url(entry.link)
                except errors.TweepyException as e:
                    print(f"Error: {e}")
                    
def main():
    fetch_and_tweet()
    
main()