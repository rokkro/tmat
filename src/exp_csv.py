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
list_guide = [  # u=user general, t=tweet general, s=sentiment, em=emotions,eth=ethnicity, ep=eyepos, group tags!!
    ['u', 'user', 'screen_name'],  # username
    ['u', 'face', 'detection', 'images', 0, 'faces', 0, 'attributes', 'age'],  # age
    ['u', 'face', 'emotion', 'frames', 0, 'people', 0, 'demographics', 'age_group'],  # age group
    ['u', 'face', 'detection', 'images', 0, 'faces', 0, 'attributes', 'glasses'],  # glasses
    ['u', 'face', 'detection', 'images', 0, 'faces', 0, 'attributes', 'gender', 'type'],  # gender
    ['u', 'face', 'detection', 'images', 0, 'faces', 0, 'attributes', 'lips'],  # lips
    ['u', 'face', 'emotion', 'frames', 0, 'people', 0, 'tracking', 'glances'],  # glances
    ['u', 'face', 'emotion', 'frames', 0, 'people', 0, 'tracking', 'dwell'],  # dwell
    ['u', 'face', 'emotion', 'frames', 0, 'people', 0, 'tracking', 'attention'],  # attention
    ['u', 'face', 'emotion', 'frames', 0, 'people', 0, 'tracking', 'blink'],  # blinking
    ['u', 'place', 'country'], ['u', 'place', 'name'], ['u', 'user', 'verified'], ['u', 'user', 'followers_count'],
    ['u', 'user', 'friends_count'],  # following
    ['t', 'created_at'], ['t', 'text'], ['t', 'lang'], ['t', 'favorite_count'], ['t', 'retweet_count'],
    ['s', 'sentiment', 'pos'], ['s', 'sentiment', 'neu'], ['s', 'sentiment', 'neg'], ['s', 'sentiment', 'compound'],
    ['em', 'face', 'emotion', 'frames', 0, 'people', 0, 'emotions', 'anger'],  # anger
    ['em', 'face', 'emotion', 'frames', 0, 'people', 0, 'emotions', 'disgust'],  # disgust
    ['em', 'face', 'emotion', 'frames', 0, 'people', 0, 'emotions', 'fear'],  # fear
    ['em', 'face', 'emotion', 'frames', 0, 'people', 0, 'emotions', 'joy'],  # joy
    ['em', 'face', 'emotion', 'frames', 0, 'people', 0, 'emotions', 'sadness'],  # sadness
    ['em', 'face', 'emotion', 'frames', 0, 'people', 0, 'emotions', 'surprise'],  # surprise
    ['eth', 'face', 'detection', 'images', 0, 'faces', 0, 'attributes', 'asian'],  # asian
    ['eth', 'face', 'detection', 'images', 0, 'faces', 0, 'attributes', 'hispanic'],  # hispanic
    ['eth', 'face', 'detection', 'images', 0, 'faces', 0, 'attributes', 'other'],  # other
    ['eth', 'face', 'detection', 'images', 0, 'faces', 0, 'attributes', 'black'],  # black
    ['eth', 'face', 'detection', 'images', 0, 'faces', 0, 'attributes', 'white'],  # white
    ['ep', 'face', 'detection', 'images', 0, 'faces', 0, 'leftEyeCenterX'],  # leftEyeX
    ['ep', 'face', 'detection', 'images', 0, 'faces', 0, 'rightEyeCenterX'],  # rightEyeX

]
def write_data(fname):
    coll = get_coll()
    if coll == None:
        return

    data = []
    with open(fname,'w',newline='',encoding='utf-8') as out_file:
        w = writer(out_file, dialect='excel')
        w.writerow(headers)
        def error_slap(cursor,list): #handles non existant key errors, replacing them with the right stuff
            try:
                for i in range(1,len(list)): #loop through the list
                    cursor = cursor[list[i]] #keep accessing the next sub element in document, till reach the final key
                #print(cursor)
                data.append(cursor)
            except Exception as e:
                print("Error:",e)
                data.append("")


        all = coll.find({})
        ethbiggest = embiggest = epgap =  0
        for k,i in enumerate(all):
            for item in list_guide:
                error_slap(i,item)
            em = find_tag("em")
            for emotion in range(em[0],em[len(em)-1]):
                try:
                    if float(data[emotion]) > embiggest:
                       embiggest = data[emotion]
                except (ValueError,TypeError):
                    continue

            eth = find_tag("eth")
            for ethnicity in range(eth[0],eth[len(eth)-1]):
                try:
                    if float(data[ethnicity]) > ethbiggest:
                        ethbiggest = data[ethnicity]
                except (ValueError,TypeError):
                    continue

            ep = find_tag("ep")
            for eyes in range(ep[0],ep[len(ep)-1]):
                try:
                    epgap = data[ep[0]] - data[ep[len(ep)-1]]
                except (ValueError, TypeError):
                    continue

            del data[ep[0]:ep[len(ep) - 1]]
            data[ep[0]] = epgap
            del data[eth[0]:eth[len(eth)-1]]
            data[eth[0]] = ethbiggest
            del data[em[0]:em[len(em)-1]]
            data[em[0]] = embiggest


            w.writerow(data)
            for i in data:
                print(i)
            ethbiggest = 0
            embiggest = 0
            epgap = 0
            data[:] = []

def find_tag(tag): #basic tag range
    r = []
    for j,i in enumerate(list_guide):
        if i[0] == tag:
            r.append(j)
    if len(r) > 0:
        return r
    else:
        return [0,0]

def setup():
    fname = input(color.BOLD + "*Please enter a filename. A .csv extension will be added.\n"
                               "Leave blank to cancel.\n>>>" + color.END).replace(" ","")
    if fname == '':
        print(color.YELLOW + "Export Cancelled." + color.END)
        return
    if ".csv" not in fname:
        fname = fname + ".csv"
    write_data(fname)

