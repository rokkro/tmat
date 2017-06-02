try:
    import config
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
            try:
                if "text" not in doc:  # if the current doc doesnt have 'text' field, move on
                    continue
                tokenized = tweet_tokenize(doc['text'])
                if len(tokenized) <=1:
                    continue
                flesch_ease = t_stat.flesch_reading_ease(tokenized)
                if flesch_ease > 100:
                    continue
                flesch_grade = t_stat.flesch_kincaid_grade(tokenized)
                text_standard = t_stat.text_standard(tokenized)
                if config.verbose:
                    print(doc['text'],"SUMMARIZED",text_standard)
                    print("FLESCH EASE",flesch_ease)
                    print("FLESCH GRADE",flesch_grade)
                coll.update_one({'_id': doc.get('_id')}, {'$set': {
                    "readability": {
                        "flesch_ease": t_stat.flesch_reading_ease(tokenized),
                        "flesch_grade": t_stat.flesch_kincaid_grade(tokenized),
                        "standard": t_stat.text_standard(tokenized)
                    }
                }})
            except Exception as e:
                #print("ERROR:",tokenized,doc['text'])
                continue
        cursor.close()
        print("Readability values have been attached to each tweet document in the collection.")
    except (NameError, LookupError) as e:
        print("Error: Make sure you have 'textstat' installed", e)
        return