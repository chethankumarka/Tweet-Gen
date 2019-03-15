"""
The script prepares a dataset consisting of reply for each tweet based on user supported views - left/right 

1. First find out the pool of left and right users separately.
2. For each of the pool, then extract the tweet ids and replies.

replyto table

        tid         | screen_name_from | screen_name_to  |   repliedto_tid    
--------------------+------------------+-----------------+--------------------
 968913716967243776 | your__own__risk  | rial_rocks      | 968912203083649024

tweet table

        tid         |        uid         |   screen_name   |                                                                                                                                        tweet                                                                                                                                         | is_retweet |       timestamp        |          gnip_predicted_location          | fav_count | retweet_count | quote_count | reply_count | possibly_sensitive 
--------------------+--------------------+-----------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------+------------------------+-------------------------------------------+-----------+---------------+-------------+-------------+--------------------
 968662285286699009 |          132339474 | EdKrassen       | After Bill Clinton implemented an assault weapons ban in 1994, deaths due to mass shootings fell by 43%.  Then after the GOP lifted the ban, mass shooting deaths more than doubled.   People didn't get more mentally ill during this time! GET IT? The problem is Assault Weapons! | f          | 2018-02-28 00:41:00-08 |                                           |     12737 |          6589 |         200 |         214 | f

"""

import psycopg2

conn = psycopg2.connect("dbname=Gun_Debate user=postgres password=test")
cur = conn.cursor()


def extract_screen_names(ideology):
    global cur
 
    screen_names = []
    cur.execute("SELECT screen_name FROM user_label WHERE label = (?)", ideology)
    rows = cur.fetchall()
 
    for row in rows:
    	screen_names.append(row[0])

    return screen_names

def extract_uids(screen_names):
	global cur
 
    uids = []
    cur.execute("SELECT uid FROM tweet WHERE screen_name in (?)", screen_names)
    rows = cur.fetchall()
 
    for row in rows:
		uids.append(row[0])

    return uids

def extract_tweets(uids):
    global cur
 
    tweets = []
    cur.execute("SELECT tid, tweet FROM tweet WHERE uid in (?)", uids)
    rows = cur.fetchall()
 
    for row in rows:
        tweets.append((row[0], row[1]))

    return tweets

def create_dataset(file_handle, tweets):
    global cur

    for tweet_tuple in tweets:
        cur.execute("SELECT tid FROM replyto where repliedto_tid = (?)", tweet_tuple[0])
        rows = cur.fetchall()

        reply_ids = []
        for row in rows:
            reply_ids.append(row[0])

        for reply_id in reply_ids:
            cur.execute("SELECT tweet FROM tweet where tid = (?)", reply_id)
            rows = cur.fetchall()
            reply = rows[0][0]
            file_handle.write(tweet_tuple[1] + "\t" + reply + "\n")

left_screen_names = extract_screen_names("left")
left_uids = extract_uids(left_screen_names)

right_screen_names = extract_screen_names("right")
right_uids = extract_uids(right_screen_names)

tweets = []
replies = []

left_tweets = extract_tweets(left_uids)
right_tweets = extract_tweets(right_uids)

left_tweet_dataset = open("left_tweet_dataset.tsv", "w")
create_dataset(left_tweet_dataset, left_tweets)

right_tweet_dataset = open("right_tweet_dataset.tsv", "w")
create_dataset(right_tweet_dataset, right_tweets)