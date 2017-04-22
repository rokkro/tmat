from display import get_coll, get_menu, color
from csv import DictWriter, DictReader

def setup():
    headers = [
        'Username', 'Tweet Date', 'Tweet Content','Favorites','Retweets',
        'Sentiment Pos','Sentiment Neu','Sentiment Neg','Sentiment Comp',
        'Emotion','Race','Age','Gender','Language','Country','City'
    ]
    coll = get_coll()
    if coll == None:
        return
    fname = input(color.BOLD + "*Please enter a filename. A .csv extension will be added.\n"
                               "Leave blank to cancel.\n>>>" + color.END).replace(" ","")
    if fname == '':
        print(color.YELLOW + "Export Cancelled." + color.END)
        return
    if ".csv" not in fname:
        fname = fname + ".csv"
    try:
        out_file=open(fname,'w')
        writer = DictWriter(f=out_file,fieldnames=headers)
        writer.writeheader()
    except BaseException as e:
        print("Error:",e)