try:
    from config import conf
    from menu import Menu
    import os,string
    from csv import writer
except ImportError as e:
    print("Import Error in export.py:", e)


def get_percent_quoted(text):
    if '\"' not in text:
        return 0

    def find_quotes(text):
        quote_indexes = []
        while True:
            try:
                index = text.find("\"", quote_indexes[len(quote_indexes) - 1] + 1)
                if index < 0:
                    raise IndexError
                quote_indexes.append(index)
            except IndexError:
                index = text.find("\"")
                if index in quote_indexes:
                    break
                if index >= 0:
                    quote_indexes.append(index)
        return quote_indexes

    indexes = find_quotes(text)
    if len(indexes) % 2 != 0:
        del indexes[int(len(indexes) / 2)]

    def quote_count(quote_indexes):
        total = 0
        counter = 0
        for enum, index in enumerate(quote_indexes):
            if enum % 2 != 0:
                continue
            next = quote_indexes[enum + 1]
            total += (next - index) + 1  # Counting the second quotation mark too.
        return total

    total = quote_count(indexes)
    return (total / len(text)) * 100

def get_biggest(values):  # find largest emotion/ethnicity value
    biggest = 0
    name = ""
    for i in values:
        try:
            if float(values.get(i)) > biggest:
                biggest = values.get(i)
                name = i
        except:
            continue
    return name, biggest


def get_difference(values):  # subtract eye values
    name, val = get_biggest(values)
    for i in values:
        try:
            if float(values.get(i)) < val:
                val -= values.get(i)
        except:
            continue
    return val


def write_data(fpath, coll, mode):
    headers = [  # Column headers, in order!
        'Username', 'User Age', 'Age Group', 'Glasses', 'User Gender', 'Lips', 'Glances', 'Dwell',
        'Attention', 'Blinking', 'User Country', 'User City',
        'User Verified', 'User Followers', 'User Following',
        'Tweet Date', 'Tweet Content', 'Tweet Language', 'Tweet Favorites', 'Tweet Retweets',
        'Sentiment Pos', 'Sentiment Neu', 'Sentiment Neg', 'Sentiment Comp', 'Flesch Ease', 'Flesch Grade',
        'Readability Standard',
        'User Emotion', 'User Ethnicity', 'Eye Gap', 'Percent Quoted', "Tweet Length"
    ]
    data = []

    # Create/Open CSV file
    with open(fpath, mode, newline='', encoding='utf-8') as out_file:
        w = writer(out_file, dialect='excel')
        if mode is not 'a':
            w.writerow(headers)  # Write headers

        def set_value(doc, item, append=True):  # append to data/catch key errors
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
        for doc in all:  # go through all docs

            if 'text' not in doc:
                continue

            set_value(doc, [['user'], ['screen_name']])  # @username
            set_value(doc,
                      [['face'], ['detection'], ['images'], [0], ['faces'], [0], ['attributes'], ['age']])  # kairos age
            set_value(doc, [['face'], ['emotion'], ['frames'], [0], ['people'], [0], ['demographics'],
                            ['age_group']])  # age group
            set_value(doc, [['face'], ['detection'], ['images'], [0], ['faces'], [0], ['attributes'],
                            ['glasses']])  # glasses
            set_value(doc, [['face'], ['detection'], ['images'], [0], ['faces'], [0], ['attributes'], ['gender'],
                            ['type']])  # gender
            set_value(doc, [['face'], ['detection'], ['images'], [0], ['faces'], [0], ['attributes'], ['lips']])  # lips
            set_value(doc,
                      [['face'], ['emotion'], ['frames'], [0], ['people'], [0], ['tracking'], ['glances']])  # glances
            set_value(doc, [['face'], ['emotion'], ['frames'], [0], ['people'], [0], ['tracking'], ['dwell']])  # dwell
            set_value(doc, [['face'], ['emotion'], ['frames'], [0], ['people'], [0], ['tracking'],
                            ['attention']])  # attention
            set_value(doc,
                      [['face'], ['emotion'], ['frames'], [0], ['people'], [0], ['tracking'], ['blink']])  # blinking
            set_value(doc, [['place'], ['country']])  # country
            set_value(doc, [['place'], ['name']])  # city
            set_value(doc, [['user'], ['verified']])  # verfied
            set_value(doc, [['user'], ['followers_count']])  # followers
            set_value(doc, [['user'], ['friends_count']])  # following
            set_value(doc, [['created_at']])  # tweet date
            set_value(doc, [['text']])  # tweet content
            set_value(doc, [['lang']])  # tweet language
            set_value(doc, [['favorite_count']])  # will be 0 unless historical tweet
            set_value(doc, [['retweet_count']])  # ^
            set_value(doc, [['sentiment'], ['pos']])
            set_value(doc, [['sentiment'], ['neu']])
            set_value(doc, [['sentiment'], ['neg']])
            set_value(doc, [['sentiment'], ['compound']])
            set_value(doc, [['readability'], ['flesch_ease']])
            set_value(doc, [['readability'], ['flesch_grade']])
            set_value(doc, [['readability'], ['standard']])

            emotions = {
                "anger": set_value(doc,
                                   [['face'], ['emotion'], ['frames'], [0], ['people'], [0], ['emotions'], ['anger']],
                                   False),
                "disgust": set_value(doc, [['face'], ['emotion'], ['frames'], [0], ['people'], [0], ['emotions'],
                                           ['disgust']], False),
                "fear": set_value(doc,
                                  [['face'], ['emotion'], ['frames'], [0], ['people'], [0], ['emotions'], ['fear']],
                                  False),
                "joy": set_value(doc, [['face'], ['emotion'], ['frames'], [0], ['people'], [0], ['emotions'], ['joy']],
                                 False),
                "sadness": set_value(doc, [['face'], ['emotion'], ['frames'], [0], ['people'], [0], ['emotions'],
                                           ['sadness']], False),
                "surprise": set_value(doc, [['face'], ['emotion'], ['frames'], [0], ['people'], [0], ['emotions'],
                                            ['surprise']], False),
            }
            name, biggest = get_biggest(emotions)
            data.append(name)

            ethnicity = {
                "asian": set_value(doc, [['face'], ['detection'], ['images'], [0], ['faces'], [0], ['attributes'],
                                         ['asian']], False),
                "hispanic": set_value(doc, [['face'], ['detection'], ['images'], [0], ['faces'], [0], ['attributes'],
                                            ['hispanic']], False),
                "other": set_value(doc, [['face'], ['detection'], ['images'], [0], ['faces'], [0], ['attributes'],
                                         ['other']], False),
                "black": set_value(doc, [['face'], ['detection'], ['images'], [0], ['faces'], [0], ['attributes'],
                                         ['black']], False),
                "white": set_value(doc, [['face'], ['detection'], ['images'], [0], ['faces'], [0], ['attributes'],
                                         ['white']], False),
            }
            name, biggest = get_biggest(ethnicity)
            data.append(name)

            eyegap = {  # eye gap, because why not?
                "leftCenterX": set_value(doc,
                                         [['face'], ['detection'], ['images'], [0], ['faces'], [0], ['leftEyeCenterX']],
                                         False),
                "rightCenterX": set_value(doc, [['face'], ['detection'], ['images'], [0], ['faces'], [0],
                                                ['rightEyeCenterX']], False),
            }
            diff = get_difference(eyegap)
            if diff != 0:
                data.append(diff)
            else:
                data.append('')

            quoted = get_percent_quoted(doc['text'])
            data.append(quoted)
            data.append(len(doc['text']))

            w.writerow(data)
            data[:] = []

class MenuExport(Menu):
    # Menu for collection and file name
    def __init__(self):
        super().__init__()
        self.fpath = ''
        self.fname = ''
        self.mode = 'w'
        self.subdir = ''

    def set_path(self):
        self.fpath = conf['export_dir'] + self.subdir
        if not os.path.exists(self.fpath):
            os.makedirs(self.fpath)
        self.fpath += self.fname

    def single_export(self):
        coll = self.get_coll_menu()
        if coll == None:
            return
        self.divider()
        self.fname = input("*Enter a filename. A .csv extension will be added.\n"
                           "*Leave blank to cancel.\n>>>" + self.colors['end']).replace(" ", "")
        if self.fname == '':
            self.notify("Export Cancelled.")
            return
        if ".csv" not in self.fname:
            self.fname = self.fname + ".csv"
        self.divider()
        self.set_path()
        if os.path.exists(self.fpath):
            self.path_exists()
        self.create_sheet(coll)

    def strip_all(self,text):
        # Remove punctuation and spaces
        return text.translate(text.maketrans('', '', string.punctuation.replace("-",""))).replace(" ","-").replace("--", "-")

    def multi_export(self):
        # NOTE: CAPITALIZATION IS AFFECTED DIFFERENTLY ON WINDOWS VS LINUX
        try:
            coll,db = self.get_db_menu()
        except TypeError:
            return
        self.divider()
        self.subdir = input("*Enter an export subdirectory to create/use, such as 'dog-tweets'.\n"
                           "*Leave blank to place all in default export directory.\n>>>" + self.colors['end']).strip()
        if self.subdir:
            self.subdir = self.strip_all(self.subdir) + "/"
        print("Exporting Data...")
        for iter, item in enumerate(coll, 1):
            current_coll = db[coll[iter - 1]]
            coll_name = current_coll.__dict__['_Collection__name']
            coll_name = coll_name[:250].strip()
            coll_name = self.strip_all(coll_name) + ".csv"
            self.fname = coll_name
            self.set_path()
            fcounter = 0
            path = self.fpath
            while os.path.exists(path):
                path = self.fpath.replace(".csv","") + "(" + str(fcounter) + ")" + ".csv"
                fcounter+=1
            self.fpath = path
            self.create_sheet(current_coll)

    def create_sheet(self,coll):
        try:
            write_data(self.fpath, coll, self.mode)
            self.notify("Finished: " + os.path.abspath(self.fpath))
        except PermissionError:
            self.notify("Permission Error: Check if the specified file is open in another program\nand if you have "
                                "permission to create files here.")
            return

    def menu_export(self):
        menu = {
            1: self.single_export,
            2: self.multi_export
        }
        inpt = self.get_menu("EXPORT",["Export a Single Collection's Data.","Auto Export All DB Collections."],"*Enter an option number or [r] - return.\n>>>")
        if not inpt:
            return
        menu[inpt]()
        self.subdir = '' # Clear subdir name for multiple exports, preventing 'left overs'

    def path_exists(self):
        inpt = input(
            self.colors['purple'] + "A file with the name '" + self.fpath + "' already exists!\n" + self.colors['end'] +
            "Append to existing? [" + self.colors['purple'] + "a" + self.colors['end'] + "] - append, [" +
            self.colors['purple'] + "o" + self.colors['end'] +
            "] - overwrite, [" + self.colors['purple'] + "r" + self.colors['end'] + "] - cancel.\n>>>").replace(" ","")

        if inpt == 'a' or inpt == 'A':
            self.mode = 'a'
        elif inpt == 'o' or inpt == 'O':
            self.mode = 'w'
        else:
            self.notify("Export Cancelled.")
            return