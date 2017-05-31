try:
    from analysis import menu_analysis
    from twitter import menu_twitter
    from menu import Color, get_menu, divider
    import menu_manage, mongo, export, config
except ImportError as e:
    print("Error",e)

def menu_main():
    def sub_connect():
        divider()
        print(Color.YELLOW, end='')
        mongo.mongo_connection()
        print(Color.END, end='')
    if config.startup_connect:
        sub_connect()
    menu = {
        1: menu_twitter.menu_stream,
        2: menu_twitter.menu_hist,
        3: menu_analysis.menu_text,
        4: export.menu_export,
        5: menu_manage.menu_manage,
        6: sub_connect
    }
    while True:
        i = get_menu("MAIN",["Stream Tweets.",
                      "Historic Tweets.",
                      "Analyze Tweets.",
                      "Export as CSV.",
                      "Manage Collections.",
                      "MongoDB Connected = " + Color.YELLOW + str(mongo.connected) + Color.END],
                     "*Enter option number or [q] - quit.\n>>>", 6)
        try:
            menu[i]()
        except KeyError:
            pass

if __name__ == "__main__":
    try:
        menu_main()
    except KeyboardInterrupt:
        pass
