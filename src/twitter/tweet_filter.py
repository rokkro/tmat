try:
    import config, string, datetime
    from difflib import SequenceMatcher
except ImportError as e:
    print("Error:", e)
    quit()

def format_date(json_date):
    current =  datetime.datetime.strptime(json_date,'%a %b %d %H:%M:%S +%f %Y')
    valid = datetime.datetime(year=current.year,month=current.month,day=current.day,hour=0,minute=0,second=0,microsecond=0)
    return valid.date()

def strip_all(text):
    return text.translate(text.maketrans('','',string.punctuation)).replace(" ","")

def duplicate_tests(coll_tweet, json_tweet):
    cfaves = int(coll_tweet['favorite_count'])
    jfaves = int(json_tweet['favorite_count'])
    if config.verbose:
        print("COLL FAVES:",coll_tweet['favorite_count'],"NEW TWEET FAVES:",json_tweet['favorite_count'])
        print("COLL DATE:", coll_tweet['created_at'], "NEW TWEET DATE:", json_tweet['created_at'])
    if  cfaves > jfaves :
        return False
    elif cfaves == jfaves:
        if format_date(coll_tweet['created_at']) <= format_date(json_tweet['created_at']):
            return False
        return True
    else:
        return True
    #returning false means we keep the collection tweet

def duplicate_find(coll, json_tweet, sim):
    # coll_tweet is already saved in the db, json_tweet is the new one
    #cursor = coll.find({'$text': {'$search': json_tweet['text']}}, {'score': {'$meta': 'textScore'}})
    #utilize text index set to the 'text' field in tweet_setup.py to get data
    #cursor.sort([('score', {'$meta': 'textScore'})]) #sort by similarity. Not necessary I guess.
    cursor = coll.find({})
    for coll_tweet in cursor:  # searching for all tweets' text, removing spaces and punct.
        if 'text' not in coll_tweet:
            continue
        coll_stripped = strip_all(coll_tweet['text'])
        json_stripped = strip_all(json_tweet['text'])
        sim_ratio = SequenceMatcher(None, coll_stripped, json_stripped).ratio()

        if sim_ratio > sim:
            if duplicate_tests(coll_tweet, json_tweet):
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
                      json_tweet['user']['screen_name'] + " ignored.") #MongoDB textScore:",coll_tweet['score'])
                print(" FIRST: " + coll_tweet['text'] + " SECOND: " + json_tweet['text'])
            cursor.close()
            return False #do not insert the new tweet into the db since it's a duplicate

    cursor.close()
    return True  # if no duplicates found


def social_filter(json_data):  # removes certain tweets
    if "created_at" not in json_data or "retweeted_status" in json_data or \
                    "quoted_status" in json_data or json_data["in_reply_to_user_id"] != None:
        return False
    return True  # does NOT affect tweet streaming. Whether or not tweet saved


def date_filter(json_data,after):
    date = json_data["created_at"]
    valid = format_date(date)
    if valid < after:
        if config.verbose:
            print("JSON DATE:", valid, "INPUT DATE:", after)
        return False
    return True
