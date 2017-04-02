from json import JSONDecodeError
from display import get_input,select_coll
from analysis import sentiment,image

def menu_sentiment():
    inpt = get_input("[1] - Run initial setup.\n[2] - Choose a collection to analyze.",
                     "*Enter an option number or [r] - return.\n>>>",2)
    if inpt=='r':
        return

    def sub_analysis():
        i = select_coll()
        if i==None:
            return
        sentiment.analyze(i)

    menu = {
        1: sentiment.initialize,
        2:sub_analysis,
    }

    menu[inpt]()

def menu_image():
    coll = select_coll()
    if coll == None:
        return
    try:
        image.insert_data(coll)
    except JSONDecodeError as e:
        print("Possible Kairos Error. Verify your API keys are correct.",e)
