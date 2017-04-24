from json import JSONDecodeError
from display import get_menu,get_coll
from analysis import sentiment,image

def menu_sentiment():
    inpt = get_menu("[1] - Run initial setup.\n[2] - Choose a collection to analyze.",
                     "*Enter an option number or [r] - return.\n>>>", 2)
    if inpt=='r':
        return

    def sub_analysis():
        i = get_coll()
        if i==None:
            return
        sentiment.analyze(i)

    menu = {
        1: sentiment.initialize,
        2:sub_analysis,
    }

    menu[inpt]()

def menu_image():
    coll = get_coll()
    if coll == None:
        return
    try:
        limit = get_menu(None,"Enter the number of tweets to analyze.\nLeave blank for all in the collection.\n>>>")
        image.insert_data(coll,limit)
    except JSONDecodeError as e:
        print("Possible Kairos Error. Verify your API keys are correct.",e)
    except BaseException as e:
        print("Error:",e)
