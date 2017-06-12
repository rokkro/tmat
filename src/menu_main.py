try:
    from menu import Menu
    from analysis import menu_analysis
    from twitter import menu_twitter
    import menu_manage, mongo, export, config
except ImportError as e:
    print("Error",e)

class MenuMain(Menu):
    def __init__(self):
        super().__init__()
        menu = {
            1: menu_twitter.MenuTwitter(True).menu_stream,
            2: menu_twitter.MenuTwitter(False).menu_hist,
            3: menu_analysis.MenuText,
            4: export.menu_export,
            5: menu_manage.MenuManage,
            6: self.mongo_connect
        }
        if config.startup_connect:
            self.mongo_connect()
        while True:
            i = self.get_menu("MAIN", ["Stream Tweets.",
               "Historic Tweets.",
               "Analyze Tweets.",
               "Export as CSV.",
               "Manage Collections.",
               "MongoDB Connected = " + self.purple + str(mongo.connected) + self.end],
                "*Enter option number or [q] - quit.\n>>>")
            try:
                menu[i]()
            except KeyError:
                pass


if __name__ == "__main__":
    try:
        MenuMain()
    except KeyboardInterrupt:
        pass
