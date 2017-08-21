try:
    from config import export_dir
    from menu import Menu
    import os
    from csv import writer
except ImportError as e:
    print("Import Error in export.py:", e)


def get_percent_quoted(text):
    if '\"' not in text:
        return ''

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
    return (total / len(text))

def write_data(fpath, coll, mode):
    headers = [  # Column headers, in order!
        'Username', 'User Age', 'Age Group', 'Glasses', 'User Gender', 'Lips', 'Glances', 'Dwell',
        'Attention', 'Blinking', 'User Country', 'User City',
        'User Verified', 'User Followers', 'User Following',
        'Tweet Date', 'Tweet Content', 'Tweet Language', 'Tweet Favorites', 'Tweet Retweets',
        'Sentiment Pos', 'Sentiment Neu', 'Sentiment Neg', 'Sentiment Comp', 'Flesch Ease', 'Flesch Grade',
        'Readability Standard',
        'User Emotion', 'User Ethnicity', 'Eye Gap', 'Percent Quoted'
    ]
    data = []

    # Create/Open CSV file
    with open(fpath, mode, newline='', encoding='utf-8') as out_file:
        w = writer(out_file, dialect='excel')
        if mode is not 'a':
            w.writerow(headers)  # Write headers

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

            w.writerow(data)
            data[:] = []

class MenuExport(Menu):
    # Menu for collection and file name
    def __init__(self):
        super().__init__()
        self.fpath = ''
        self.fname = ''
        self.mode = 'w'
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)

    def menu_export(self):
        coll = self.get_coll_menu()
        if coll == None:
            return
        self.divider()
        self.fname = input("*Enter a filename. A .csv extension will be added.\n"
                      "Leave blank to cancel.\n>>>" + self.colors['end']).replace(" ", "")
        if self.fname == '':
            Menu.notification_queue.append(self.colors['purple'] + "Export Cancelled." + self.colors['end'])
            return
        if ".csv" not in self.fname:
            self.fname = self.fname + ".csv"
        self.divider()
        try:
            print(self.colors['purple'], end='')
            self.fpath = export_dir + self.fname
            if os.path.exists(self.fpath):
                self.path_exists()
            write_data(self.fpath, coll, self.mode)
            Menu.notification_queue.append("Finished: " + os.path.abspath(self.fpath))
        except PermissionError:
            Menu.notification_queue.append(self.colors['purple'] + "Permission Error: Check if the specified file is open in another program\nand if you have "
                                "permission to create files here." + self.colors['end'])
            return

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
            Menu.notification_queue.append(self.colors['purple'] + "Export Cancelled." + self.colors['end'])
            return