from display import get_coll, color
from csv import writer

#permissionError when file is open elsewhere
headers = [
    'Username','User Age', 'Age Group', 'Glasses', 'User Gender','Lips', 'Glances', 'Dwell',
    'Attention', 'Blinking', 'User Country', 'User City',
    'User Verified', 'User Followers', 'User Following',
    'Tweet Date', 'Tweet Content', 'Tweet Language', 'Tweet Favorites', 'Tweet Retweets',
    'Sentiment Pos', 'Sentiment Neu', 'Sentiment Neg', 'Sentiment Comp',
    'User Emotion', 'User Ethnicity',  'Eye Gap',
]
def write_data(fname):
    coll = get_coll()
    if coll == None:
        return
    data = []
    with open(fname,'w',newline='',encoding='utf-8') as out_file:
        w = writer(out_file, dialect='excel')
        w.writerow(headers)

        def get_biggest(values):
            biggest = 0
            name = ""
            for i in values:
                try:
                    if float(values.get(i)) > biggest:
                        biggest = values.get(i)
                        name = i
                except:
                    continue
            return name,biggest

        def get_difference(values):
            name, val = get_biggest(values)
            for i in values:
                try:
                    if float(values.get(i)) < val:
                        val-=values.get(i)
                except:
                    continue
            return val

        def set_value(doc,item,append=True):
            try:
                for i in item:
                    doc = doc[i[0]]
                if append:
                    data.append(doc)
                else:
                    return doc
            except:
                if append:
                    data.append("")
                else:
                    return None


        all = coll.find({})
        for iterator,doc in enumerate(all): #far less convoluted than i originally had it set up
            set_value(doc,[['user'],['screen_name']])
            set_value(doc,[['face'],['detection'],['images'],[0],['faces'],[0],['attributes'],['age']])
            set_value(doc,[['face'],['emotion'],['frames'],[0],['people'], [0], ['demographics'], ['age_group']])  # age group
            set_value(doc,[['face'],['detection'],['images'], [0], ['faces'], [0], ['attributes'], ['glasses']])  # glasses
            set_value(doc,[['face'], ['detection'], ['images'], [0], ['faces'], [0], ['attributes'], ['gender'],['type']])  # gender
            set_value(doc,[['face'], ['detection'], ['images'], [0], ['faces'], [0], ['attributes'], ['lips']])  # lips
            set_value(doc,[['face'], ['emotion'], ['frames'], [0], ['people'], [0], ['tracking'], ['glances']])  # glances
            set_value(doc,[['face'],['emotion'],['frames'], [0], ['people'], [0], ['tracking'], ['dwell']])  # dwell
            set_value(doc,[['face'], ['emotion'], ['frames'], [0], ['people'], [0], ['tracking'], ['attention']]) #attention
            set_value(doc,[['face'], ['emotion'], ['frames'], [0], ['people'], [0], ['tracking'], ['blink']]) #blinking
            set_value(doc,[['place'], ['country']])
            set_value(doc,[['place'], ['name']])
            set_value(doc,[['user'], ['verified']])
            set_value(doc,[['user'], ['followers_count']]) #followers
            set_value(doc,[['user'], ['friends_count']]) #following
            set_value(doc,[['created_at']]) #tweet date
            set_value(doc, [['text']])
            set_value(doc, [['lang']])
            set_value(doc,[['favorite_count']]) #will be 0 unless historical tweet
            set_value(doc,[['retweet_count']])
            set_value(doc,[['sentiment'],['pos']])
            set_value(doc, [['sentiment'],['neu']])
            set_value(doc,[['sentiment'],['neg']])
            set_value(doc,[['sentiment'],['compound']])
            emotions = {
                "anger": set_value(doc,[['face'], ['emotion'], ['frames'], [0], ['people'], [0], ['emotions'], ['anger']],False),
                "disgust": set_value(doc,[['face'], ['emotion'], ['frames'], [0], ['people'], [0], ['emotions'], ['disgust']],False),
                "fear" : set_value(doc,[['face'], ['emotion'], ['frames'], [0], ['people'], [0], ['emotions'], ['fear']],False),
                "joy" : set_value(doc,[['face'], ['emotion'], ['frames'], [0], ['people'], [0], ['emotions'], ['joy']],False),
                "sadness" : set_value(doc,[['face'], ['emotion'], ['frames'], [0], ['people'], [0], ['emotions'], ['sadness']],False),
                "surprise" :set_value(doc,[['face'], ['emotion'], ['frames'], [0], ['people'], [0], ['emotions'], ['surprise']],False),
            }
            name, biggest = get_biggest(emotions)
            data.append(name)

            ethnicity = {
                "asian":set_value(doc,[['face'], ['detection'], ['images'], [0], ['faces'], [0], ['attributes'], ['asian']],False),
                "hispanic":set_value(doc,[['face'], ['detection'], ['images'], [0], ['faces'],[0],['attributes'],['hispanic']],False),
                "other":set_value(doc,[['face'], ['detection'], ['images'], [0], ['faces'], [0], ['attributes'], ['other']],False),
                "black":set_value(doc,[['face'], ['detection'], ['images'], [0], ['faces'], [0], ['attributes'], ['black']],False),
                "white":set_value(doc,[['face'], ['detection'], ['images'], [0], ['faces'], [0], ['attributes'], ['white']],False),
            }
            name, biggest = get_biggest(ethnicity)
            data.append(name)
            eyegap = {
                "leftCenterX":set_value(doc,[['face'], ['detection'], ['images'], [0], ['faces'], [0], ['leftEyeCenterX']],False),
                "rightCenterX":set_value(doc,[['face'], ['detection'], ['images'], [0], ['faces'], [0], ['rightEyeCenterX']],False),
            }
            diff = get_difference(eyegap)
            data.append(diff)
            w.writerow(data)
            data[:] = []

def setup():
    fname = input(color.BOLD + "*Please enter a filename. A .csv extension will be added.\n"
                               "Leave blank to cancel.\n>>>" + color.END).replace(" ","")
    if fname == '':
        print(color.YELLOW + "Export Cancelled." + color.END)
        return
    if ".csv" not in fname:
        fname = fname + ".csv"
    try:
        write_data(fname)
    except PermissionError:
        print(color.YELLOW + "Permission Error: Check if it's open in another program\nor if you have "
                             "permission to create files here." + color.END)
        return
