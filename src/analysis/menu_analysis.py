try:
    from menu import Menu
    from analysis import sentiment, image, readability
except ImportError as e:
    print("Import Error in menu_analysis.py:",e)
    quit()

class MenuText(Menu):
    """
    Menu function for the analysis submenu. 
    """
    def __init__(self):
        super().__init__()
        menu = {
            1: self.sub_init,
            2: self.sub_sentiment,
            3: self.sub_readability,
            4: self.sub_image
        }
        while True:
            inpt = self.get_menu("ANALYSIS",["Setup Text Analysis.", "Run Sentiment Analysis.", "Run Readability Analysis.", "Run Image Analysis."],
                "*Enter an option number or [r] - return.\n>>>")
            if inpt == 'r':
                return
            print(self.purple, end='')
            menu[inpt]()

    def sub_init(self):
        """
        Calls NLTK initialization/download function in sentiment.py
        """
        print(self.purple, end='')
        sentiment.initialize()
        print(self.end, end='')

    def sub_sentiment(self):
        """
        Gets selected collection, passes it to NLTK analysis function.
        """
        i = self.get_coll_menu()
        if i is None:
            return
        print(self.purple, end='')
        sentiment.analyze(i)
        print(self.end, end='')

    def sub_readability(self):
        """
        Gets selected collection, passes it to readability analysis function.
        """
        i = self.get_coll_menu()
        if i is None:
            return
        print(self.purple, end='')
        readability.analyze(i)
        print(self.end, end='')

    def sub_image(self):
        """
        Gets selected collection and an image limit
        passes it to readability analysis function.
        """
        coll = self.get_coll_menu()
        if coll is None:
            return
        self.divider()
        limit = self.get_menu("", None,"Enter the number of tweets to analyze.\nLeave blank for all in the collection.\n>>>")
        if limit == 'r':
            return
        self.divider()
        print(self.purple, end='')
        image.analyze(coll, limit)
        print(self.end, end='')


if __name__ == '__main__':
    MenuText()


