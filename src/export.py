try:
    from csv import writer
except ImportError as e:
    print("Import Error in export.py:", e)


def write_data(fname, coll):
    headers = [  # Column headers, in order!
        'Username', 'User Age', 'Age Group', 'Glasses', 'User Gender', 'Lips', 'Glances', 'Dwell',
        'Attention', 'Blinking', 'User Country', 'User City',
        'User Verified', 'User Followers', 'User Following',
        'Tweet Date', 'Tweet Content', 'Tweet Language', 'Tweet Favorites', 'Tweet Retweets',
        'Sentiment Pos', 'Sentiment Neu', 'Sentiment Neg', 'Sentiment Comp', 'Flesch Ease', 'Flesch Grade',
        'Readability Standard',
        'User Emotion', 'User Ethnicity', 'Eye Gap',
    ]
    data = []
    # Create/Open CSV file
    with open(fname, 'w', newline='', encoding='utf-8') as out_file:
        w = writer(out_file, dialect='excel')
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

            w.writerow(data)
            data[:] = []
        print(fname + " created in the current directory!")


def menu_export():
    # Mini menu for collection and file name
    try:
        from menu import Menu
    except ImportError as e:
        print("Error in export.py:", e)
        return
    menu = Menu()
    coll = menu.get_coll_menu()
    if coll == None:
        return
    menu.divider()
    fname = input("*Enter a filename. A .csv extension will be added.\n"
                  "Leave blank to cancel.\n>>>" + menu.end).replace(" ", "")
    if fname == '':
        print(menu.purple + "Export Cancelled." + menu.end)
        return
    if ".csv" not in fname:
        fname = fname + ".csv"
    menu.divider()
    try:
        print(menu.purple, end='')
        write_data(fname, coll)
        print(menu.end, end='')
    except PermissionError:
        print(menu.purple + "Permission Error: Check if the specified file is open in another program\nand if you have "
                            "permission to create files here." + menu.end)
        return
