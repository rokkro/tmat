try:
    from menu import Menu
    from . import sentiment, image, readability
except ImportError as e:
    print("Import Error in menu_analysis.py:",e)
    quit()

class MenuText(Menu):
    """
    Menu function for the analysis submenu. 
    """
    def __init__(self):
        super().__init__()

    def menu_analysis(self):
        menu = {
            1: self.sub_init,
            2: self.sub_sentiment,
            3: self.sub_readability,
            4: self.sub_image
        }
        while True:
            inpt = self.get_menu("ANALYSIS",
                                 ["Setup Text Analysis.", "Run Sentiment Analysis.", "Run Readability Analysis.",
                                  "Run Image Analysis."],
                                 "*Enter an option number or [r] - return.\n>>>")
            if inpt == 'r':
                return
            print(self.colors['purple'], end='')
            menu[inpt]()

    def sub_init(self):
        """
        Calls NLTK initialization/download function in sentiment.py
        """
        print(self.colors['purple'], end='')
        sentiment.initialize()
        print(self.colors['end'], end='')

    def sub_sentiment(self):
        """
        Gets selected collection, passes it to NLTK analysis function.
        """

        def sub_db():
            # Get database/collection by spawning a db menu. Raises TypeError if user cancels menu.
            try:
                coll,db = self.get_db_menu()
                return coll, db
            except TypeError:
                return None, None

        def sub_coll():
            # Handles returning second non-existant variable
            coll = self.get_coll_menu()
            return coll,None

        menu = {
            1: sub_db,
            2: sub_coll,
        }
        inpt = self.get_menu("SENTIMENT",["Run SA on an Entire Database.", "Run SA on a Single Collection."], "*Enter an option number or [r] - return.\n>>>")
        coll,db = menu[inpt]()
        if coll is None:
            return
        sentiment.coll_set(coll,db)
        self.notify("Sentiment values have been attached to each tweet document in the collection.")

    def sub_readability(self):
        """
        Gets selected collection, passes it to readability analysis function.
        """
        i = self.get_coll_menu()
        if i is None:
            return
        print(self.colors['purple'], end='')
        readability.analyze(i)
        print(self.colors['end'], end='')

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
        print(self.colors['purple'], end='')
        image.analyze(coll, limit)
        print(self.colors['end'], end='')


if __name__ == '__main__':
    MenuText()


