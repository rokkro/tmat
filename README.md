To use: insert correct Twitter (tweet streaming) and/or Kairos (image analysis) API keys into the `config.py` file, then run `menu_main.py` for the menu interface.

Install mongoDB and run with `mongod --dbpath=/path/to/db` (Find `mongod.exe` in Program Files on Windows).
Use something like Robomongo for a nice visual view of the data.
  
Requires Python 3.x, tested on 3.5/3.6.

Modules: `tweepy`,`nltk`,`requests`,`pymongo`


1. Twitter tweet streaming. [x]
2. Set up MongoDB system. [x]
3. Check tweet duplicates. [x]
4. Sentiment analaysis (<a href="https://github.com/cjhutto/vaderSentiment">Vader Sentiment</a>) [x]
5. Associate characteristics using Kairos to tweets + users. [x]
6. Export to .csv spreadsheets. [x]
7. Historical tweet gathering. [x]


## Notes:
  #### Menus:
1.  Menus are designed to make it simple to use this program. They will, however, generate an unholy amount of console ouput from navigation.
2.  Run `menu_main.py` for complete access to all the menus/functions.

  #### Config.py:
1.  Enter your Twitter API and Kairos API keys into `config.py`.
2.  `verbose` set to `True` outputs far more console output, letting you see what's going on.
3.  `startup_connect` determines whether MongoDB attempts to connect on the program's startup.

  #### MongoDB:
1.  Tweets are placed in MongoDB databases. These databases contain collections, and these collections contain documents.
2.  A document will contain the Twitter API data, the Kairos API data, the Vader Sentiment data, and anything else that is inserted.
      A document is basically a JSON file, but in binary format - a <a href="https://docs.mongodb.com/manual/core/document/">BSON</a>.
3.  When a collection is marked as temporary, a single document is created with the value `"t_temp" : True`. 
      This makes it easier to delete a group of collections later using the "Manage Collections" menu later.
4.  MongoDB must be running to use most of the functions of this program.
5.  I don't reccomend you modify, delete, or insert into the `local` or `admin` collections unless you know what you're doing.

  #### Tweet Streaming:
 1.  Tweepy is used as the Python module to interface with the Twitter API.
 2.  Retrieves new tweets created while the program is running.
 3.  Filters out retweets, quoted retweets, replies, and incomplete tweets(does not contain "created_at" date in JSON data).
 4.  Finds duplicates in same collection by removing punctuation and spaces from tweet to be checked, 
      then getting all tweets from the same Twitter user. All of their tweets have punct. and spaces removed. Exact duplicates, and 
      similar tweets(defined by the similarity threshold, and compared using the Python `SequenceMatcher`) are ignored.
 5. Tweet data from the Twitter API is inserted into the specified MongoDB database and collection, in a JSON-like format.
 6. Incomplete Read error occurs when the API needs to "catch up" to the latest tweets. Some tweets are skipped when this occurs.
      Adding more filters (language, follower, etc.) supposedly increases the frequency of this error.
 7. Queries using both the follower and search term options, will retrieve ANY new tweets from the specified user, and ANY  new tweets
    from any user who tweets the specified search term.
    
  #### Historic Tweet Gathering:
1.  Much of the same applies from the "Tweet Streaming" section. Tweepy is used to gather tweets.
2.  Gathers tweets with the specified search term. <a href="https://dev.twitter.com/rest/public/search">Operators</a> may be used.
3.  A 'before' date may be specified up to 7 days (as far back as the Twitter API allows). This setting gathers tweets until the set date. More testing is needed to verify, but it seems to gather tweets before the date entered (<). An 'on/after' date can be set in the same menu. This is used to filter out tweets as they are recieved with their `created_at` date attribute. The 'on/after' date works in a (>=) way. You can use these two date types together to set up a way to get tweets within a time period, in a format like: `A-YYYY-MM-DD || B-YYYY-MM-DD`. One, both, or neither dates can be entered.
4.  A <a href="https://dev.twitter.com/rest/reference/get/search/tweets">result type</a> can be set to set the types of tweets gathered: 'popular' only returns the most popular tweets, 'recent' only returns the most recent, and 'mixed' (the default) returns a combination of real time and popular tweets.
5. Note that changing the result type (and date) may result in fewer returned tweets since, say, there are only so many popular tweets from the search.
6. Tweets are filtered out in exactly the same way as explained with Tweet Streaming: by RT, quote, reply, and using the duplicate checking methods.
7. Tweets are gathered <a href="https://dev.twitter.com/rest/public/timelines">100 at a time</a>, until the specific limit requires fewer tweets to be gathered. See the above link(s) for an idea how Twitter returns these tweets. The `max_id` is found the help the API determine where and when to continue tweet retrieval/where it left off. These tweets are then filtered using the above methods, and the successful tweets are counted and inserted into the database.
8. The API rate limit will be hit after so many tweets are retrieved. Tweepy automatically will pause/sleep until it can continue.

  #### Sentiment Analysis with Vader Sentiment:
1.  The NLTK Python module is used with <a href="https://github.com/cjhutto/vaderSentiment">Vader Sentiment</a>.
      Specifically, `subjectivity`, `vader_lexicon`, and `punkt` are used with the Naive Bayes Classifier to train it to understand
      tweet content.
2.  Four values are found from analysis: the positivity, negativity, and neutrality of the tweet. 
      In addition, the compound value is calculated: see the Vader Sentiment link above for an explanation.
3.  These values are inserted in each tweet document in the specified collection under `sentiment` : (`pos`,`neg`,`neu`, and `compound`).

  #### Facial Analysis with Kairos:
1.  The Kairos facial detection and emotion/age/gender APIs are used.
2.  The profile image URL is taken from the current document in the collection, and is tested if it exists.
3.  The current doc is checked for `default_profile_image` being false, and if the URL does not contain a 'default' picture URL.
4.  The current image is individually downloaded as `ta-image.jpg`, then is uploaded to the Kairos detect API.
5.  If the API does not find a face, then the next document repeats this process (overwriting `ta-image.jpg` with each new image).
6.  If a face is found, the image is then uploaded and run through the Kairos emotion API. 
7.  Data from the detection and emotion API are inserted into the current document under `face` : (`detection` and `emotion`)
8.  When the final image is processed, `ta-image.jpg` is deleted. If an error occurs the image is deleted.
9.  Occasionally, the Kairos API will return facial detection data, but not emotion data.
10. The older the collection, the more dead profile pic links.

  #### CSV Export:
1.  Column headings are manually defined within the `headers` list in `export.py`.
2.  The values are serached for within the current document. If they exist, the values are directly inserted into the `data` list. If they do not exist, a blank is inserted.
3.  Before being added to `data`, the emotion values are compared with one another for the highest value. Whatever the highest value refers to is inserted into the list. The same is done with the ethnicity values provided by the Kairos API. 
4.  The `rightEyeCenterX` is subtracted from `leftEyeCenterX` (or is it the other way around?) for the `eyegap`, which is then inserted into `data`.
5.  The `data` list is then written to the CSV file as a single row (the current document). This process is repeated for every document in the collection.
