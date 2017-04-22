from display import get_coll, color
from csv import writer

#permissionError when file is open elsewhere
def write_data(fname):
    coll = get_coll()
    if coll == None:
        return
    headers = [
        'Username', 'Tweet Date', 'Tweet Content','Favorites','Retweets',
        'Sentiment Pos','Sentiment Neu','Sentiment Neg','Sentiment Comp',
        'Emotion','Race','Age','Gender','Tweet Language','Country','City',
        'Verified', 'Followers', 'Following'
    ]

    with open(fname,'w',newline='') as out_file:
        w = writer(out_file, dialect='excel')
        w.writerow(headers)
        #begin grand loop
        all = coll.find({})
        for i in all:
            username = i.find()



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

