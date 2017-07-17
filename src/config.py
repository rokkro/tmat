# Twitter API keys. Use for tweet scraping.
ckey = ''
csecret = ''
atoken = ''
asecret = ''

# Kairos API keys. Use for facial recognition.
appid = ''
appkey = ''

verbose = False
export_folder = "../output/"
startup_connect = True
mongo_timeout = 30

tweet_similarity_threshold = .6
tweet_duplicate_limit = 10


"""
verbose = Amount of console output printed. (True/False)
startup_connect = Whether it attempts MongoDB connection on program startup. (True/False)
mongo_timeout = Timeout in ms for connection to mongod service. Keep low if running locally. (integer)
export_folder = Folder where exported .csv files are placed.

tweet_similarity_threshold = How similar a tweet must be before it's considered a duplicate. 
    From 0 to 1, with 1 being an exact duplicate. (float, 0 - 1)
tweet_duplicate_limit = Number of tweets to check for duplicates. (integer)
    0 = check ALL in collection (VERY slow). 1 = check 1 tweet (fast!).
    MongoDB sorts by sim using text indexes, so only the top few tweets should be checked before a duplicate is found.
"""