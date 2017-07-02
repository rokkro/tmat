#TWITTER API KEYS
ckey = ''
csecret = ''
atoken = ''
asecret = ''
#KAIROS API KEYS
appid = ''
appkey = ''

verbose = False
startup_connect = True
tweet_similarity_threshold = .6
tweet_duplicate_limit = 15

'''
X***************************************************************************X
| verbose - Sets how much console output is printed.                        |
| Set to True to see duplicate catching, sentiment, etc.                    |
|                                                                           |
| startup_connect - Set to True to attempt MongoDB connection on startup.   |
|                                                                           |
| tweet_similarity_threshold - Sets how similar a tweet must be before it's |
| considered a duplicate. Values from 0 to 1, with 1 being exact duplicate. |
| Recommended at around .6                                                  |
|                                                                           |
| tweet_duplicate_limit - Number of tweets to check for duplicates.         |
| 0 = Check ALL in the collection (becomes VERY slow).                      |
| Tweets are auto sorted by similarity by MongoDB,                          |
| so it only needs to check the top few matches before it finds one.        |
X***************************************************************************X
'''