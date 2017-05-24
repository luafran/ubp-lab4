import sys
import requests
import requests_oauthlib
import json

import settings

my_auth = requests_oauthlib.OAuth1(settings.CONSUMER_KEY,
                                   settings.CONSUMER_SECRET,
                                   settings.ACCESS_TOKEN,
                                   settings.ACCESS_SECRET)


def get_tweets_stream():

    # Use stream API
    url = 'https://stream.twitter.com/1.1/statuses/filter.json'
    # query_data = [('language', 'en'), ('locations', '-130,-20,100,50'), ('track', '#ubplab4')]
    query_data = [('language', 'en'), ('track', '%23ubplab4')]

    # url = 'https://api.twitter.com/1.1/search/tweets.json'
    # query_data = [('q', '%23ubplab4')]

    query_url = url + '?' + '&'.join([str(t[0]) + '=' + str(t[1]) for t in query_data])
    response = requests.get(query_url, auth=my_auth, stream=True)
    print(query_url, response)
    print ("------------------------------------------")
    return response


def process_tweets_stream(http_resp):
    for line in http_resp.iter_lines():
        try:
            if len(line) > 0:
                full_tweet = json.loads(line)
                tweet_text = full_tweet['text']
                print("Tweet Text: " + tweet_text)
                print ("------------------------------------------")
        except:
            e = sys.exc_info()[0]
            print("Error: %s" % e)
            print("line: %s" % line)


def get_tweets_search():

    url = 'https://api.twitter.com/1.1/search/tweets.json'
    query_data = [('q', '%23ubplab4')]

    query_url = url + '?' + '&'.join([str(t[0]) + '=' + str(t[1]) for t in query_data])
    response = requests.get(query_url, auth=my_auth, stream=True)
    print(query_url, response)
    print ("------------------------------------------")
    return response


def process_tweets_search(http_resp):
    for line in http_resp.iter_lines():
        try:
            if len(line) > 0:
                full_response = json.loads(line)
                for full_tweet in full_response['statuses']:
                    tweet_text = full_tweet['text']
                    print("Tweet Text: " + tweet_text)
                    print ("------------------------------------------")
        except:
            e = sys.exc_info()[0]
            print("Error: %s" % e)
            print("line: %s" % line)


print("Processing tweets...")
resp = get_tweets_stream()
process_tweets_stream(resp)
# resp = get_tweets_search()
# process_tweets_search(resp)
