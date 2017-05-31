try:
    import config
    from menu import Color
    from textstat import textstat
    from nltk.tokenize import TweetTokenizer, sent_tokenize
    import re
except ImportError as e:
    print("Error:",e)

def tweet_tokenize(text):
    '''
    Strip out Tweet URLs, handles, shorten elongated words.
    '''
    try:
        tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)
    except (NameError, LookupError) as e:
        print("Error: Make sure NLTK is installed and you have run text analysis setup:", e)
        return
    no_url = re.sub(r"http\S+", "", text).replace("#", "").strip()
    return ' '.join(tknzr.tokenize(no_url)) #str

class ts(textstat.textstatistics):
    '''
    Overriding the sentence_count function to work better on tweets,
    Treat the period recognition better.
    '''
    def sentence_count(self, text):
        ignoreCount=0
        sentences = sent_tokenize(text)
        for sentence in sentences:
            if self.lexicon_count(sentence) <= 2:
                ignoreCount = ignoreCount + 1
        return max(1, len(sentences) - ignoreCount)

def analyze(coll):
    try:
        t_stat = ts()
        cursor = coll.find({})
        for doc in cursor:
            if "text" not in doc:  # if the current doc doesnt have 'text' field, move on
                continue
            tokenized = tweet_tokenize(doc['text'])
            if not len(tokenized):
                continue
            if config.verbose:
                print(doc['text'],"SUMMARIZED",t_stat.text_standard(tokenized))
                print("FLESCH EASE",t_stat.flesch_reading_ease(tokenized))
                print("FLESCH GRADE",t_stat.flesch_kincaid_grade(tokenized))
            coll.update_one({'_id': doc.get('_id')}, {'$set': {
                "readability": {
                    "flesch_ease": t_stat.flesch_reading_ease(tokenized),
                    "flesch_grade": t_stat.flesch_kincaid_grade(tokenized),
                    "summary": t_stat.text_standard(tokenized)
                }
            }})
        cursor.close()
        print(Color.YELLOW + "Readability values have been attached to each tweet document in the collection." + Color.END)
    except (NameError, LookupError) as e:
        print("Error: Make sure you have 'textstat' installed", e)
        return
    except Exception as e:
        print(e)



