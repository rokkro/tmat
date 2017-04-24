To use: insert correct Twitter (tweet streaming) and/or Kairos (image analysis) API keys into the `config.py` file, then run `menu_main.py`, which is a menu interface.

Install mongoDB and run with `mongod --dbpath=/path/to/db`.

Requires Python 3.x, tested on 3.5/3.6.

1. Twitter tweet streaming [x]  - queue system found to be unnecessary, rarely tweets will be skipped to catch up.
2. Set up MongoDB system [x]
3. Check tweet duplicates [x] - Checks for exact duplicates and by similarity user can modify (default 55%) within same collection.
4. Sentiment analaysis [x] - Basic <a href="https://github.com/cjhutto/vaderSentiment">Vader Sentiment</a> implemented.
5. Associate characteristics using Kairos to tweets + users. [x]
6. Export to .csv spreadsheets. [x]
7. Historical tweet gathering 

## Notes:

  #### Tweet Streaming:
 1.  Tweepy is used as the Python module to interface with the Twitter API.
 2.  Retrieves new tweets created while the program is running.
 3.  Filters out retweets, quoted retweets, replies, and incomplete tweets(does not contain "created_at" in JSON data).
 4.  Finds duplicates in same collection by removing punctuation and spaces from tweet to be checked, 
      then getting all tweets from the same Twitter user. All of their tweets have punct. and spaces removed. Exact duplicates, and 
      similar tweets(defined by the similarity threshold) are ignored.
 5. Tweet data from the Twitter API is inserted into the specified MongoDB database and collection, in a JSON-like format.
 6. Incomplete Read error occurs when the API needs to "catch up" to the latest tweets. Some tweets are skipped when this occurs.
      Adding more filters (language, follower, etc) supposedly increases the frequency of this error.
 7. Queries using both the follower and search term options, will retrieve ANY new tweets from the specified user, and ANY tweets
    from any user who tweets the specified search term.
