try:
    from menu import Menu
    from analysis import sentiment, image, readability
except ImportError as e:
    print("Error:",e)


class MenuText(Menu):
    def __init__(self):
        super().__init__()
        menu = {
            1: self.sub_init,
            2: self.sub_analysis,
            3: self.sub_readability,
            4: self.sub_image
        }
        while True:
            inpt = self.get_menu("ANALYSIS",["Setup Text Analysis.", "Run Sentiment Analysis.", "Run Readability Analysis.", "Run Image Analysis."],
                "*Enter an option number or [r] - return.\n>>>")
            if inpt == 'r':
                return
            menu[inpt]()

    def sub_init(self):
        print(self.purple, end='')
        sentiment.initialize()
        print(self.end, end='')

    def sub_analysis(self):
        i = self.get_coll()
        if i is None:
            return
        print(self.purple, end='')
        sentiment.analyze(i)
        print(self.end, end='')

    def sub_readability(self):
        i = self.get_coll()
        if i is None:
            return
        print(self.purple, end='')
        readability.analyze(i)
        print(self.end, end='')

    def sub_image(self):
        coll = self.get_coll()
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


