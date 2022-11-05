import argparse
import datetime
import gzip
import os
import re
import numpy as np
import sys
import time
import json
from tweepy import Stream, Client, StreamingClient, StreamRule, Paginator


def eprint(*args, **kwargs):
    """Print to stderr"""
    print(*args, file=sys.stderr, **kwargs)


class CustomStreamingClient(StreamingClient):
    total_tweets = 0
    sunset_time = datetime.datetime.now()

    def __init__(self, write=print, **kwds):
        super(CustomStreamingClient, self).__init__(**kwds)
        self.write = write
        self.sunset_time = datetime.datetime.now() + datetime.timedelta(hours=24)

    def is_maxed_out(self):
        return self.total_tweets > 0.8 * MAX_TWEETS

    def is_sunset(self):
        return datetime.datetime.now() > self.sunset_time

    def on_tweet(self, tweet):
        self.write(tweet.data)

    def on_data(self, raw_data):
        """
        on_data handles what to do when the client streams a tweet (in bytes).
        The usual behavior is to hand the tweet to self.write, which itself is
        configured in the constructor. But Twitter imposes a 500,000 tweet/month
        limit on how many tweets you can pull down through a filtered stream.
        If we get within 20% of that limit, we stop streaming. Note that you may
        be asked to pull more tweets down for assignment 2, so be careful about
        hitting the 500,000 limit too early!
        """

        # You can modify the below code to e.g. manually the adjust the rate
        # at which you pull tweets, modify the cutoff, etc.
        if self.is_maxed_out():
            eprint("Read " + str(self.total_tweets) +
                   " tweets, terminating to avoid hitting 500k maximum")
            time.sleep(1)
            self.disconnect()
            return

        if self.is_sunset():
            eprint("Process has been reading tweets for 24 hours. Terminating")
            self.disconnect()
            return

        self.write(raw_data)
        self.total_tweets += 1

    def on_error(self, status_code):
        eprint(status_code)


def retrieve_reply_tweets(id_lst: list):
    """Blablabla
    """
    count = 0
    try:
        tweet_info = twitter_client.get_tweets(ids=id_lst, tweet_fields=['referenced_tweets'])
        for tweet in tweet_info.data:
            for ref_tweet in tweet.referenced_tweets:
                if ref_tweet.type == 'replied_to':
                    print(dict({'id': tweet.id, 'replied_to_tweet_id': ref_tweet.id}))
                    count += 1
                    break
        eprint(count)
    except:
        eprint('smth went wrong')
    #conversation_id_str = "conversation_id:" + \
    #    str(og_tweet['tweet_info']['conversation_id'])
    #count = og_tweet['tweet_info']['public_metrics']['reply_count']
    # Run query to get tweets
    #eprint("Getting reply tweets for " + conversation_id_str + " estimated replies: " + str(count))
    #try:
    #    paginator = Paginator(twitter_client.search_recent_tweets,
    #                          query=conversation_id_str,
    #                          expansions=[
    #                              'author_id', 'entities.mentions.username', 'in_reply_to_user_id'],
    #                          tweet_fields=['conversation_id',
    #                                        'created_at', 'public_metrics', 'in_reply_to_user_id'],
    #                          user_fields=['public_metrics', 'verified'],
    #                          max_results=100)
    #    includes = {}
    #    for response in paginator:
    #        includes = response.includes['users'][0].data if 'users' in response.includes.keys() else {}
    #        break
    #    for tweet in paginator.flatten():
    #        full_object = {}
    #        full_object['user_info'] = includes
    #        full_object['tweet_info'] = tweet.data
    #        print(json.dumps(full_object))

    #except KeyboardInterrupt:
    #    eprint()
    #except AttributeError:
        # Catch rare occasion when Streaming API returns None
    #    pass
    #pass


if __name__ == "__main__":
    # Set up the argument parser
    parser = argparse.ArgumentParser(
        description="Fetch data with Twitter Streaming API"
    )
    parser.add_argument(
        "--keyfile", help="file with user credentials", required=True)
    parser.add_argument(
        "--gzip", metavar="OUTPUT_FILE", help="file to write compressed results to"
    )
    flags = parser.parse_args()

    # Write tweets to stdout or a gzipped file, as requested
    if flags.gzip:
        # Write to gzipped file
        f = gzip.open(flags.gzip, "wb")
        eprint("Writing gzipped output to %s" % flags.gzip)
        sep = os.linesep.encode()
        def output(x): return f.write(x + sep)
    else:
        # write to stdout
        output = print

    # Read twitter app credentials and set up authentication
    creds = {}
    for line in open(flags.keyfile, "r"):
        row = line.strip()
        if row:
            key, value = row.split()
            creds[key] = value

    twitterstream = Stream(
        creds["api_key"], creds["api_secret"], creds["token"], creds["token_secret"]
    )

    # Track time and start streaming
    starttime = datetime.datetime.now()
    twitter_streaming_client = CustomStreamingClient(
        write=output, bearer_token=creds["bearer_token"])
    twitter_client = Client(
        bearer_token=creds["bearer_token"], wait_on_rate_limit=True)

    # Clear out old rules
    old_rules = twitter_streaming_client.get_rules()
    if old_rules.data is not None:
        rule_ids = [rule.id for rule in old_rules.data]
        twitter_streaming_client.delete_rules(rule_ids)

    # Start streaming
    eprint("Started running at", starttime)
    id_100_list = []
    for line in sys.stdin:
        og_tweet = json.loads(line)
        id_100_list.append(og_tweet['tweet_info']['id'])
        if len(id_100_list) == 100:
            retrieve_reply_tweets(id_100_list)
            id_100_list = []

    if len(id_100_list) != 0:
        retrieve_reply_tweets(id_100_list)
        
    if flags.gzip:
        eprint("Closing %s" % flags.gzip)
        f.close()

    eprint("total run time", datetime.datetime.now() - starttime)
