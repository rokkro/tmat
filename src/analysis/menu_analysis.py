try:
    from menu import get_menu, get_coll, divider,Color
    from analysis import sentiment, image, readability
except ImportError as e:
    print("Error:",e)

def menu_text():
    while True:
        inpt = get_menu("ANALYSIS",["Setup Text Analysis.", "Run Sentiment Analysis.", "Run Readability Analysis.", "Run Image Analysis."],
                        "*Enter an option number or [r] - return.\n>>>")
        if inpt == 'r':
            return
        def sub_init():
            print(Color.YELLOW,end='')
            sentiment.initialize()
            print(Color.END,end='')

        def sub_analysis():
            i = get_coll()
            if i is None:
                return
            print(Color.YELLOW,end='')
            sentiment.analyze(i)
            print(Color.END,end='')

        def sub_readability():
            i = get_coll()
            if i is None:
                return
            print(Color.YELLOW,end='')
            readability.analyze(i)
            print(Color.END, end='')

        def sub_image():
            coll = get_coll()
            if coll is None:
                return
            divider()
            limit = get_menu("", None,"Enter the number of tweets to analyze.\nLeave blank for all in the collection.\n>>>")
            if limit == 'r':
                return
            divider()
            print(Color.YELLOW,end='')
            image.analyze(coll, limit)
            print(Color.END,end='')

        menu = {
            1: sub_init,
            2: sub_analysis,
            3: sub_readability,
            4: sub_image
        }
        menu[inpt]()



