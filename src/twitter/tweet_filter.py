try:
    import config, datetime, string
    from difflib import SequenceMatcher
except ImportError as e:
    print("Import Error in tweet_filter.py:", e)

def format_date(json_date):
    # Reformat data from twitter format to datetime format
    current =  datetime.datetime.strptime(json_date,'%a %b %d %H:%M:%S +%f %Y')
    valid = datetime.datetime(year=current.year,month=current.month,day=current.day,hour=0,minute=0,second=0,microsecond=0)
    return valid.date()

def strip_all(text):
    # Remove punctuation and spaces
    return text.translate(text.maketrans('','',string.punctuation)).replace(" ","")

def duplicate_tests(coll_tweet, json_tweet):
    # Extra duplicate checking tests, returning false means we keep the collection tweet
    cfaves = int(coll_tweet['favorite_count'])
    jfaves = int(json_tweet['favorite_count'])
    if config.verbose:
        print("COLL FAVES:",coll_tweet['favorite_count'],"NEW TWEET FAVES:",json_tweet['favorite_count'])
        print("COLL DATE:", coll_tweet['created_at'], "NEW TWEET DATE:", json_tweet['created_at'])
    if cfaves > jfaves: # Keep the tweet in the collection w/ more faves
        return False
    elif cfaves == jfaves: # Keep the older tweet if have same fave count
        if format_date(coll_tweet['created_at']) <= format_date(json_tweet['created_at']):
            return False
        return True
    else: # Keep new tweet since it has more faves
        return True

def duplicate_find(coll, json_tweet):
    """
    See README!
    coll_tweet is already saved in the db, json_tweet is the new one
    Utilizes MongoDB's textScore, sorting by similarity, only providing top matches (set in config file how many)
    """
    cursor = coll.find({'$text': {'$search': json_tweet['text']}}, {'score': {'$meta': 'textScore'}})
    cursor = cursor.sort([('score', {'$meta': 'textScore'})]).limit(config.tweet_duplicate_limit) #sort all by similarity, only give us so many
    for iterator,coll_tweet in enumerate(cursor):  # searching for all tweets' text, removing spaces and punct.
        if 'text' not in coll_tweet:
            continue
        coll_stripped = strip_all(coll_tweet['text'])
        json_stripped = strip_all(json_tweet['text'])
        sim_ratio = SequenceMatcher(None, coll_stripped, json_stripped).ratio() # Compare tweet content
        if sim_ratio > config.tweet_similarity_threshold: # If the text is similar
            #print("\n",iterator)
            if duplicate_tests(coll_tweet, json_tweet): # Compare them this way, True = delete coll tweet
                try:
                    coll.delete_one({"_id":coll_tweet["_id"]})
                except Exception as e:
                    print(e)
                cursor.close()
                if config.verbose:
                    print("Old tweet deleted! Keeping new one.")
                return True
            if config.verbose:
                print("\n" + str(sim_ratio * 100) + "% similar existing. Tweet from " + "@" +
                      json_tweet['user']['screen_name'] + " ignored.MongoDB textScore:",coll_tweet['score']) #MongoDB textScore:",coll_tweet['score'])
                print(" FIRST: " + coll_tweet['text'] + " SECOND: " + json_tweet['text'])
            cursor.close()
            return False # Do not insert the new tweet into the db since it's a duplicate
    cursor.close()
    return True  # if no duplicates found


def social_filter(json_data):
    # Ignores RT's, Quotes, Replies, and dead tweets
    if "created_at" not in json_data or "retweeted_status" in json_data or \
                    "quoted_status" in json_data or json_data["in_reply_to_user_id"] != None:
        return False
    return True  # does NOT affect tweet streaming. Whether or not tweet saved


def date_filter(json_data,after):
    # Date comparison checker
    date = json_data["created_at"]
    valid = format_date(date)
    if valid < after:
        if config.verbose:
            print("JSON DATE:", valid, "INPUT DATE:", after)
        return False
    return True
