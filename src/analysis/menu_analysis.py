from display_menu import get_menu, get_coll, dashes
from analysis import sentiment, image


def menu_sentiment():
    while True:
        inpt = get_menu("SENTIMENT",["Run initial setup.", "Choose a collection to analyze."],
                        "*Enter an option number or [r] - return.\n>>>", 2)
        if inpt == 'r':
            return

        def sub_analysis():
            i = get_coll()
            if i is None:
                return
            sentiment.analyze(i)

        menu = {
            1: sentiment.initialize,
            2: sub_analysis,
        }
        menu[inpt]()


def menu_image():
    coll = get_coll()
    if coll is None:
        return
    dashes()
    limit = get_menu("",None, "Enter the number of tweets to analyze.\nLeave blank for all in the collection.\n>>>")
    if limit == 'r':
        return
    dashes()
    image.insert_data(coll, limit)
