#http://www.nltk.org/howto/sentiment.html
import warnings
warnings.filterwarnings("ignore")
import mongo
try:
    from nltk.sentiment.util import *
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    from nltk.classify import NaiveBayesClassifier
    from nltk.corpus import subjectivity
    from nltk.sentiment import SentimentAnalyzer
    from nltk import tokenize
except ModuleNotFoundError as e:
    print("Module missing, install with pip:",e)

def initialize():

    n_instances = 100
    try:
        subj_docs = [(sent, 'subj') for sent in subjectivity.sents(categories='subj')[:n_instances]]
        obj_docs = [(sent, 'obj') for sent in subjectivity.sents(categories='obj')[:n_instances]]
    except NameError as e:
        print("Make sure NLTK is installed:",e)
        return
    nltk.download('subjectivity')
    nltk.download('vader_lexicon')
    nltk.download('punkt')
    len(subj_docs), len(obj_docs)

    train_subj_docs = subj_docs[:80]
    test_subj_docs = subj_docs[80:100]
    train_obj_docs = obj_docs[:80]
    test_obj_docs = obj_docs[80:100]
    training_docs = train_subj_docs +train_obj_docs
    testing_docs = test_subj_docs+test_obj_docs
    sentim_analyzer = SentimentAnalyzer()
    all_words_neg = sentim_analyzer.all_words([mark_negation(doc) for doc in training_docs])

    unigram_feats = sentim_analyzer.unigram_word_feats(all_words_neg, min_freq=4)
    sentim_analyzer.add_feat_extractor(extract_unigram_feats, unigrams=unigram_feats)

    training_set = sentim_analyzer.apply_features(training_docs)
    test_set = sentim_analyzer.apply_features(testing_docs)

    trainer = NaiveBayesClassifier.train
    classifier = sentim_analyzer.train(trainer, training_set)

    for key,value in sorted(sentim_analyzer.evaluate(test_set).items()):
         print('{0}: {1}'.format(key, value))

def analyze(coll):
    if not mongo.connected:
        print("MongoDB must be connected to perform sentiment analysis!")
        return
    sentences = []
    try:
        sid = SentimentIntensityAnalyzer()
    except NameError as e:
        print("Make sure NLTK is installed and you have run initial setup:",e)
        return
    cursor = coll.find({}) #finds all documents in collection
    for i in cursor: #loop through those
        if "text" not in i: #if the current doc doesnt have 'text' field, move on
            continue
        try:
            sentences.extend(tokenize.sent_tokenize(i["text"])) #prepare tweet text
            ss = sid.polarity_scores(sentences[0]) #get polarity of text
        except LookupError as e:
            print("Make sure you have run initial setup:",e)
        #print(i.get('_id'))
        #print(sentences[0])
        #print(ss)
        coll.update_one({'_id':i.get('_id')},{ '$set' : {
            "sentiment":{
                "pos": ss['pos'],
                "neg": ss['neg'],
                "neu": ss['neu'],
                "compound": ss['compound']
            }
        }})
        sentences[:] = [] #empty list
    print("Sentiment values have been attached to each tweet document in the collection.")
