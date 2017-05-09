from analysis import menu_analysis
from twitter import menu_twitter
from display import Color, get_menu
import menu_list, mongo, export, config

def menu_main():
    def sub_connect():
        print(Color.YELLOW, end='')
        mongo.mongo_connection()
        print(Color.END, end='')

    if config.startup_connect:
        sub_connect()
    menu = {
        1: menu_twitter.menu_scrape,
        2: menu_analysis.menu_sentiment,
        3: menu_analysis.menu_image,
        4: export.setup,
        5: menu_list.menu_manage,
        6: sub_connect
    }
    while True:
        i = get_menu(["Scrape tweets.",
                      "Perform Sentiment Analysis.",
                      "Perform Image Analysis.",
                      "Export as csv.",
                      "Manage Collections.",
                      "MongoDB Connected = " + Color.YELLOW + str(mongo.connected) + Color.END],
                     "*Enter option number or [q] - quit.\n>>>", 7)
        try:
            menu[i]()
        except KeyError:
            pass


if __name__ == "__main__":
    try:
        menu_main()
    except KeyboardInterrupt:
        pass
