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
        'User Emotion','User Race','User Age','User Gender','User Country','User City',
        'User Verified', 'User Followers', 'User Following'
    ]
    with open(fname,'w',newline='') as out_file:
        w = writer(out_file, dialect='excel')
        w.writerow(headers)
        #begin grand loop
        def error_slap(cursor,lisst): #woooo!
            try:
                for i in range(len(lisst)):
                    cursor = cursor[lisst[i]]
                print(cursor)
            except Exception as e:
                print(e)
       # row = [i['user']['screen_name'], i['created_at'], i['text'], i['lang'],
       #  i['face']['detection']['images'][0]['faces'][0]['attributes']['gender']['type']]

        all = coll.find({})
        for k,i in enumerate(all):
            error_slap(i,['favorite_count'])
            error_slap(i,['sentiment','pos'])
            #uname =
            #tdate =
            #tweet = i['text']
            #tlang = i['lang']
            tfaves = i['favorite_count']
            tretweets = i['retweet_count']
            tspos = i['sentiment']['pos']
            tsneu = i['sentiment']['neu']
            tsneg = i['sentiment']['neg']
            tscomp = i['sentiment']['compound']
            #uemotion =
            #urace =
            #uage =
            print(k,i)
            ugender = i['face']['detection']['images'][0]['faces'][0]['attributes']['gender']['type']
            print(ugender)
            utimezone = i['user']['time_zone']
            print("MAED IT TO TIMEZONE")



        w.writerow(['test'])


def setup():
    fname = input(color.BOLD + "*Please enter a filename. A .csv extension will be added.\n"
                               "Leave blank to cancel.\n>>>" + color.END).replace(" ","")
    if fname == '':
        print(color.YELLOW + "Export Cancelled." + color.END)
        return
    if ".csv" not in fname:
        fname = fname + ".csv"
    write_data(fname)

