from display import select_coll, get_input

def menu_filter_sentiment():
    print("test")
def menu_filter_image():

def menu_filter_tweets():


def menu_export():
    coll = select_coll()
    if coll == None:
        return
    while True:
        inpt = get_input("[1] - Set Tweet Filters.\n[2] - Set Sentiment Value Filters."
                         "\n[3] - Set Image Analysis Filters.","*Set filters or: [Enter] - export to csv, [r] -return",3)

        menu = {
            1: menu_filter_tweets,
            2: menu_filter_sentiment,
            3: menu_filter_image,
        }
        menu[inpt]()
