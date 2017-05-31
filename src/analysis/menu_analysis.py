from menu import get_menu, get_coll, divider
from analysis import sentiment, image, text


def menu_text():
    while True:
        inpt = get_menu("TEXT ANALYSIS",["Run Initial Setup.", "Run Sentiment Analysis.", "Run Text Analysis."],
                        "*Enter an option number or [r] - return.\n>>>", 3)
        if inpt == 'r':
            return

        def sub_analysis():
            i = get_coll()
            if i is None:
                return
            sentiment.analyze(i)

        def sub_text():
            i = get_coll()
            if i is None:
                return
            text.analyze(i)

        menu = {
            1: sentiment.initialize,
            2: sub_analysis,
            3: sub_text
        }
        menu[inpt]()


def menu_image():
    coll = get_coll()
    if coll is None:
        return
    divider()
    limit = get_menu("",None, "Enter the number of tweets to analyze.\nLeave blank for all in the collection.\n>>>")
    if limit == 'r':
        return
    divider()
    image.insert_data(coll, limit)
