import json
import logging
import sys
import time

import requests
import requests_oauthlib
import requests.exceptions
import tweepy

import settings

logger = logging.getLogger('twitter_app')
logger.setLevel(logging.DEBUG)
logger.propagate = False
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

my_auth = requests_oauthlib.OAuth1(settings.CONSUMER_KEY,
                                   settings.CONSUMER_SECRET,
                                   settings.ACCESS_TOKEN,
                                   settings.ACCESS_SECRET)


def get_tweets_stream(tag, duration):

    logger.info('get_tweets_stream')
    # Use stream API
    url = 'https://stream.twitter.com/1.1/statuses/filter.json'
    # query_data = [('language', 'en'), ('locations', '-130,-20,100,50'), ('track', '#ubplab4')]
    hash_tag = '%23{0}'.format(tag)
    query_data = [('track', hash_tag)]

    query_url = url + '?' + '&'.join([str(t[0]) + '=' + str(t[1]) for t in query_data])
    logger.debug('doing request')
    try:
        response = requests.get(query_url, auth=my_auth, stream=True, timeout=duration)
        logger.debug((query_url, response))
    except requests.exceptions.Timeout:
        logger.debug('TIMEOUT!')
        raise SystemExit(0)
    except requests.exceptions.ConnectionError as ex:
        logger.debug('exception: {}'.format(ex))

    return response


def process_tweets_stream(http_resp):
    logger.info('process_tweets_stream')
    try:
        for line in http_resp.iter_lines():
            try:
                if len(line) > 0:
                    full_tweet = json.loads(line)
                    tweet_text = full_tweet['text']
                    logger.debug("------------------------------------------")
                    logger.debug("Tweet Text: " + tweet_text)
                    logger.debug("------------------------------------------")
                else:
                    logger.debug('keep-alive')
            except:
                e = sys.exc_info()[0]
                print("Error: %s" % e)
                print("line: %s" % line)

    except requests.exceptions.Timeout:
        logger.debug('TIMEOUT!')
        raise SystemExit(0)
    except requests.exceptions.ConnectionError as ex:
        logger.debug('ConnectionError')
        logger.debug('exception: {}'.format(ex))


class MyStreamListener(tweepy.StreamListener):

    def __init__(self, duration):
        tweepy.StreamListener.__init__(self)
        self.duration = duration
        self.start_time = None
        self.end_time = None
        self.count = 0

    def on_connect(self):
        self.start_time = time.time()
        self.end_time = self.start_time + self.duration
        logger.debug('on_connect: starting to collect tweets. start_time: {}, end_time: {}'.
                     format(self.start_time, self.end_time))

    def on_status(self, status):
        logger.debug('on_status')
        now = time.time()
        if now > self.end_time:
            return False
        else:
            logger.debug(status.text)
            self.count += 1
            return True

    def keep_alive(self):
        logger.debug('keep_alive')
        now = time.time()
        if now > self.end_time:
            return False
        else:
            return True

    def on_timeout(self):
        logger.debug('on_timeout')
        now = time.time()
        if now > self.end_time:
            return False
        else:
            return True

    def on_error(self, status_code):
        logger.error('status_code: {}'.format(status_code))
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False


def get_tweets_stream_2(tag, duration):
    logger.info('get_tweets_stream_2')

    auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_SECRET)

    my_stream_listener = MyStreamListener(duration)
    # Use small chunk_size to receive keep-alive from Twitter
    my_stream = tweepy.Stream(auth=auth, listener=my_stream_listener, chunk_size=10)
    my_stream.filter(track=[tag], async=False)
    my_stream.disconnect()
    logger.info('track: {}, duration: {}, count: {}'.format(tag, duration, my_stream_listener.count))


def get_tweets_search(tag):
    logger.info('get_tweets_search')

    url = 'https://api.twitter.com/1.1/search/tweets.json'
    hash_tag = '%23{0}'.format(tag)
    query_data = [('q', hash_tag)]

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


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) < 3:
        print 'usage: {0} stream|search hashtag (without #) time'.format(sys.argv[0])
        raise SystemExit(1)

    mode = args[0]
    tag_arg = args[1]
    duration_arg = int(args[2])

    logger.debug('mode: {}, tag: {}, duration: {}'.format(mode, tag_arg, duration_arg))

    if mode == 'stream':
        resp = get_tweets_stream(tag_arg, duration_arg)
        process_tweets_stream(resp)
    elif mode == 'stream2':
        get_tweets_stream_2(tag_arg, duration_arg)
    elif mode == 'search':
        resp = get_tweets_search(tag_arg)
        process_tweets_search(resp)
    else:
        print 'usage: {0} stream|search hashtag (without #)'.format(sys.argv[0])
        raise SystemExit(1)
