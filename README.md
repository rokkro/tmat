<p align="center">
<img src="https://cdn3.iconfinder.com/data/icons/free-social-icons/67/twitter_circle_gray-128.png">
</p>


#  Twitter Multiple Analysis Tool

**What can it do?**
* Twitter tweet streaming.
* Twitter tweet scraping (tweets approx. <=7 days old).
* Give access to plenty of search settings.
* Utilize MongoDB collections to store tweets.
* Filter out similar and duplicate tweets from the same collection.
* Perform sentiment analaysis using NLTK and <a href="https://github.com/cjhutto/vaderSentiment">Vader Sentiment</a>.
* Score tweets' readability using the Flesch-Kincaid readability tests and others.
* Use the <a href="http://kairos.com/">Kairos</a> APIs to detect emotion, age, gender, and other characteristics of profile pictures.
* Export organized data to .csv spreadsheets.
* Simple database, collection, and document management.
* Be used with a simple textual interface.

## Setup:

***To Install***: Install mongoDB and run with `mongod --dbpath=/path/to/db` (Find `mongod.exe` under `Program Files` on Windows). Clone this repo and extract the files. Make sure you've got Python 3.x (tested on 3.5/3.6) installed.

***Modules Needed***: `tweepy` (tweet collection), `nltk` (text analysis), `requests` (image analysis), `pymongo` (mongoDB), and `textstat` (readability analysis). Install these with: `pip install tweepy nltk requests pymongo textstat` or `pip3 install` (Linux + Mac OS). Use `pip install --user` on systems without admin privileges.

***To use***: insert correct <a href="https://dev.twitter.com/">Twitter</a> (tweet retrieval) and/or <a href="http://kairos.com/">Kairos</a> (image analysis) API keys into the `config.py` file, then run `menu_main.py` for the menu interface. Run with `python C:\path\to\menu_main.py` or `python3 /path/to/menu_main.py` (Linux + Mac OS). Use something like RoboMongo if you want a good visual view of your databases.

## Details:
  #### Menus:
1.  Menus are basic textual interfaces designed to make it easy to use this program. They will, however, generate an unholy amount of console ouput from navigation.
2.  Run `menu_main.py` for complete access to all the menus/functions.

  #### Config.py:
1.  Enter your Twitter API and Kairos API keys into `config.py`, within the quotation marks.
2.  `verbose` set to `True` outputs far more console output, letting you see what's going on.
3.  `startup_connect` determines whether `pymongo` attempts to connect to `mongod` on the program's startup.
4.  `tweet_similarity_threshold` sets how similar tweets must be before they are filtered out. (1=exact copies, 0=not similar)
5.  `tweet_duplicate_limit` is how many tweets are compared to the incoming tweet for duplicates. This value does not need to be high, as MongoDB sorts the most similar tweets first. Usually a duplicate is found with the first or second tweets because of this. Note that once a duplicate is found, the duplicate checking process is stopped.

  #### MongoDB:
1.  Tweets are placed in MongoDB databases. These databases contain collections, and these collections contain documents.
2.  A document will contain the Twitter API data, the Kairos API data, the Vader Sentiment data, and anything else that is inserted.
      A document is basically a JSON file, but in binary format - a <a href="https://docs.mongodb.com/manual/core/document/">BSON</a>.
3.  When a collection is marked as temporary, a single document is created with the value `"t_temp" : True`. 
      This makes it easier to delete a group of collections later using the "Manage Collections" menu later.
4.  MongoDB must be running to use most of the functions of this program.
5.  I don't reccomend you modify, delete, or insert into the `local` or `admin` collections unless you know what you're doing.

  #### Tweet Duplicates and Filtering:
 1. Filters out retweets, quoted retweets, replies, and incomplete tweets(does not contain "created_at" date in JSON data).
 2. MongoDB's cursor sorting feature is used with its "textscore" comparison values to sort the most likely duplicates first. This eliminates the need to search the entire unordered collection for a match. Instead, the max tweets searched is defined by the `tweet_duplicate_limit` in `config.py`. 
 3. Most of the time, the first tweet compared will be a duplicate.
 4. Duplicates are found by removing punctuation and spaces from the new tweet and the current tweet to be tested. Using Python's `SequenceMatcher` and the `tweet_similarity_threshold` in `config.py`, the tweet's text is compared to all other tweets in the current collection. If a duplicate is found, the two tweets are compared. The tweet with the most favorites is kept. If they have the same number of favorites, such as when tweet streaming, the older tweet is kept. 
 5. The more tweets collected, the longer duplicate checking takes. This is likely due to the slowly increasing time it takes for MongoDB to sort the tweets.
 
  #### Tweet Streaming:
 1.  Tweepy is used as the Python module to interface with the Twitter API.
 2.  Retrieves new tweets created while the program is running.
 3. Tweet data from the Twitter API is inserted into the specified MongoDB database and collection, in a JSON-like format.
 4. Incomplete Read error occurs when the API needs to "catch up" to the latest tweets. Some tweets are skipped when this occurs. Adding more search filters (language, follower, etc.) supposedly increases the frequency of this error.
 5. Queries using both the follower and search term options, will retrieve ANY new tweets from the specified user, and ANY  new tweets
    from any user who tweets the specified search term.
    
  #### Historic Tweet Gathering:
1.  Much of the same applies from the "Tweet Streaming" section. Tweepy is used to gather tweets.
2.  Gathers tweets with the specified search term. <a href="https://dev.twitter.com/rest/public/search">Operators</a> may be used.
3.  A 'before' date may be specified up to 7 days (as far back as the Twitter API allows). This setting gathers tweets until the set date. More testing is needed to verify, but it seems to gather tweets before the date entered (<). An 'on/after' date can be set in the same menu. This is used to filter out tweets as they are recieved with their `created_at` date attribute. The 'on/after' date works in a (>=) way. You can use these two date types together to set up a way to get tweets within a time period, in a format like: `A-YYYY-MM-DD || B-YYYY-MM-DD`. One, both, or neither dates can be entered.
4.  A <a href="https://dev.twitter.com/rest/reference/get/search/tweets">result type</a> can be set to set the types of tweets gathered: 'popular' only returns the most popular tweets, 'recent' only returns the most recent, and 'mixed' (the default) returns a combination of real time and popular tweets.
5. Note that changing the result type (and date) may result in fewer returned tweets since, say, there are only so many popular tweets from the search.
6. Tweets are filtered out in exactly the same way as explained with Tweet Streaming: by RT, quote, reply, and using the duplicate checking methods.
7. Tweets are gathered <a href="https://dev.twitter.com/rest/public/timelines">100 at a time</a>, until the specific limit requires fewer tweets to be gathered. See the link(s) for an idea how Twitter returns these tweets. The `max_id` is found to help the API determine where and when to continue tweet retrieval/where it left off. These tweets are then filtered using the above methods, and the successful tweets are counted and inserted into the database.
8. The API rate limit will be hit after so many tweets are retrieved. Tweepy automatically will pause/sleep until it can continue.
9. The 7 day tweet limit doesn't seem to be exact for some reason. I have recieved tweets 8 to 9 days old.

  #### Sentiment Analysis with Vader Sentiment:
1.  The NLTK Python module is used with <a href="https://github.com/cjhutto/vaderSentiment">Vader Sentiment</a>.
      Specifically, `subjectivity`, `vader_lexicon`, and `punkt` are used with the Naive Bayes Classifier to train it to understand
      tweet content.
2.  Four values are found from analysis: the positivity, negativity, and neutrality of the tweet. 
      In addition, the compound value is calculated: see the Vader Sentiment link above for an explanation.
3.  These values are inserted in each tweet document in the specified collection under `sentiment` : {`pos`, `neg`, `neu`, `compound`}.

  #### Facial Analysis with Kairos:
1.  The Kairos facial detection and emotion/age/gender APIs are used.
2.  The profile image URL is taken from the current document in the collection, and is tested if it exists.
3.  The current doc is checked for `default_profile_image` being false, and if the URL does not contain a 'default' picture URL.
4.  The current image is individually downloaded as `ta-image.jpg`, then is uploaded to the Kairos detect API.
5.  If the API does not find a face, then the next document repeats this process (overwriting `ta-image.jpg` with each new image).
6.  If a face is found, the image is then uploaded and run through the Kairos emotion API. 
7.  Data from the detection and emotion API are inserted into the current document under `face` : {`detection`, `emotion`}
8.  When the final image is processed, `ta-image.jpg` is deleted. If an error occurs, the image is deleted.
9.  Occasionally, the Kairos API will return facial detection data, but not emotion data.
10. The older the collection, the more dead profile pic links.

  #### CSV Export:
1.  Column headings are manually defined within the `headers` list in `export.py`.
2.  The values are serached for within the current document. If they exist, the values are directly inserted into the `data` list. If they do not exist, a blank is inserted.
3.  Before being added to `data`, the emotion values are compared with one another for the highest value. Whatever the highest value refers to is inserted into the list. The same is done with the ethnicity values provided by the Kairos API. 
4.  The `rightEyeCenterX` is subtracted from `leftEyeCenterX` (or is it the other way around?) for the `eyegap`, which is then inserted into `data`.
5.  The `data` list is then written to the CSV file as a single row (the current document). This process is repeated for every document in the collection.

  #### Readability:
 1. Uses the module <a href="https://github.com/shivam5992/textstat">textstat</a> to simplify finding the various readability values.
 2. Finds and inserts 3 values: `readability`: {`flesch_ease`, `flesch_grade`, `standard`}.
 3. Overrides `textstat`'s `sentence_count` function to utilize NLTK's `TweetTokenizer` to remove @users and reduce word length with over 3 letters (such as "waaaaaay" to "waaay"). Additionally, a regex removes any urls, and any '#' symbols are removed. NLTK's `sent_tokenize` is used to split up sentences.
 4. The `standard` value is the 'best grade level' from the results of many readability tests, see the link above for details.
 5. These scores can be negative or too high if the tweet content is too short, therefore, they are not inserted into the db in these cases.
 6. On occasion, `textstat` may generate an error message (such as a division by zero message). Just ignore it. The rest of the collection is still processed.
 ---
  #### References:
  >Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.
  
