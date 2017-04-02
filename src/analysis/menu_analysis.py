from display import get_input,get_list
from analysis import sentiment

def menu_sentiment():
    inpt = get_input("[1] - Run initial setup.\n[2] - Choose a collection to analyze.",
                     "Enter an option number or [r] - return.\n>>>",2)
    if inpt=='r':
        return

    def sub_analysis():
        i = get_list()
        if i==None:
            return
        sentiment.analyze(i)

    menu = {
        1: sentiment.initialize,
        2:sub_analysis,
    }

    menu[inpt]()
def menu_image():
    print("placeholder")
