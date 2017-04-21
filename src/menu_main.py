from analysis import menu_analysis
from twitter import menu_twitter
from display import color,get_input
import menu_list,mongo

def menu_main():
    print(color.YELLOW, end='')
    mongo.mongo_connection()
    print(color.END, end='')
    menu = {
        1: menu_twitter.menu_scrape,
        2: menu_analysis.menu_sentiment,
        3: menu_analysis.menu_image,
        4: exit,
        5: menu_list.menu_manage,
        6: mongo.mongo_connection
    }
    while True:
        i = get_input("[1] - Scrape tweets.\n"
          "[2] - Perform Sentiment Analysis.\n"
          "[3] - Perform Image Analysis.\n"
          "[4] - Export to CSV.\n"
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
