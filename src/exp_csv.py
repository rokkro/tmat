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
        def error_slap(cursor,list): #handles non existant key errors, replacing them with the right stuff
            try:
                for i in range(len(list)):
                    cursor = cursor[list[i]]
                print(cursor)
            except Exception as e:
                print("Error:",e)
       # row = [i['user']['screen_name'], i['created_at'], i['text'], i['lang'],
       #  i['face']['detection']['images'][0]['faces'][0]['attributes']['gender']['type']]
        row = [
            ['user','screen_name'],['created_at'],['text'],['lang'],['favorite_count'],['retweet_count'],
            ['sentiment', 'pos'],['sentiment','neu'],['sentiment', 'neg'],['sentiment', 'compound'],
            ['face', 'detection', 'images', 0, 'faces', 0, 'attributes', 'gender', 'type']
        ]
        all = coll.find({})
        for k,i in enumerate(all):
            for item in row:
                error_slap(i,item)


            #uemotion =
            #urace =
            #uage =
            error_slap(i,['user','time_zone'])



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

