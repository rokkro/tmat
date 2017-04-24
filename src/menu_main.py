from analysis import menu_analysis
from twitter import menu_twitter
from display import color,get_menu
import menu_list,mongo,exp_csv,config

def menu_main():

    def connect():
        print(color.YELLOW, end='')
        mongo.mongo_connection()
        print(color.END, end='')

    if config.startup_connect:
        connect()
    menu = {
        1: menu_twitter.menu_scrape,
        2: menu_analysis.menu_sentiment,
        3: menu_analysis.menu_image,
        4: csv.setup,
        5: menu_list.menu_manage,
        6: connect
    }
    while True:
        i = get_menu("[1] - Scrape tweets.\n"
          "[2] - Perform Sentiment Analysis.\n"
          "[3] - Perform Image Analysis.\n"
          "[4] - Export as csv.\n"
          "[5] - Manage Collections.\n"
          "[6] - MongoDB Connected = " + color.YELLOW + str(mongo.connected) + color.END,
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
