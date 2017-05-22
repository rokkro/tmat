try:
    import config, string, datetime
    from difflib import SequenceMatcher
except ImportError as e:
    print("Error:", e)
    quit()

def duplicate_find(coll,json_data,sim):
    cursor = coll.find({'user.screen_name': json_data['user']['screen_name']})
    for c in cursor:  # searching for exact same tweets from same user, removing spaces and punct.
        coll_tweet = c['text'].translate(c['text'].maketrans('', '', string.punctuation)).replace(" ", "")
        json_tweet = json_data['text'].translate(json_data['text'].maketrans('', '', string.punctuation)).replace(
            " ", "")

        if coll_tweet == json_tweet:
            if config.verbose:
                print(" FIRST: " + c['text'] + " SECOND: " + json_data['text'])
                print("\nDuplicate tweet from " + "@" + json_data['user']['screen_name'] + " ignored.")
            cursor.close()
            return False
        elif SequenceMatcher(None, coll_tweet, json_tweet).ratio() > sim:
            if config.verbose:
                print("\n" + str(SequenceMatcher(None, coll_tweet, json_tweet).ratio() * 100) + "% similar existing"
                                                                                                " tweet from " + "@" +
                      json_data['user']['screen_name'] + " ignored.")
                print(" FIRST: " + c['text'] + " SECOND: " + json_data['text'])
            cursor.close()
            return False

    cursor.close()
    return True  # if no duplicates found


def social_filter(json_data):  # removes certain tweets
    if "created_at" not in json_data or "retweeted_status" in json_data or \
                    "quoted_status" in json_data or json_data["in_reply_to_user_id"] != None:
        return False
    return True  # does NOT affect tweet streaming. Whether or not tweet saved


def date_filter(json_data,after):
    date = json_data["created_at"]
    current = datetime.datetime.strptime(date,'%a %b %d %H:%M:%S +%f %Y')
    valid = datetime.datetime(year=current.year,month=current.month,day=current.day,hour=0,minute=0,second=0,microsecond=0)
    if valid.date() < after:
        return False
    return True
