from display import get_coll, color
from csv import writer

#permissionError when file is open elsewhere
def write_data(fname):
    coll = get_coll()
    if coll == None:
        return
    headers = [
        'Username', 'Tweet Date', 'Tweet Content','Tweet Language', 'Tweet Favorites','Tweet Retweets',
        'Sentiment Pos','Sentiment Neu','Sentiment Neg','Sentiment Comp',
        'User Emotion','User Ethnicity','User Age','Age Group','Glasses','User Gender','Eye Gap', 'Lips','Dwell','Attention','Blinking','User Country','User City',
        'User Verified', 'User Followers', 'User Following'
    ]
    list_guide = [
        ['user', 'screen_name'], ['created_at'], ['text'], ['lang'], ['favorite_count'], ['retweet_count'],
        ['sentiment', 'pos'], ['sentiment', 'neu'], ['sentiment', 'neg'], ['sentiment', 'compound'],
        ['face','emotion','frames',0,'people',0,'emotions','anger'], #anger
        ['face', 'emotion', 'frames', 0, 'people', 0, 'emotions', 'disgust'],#disgust
        ['face', 'emotion', 'frames', 0, 'people', 0, 'emotions', 'fear'],#fear
        ['face', 'emotion', 'frames', 0, 'people', 0, 'emotions', 'joy'],#joy
        ['face', 'emotion', 'frames', 0, 'people', 0, 'emotions', 'sadness'],#sadness
        ['face', 'emotion', 'frames', 0, 'people', 0, 'emotions', 'surprise'],#surprise
        ['face','detection','images',0,'faces',0,'attributes','asian'],#asian
        ['face', 'detection', 'images', 0, 'faces', 0, 'attributes', 'hispanic'], #hispanic
        ['face', 'detection', 'images', 0, 'faces', 0, 'attributes', 'other'], #other
        ['face', 'detection', 'images', 0, 'faces', 0, 'attributes', 'black'], #black
        ['face', 'detection', 'images', 0, 'faces', 0, 'attributes', 'white'], #white
        ['face', 'detection', 'images', 0, 'faces', 0, 'attributes', 'age'],  # age
        ['face', 'emotion', 'frames', 0, 'people', 0, 'demographics', 'age_group'], #age group
        ['face', 'detection', 'images', 0, 'faces', 0, 'attributes', 'glasses'], #glasses
        ['face', 'detection', 'images', 0, 'faces', 0, 'attributes', 'gender', 'type'],  # gender
        ['face', 'detection', 'images', 0, 'faces', 0, 'leftEyeCenterX'],  # leftEyeX
        ['face', 'detection', 'images', 0, 'faces', 0, 'rightEyeCenterX'],  # rightEyeX
        ['face', 'detection', 'images', 0, 'faces', 0, 'attributes', 'lips'],  # lips
        ['face', 'emotion', 'frames', 0, 'people', 0, 'tracking', 'glances'],  # glances
        ['face', 'emotion', 'frames', 0, 'people', 0, 'tracking', 'dwell'],  # dwell
        ['face', 'emotion', 'frames', 0, 'people', 0, 'tracking', 'attention'],  # attention
        ['face', 'emotion', 'frames', 0, 'people', 0, 'tracking', 'blink'],  # blinking
        ['place','country'], ['place','name'], ['user','verified'],['user','followers_count'],['user','friends_count']
    ]
    data = []
    with open(fname,'w',newline='',encoding='utf-8') as out_file:
        w = writer(out_file, dialect='excel')
        w.writerow(headers)
        def error_slap(cursor,list): #handles non existant key errors, replacing them with the right stuff
            try:
                for i in range(len(list)): #loop through the list
                    cursor = cursor[list[i]] #keep accessing the next sub element in document, till reach the final key
                #print(cursor)
                data.append(cursor)
            except Exception as e:
                print("Error:",e)
                data.append("")


        all = coll.find({})
        ethbiggest = embiggest = 0
        for k,i in enumerate(all):
            for item in list_guide:
                error_slap(i,item)
            for emotion in range(10,16):
                try:
                    if float(data[emotion]) > embiggest:
                       embiggest = data[emotion]
                except (ValueError,TypeError):
                    continue
            for ethnicity in range(16,21):
                try:
                    if float(data[ethnicity]) > ethbiggest:
                        ethbiggest = data[ethnicity]
                except (ValueError,TypeError):
                    continue
            del data[17:21]
            data[16] = ethbiggest
            del data[11:16]
            data[10] = embiggest
            w.writerow(data)
            for i in data:
                print(i)
            ethbiggest = 0
            embiggest = 0
            data[:] = []


def setup():
    fname = input(color.BOLD + "*Please enter a filename. A .csv extension will be added.\n"
                               "Leave blank to cancel.\n>>>" + color.END).replace(" ","")
    if fname == '':
        print(color.YELLOW + "Export Cancelled." + color.END)
        return
    if ".csv" not in fname:
        fname = fname + ".csv"
    write_data(fname)

