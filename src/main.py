import twitter
def inputNum(msg, lim): #for typecasting to an int without a bazillion try..except's
    print(msg)
    while True:
        inpt = input("Enter option number:")
        try:
            inpt = int(inpt)
        except ValueError:
            continue
        if inpt > lim or inpt < 1:
            continue
        else:
            return inpt


def mode():
    input1 = inputNum("\n[1] - Scrape tweets.\n"
          "[2] - Perform Sentiment Analysis.\n"
          "[3] - Data Presentation.\n"
          "[4] - List Tweet Collections in DB.\n"
          "[5] - Purge temporary data\n",5)
    if input1 == 1:
        s = twitter.Setup()
        search = s.search()
        limit = s.limit()
        inputNum("[1] - Search = " + search + "\n[2] - Limit = " + str(limit) + "\n[3] - Temporary Collection = " + str(s.temp) +
              "\n[4] - Image Filtering and Analysis = False\n[5] - Collection Name = '" + s.coll_name +
              "' (time will update when streaming starts)\n",5)
        #twitter.stream()
        print(1)
    elif input1 == 2:
        #yes
        print(2)
    elif input1 == 3:
        #3
        print(3)
    elif input1 == 4:
        #
        print(4)
    elif input1 == 5:
        ##
        print(5)
    elif input1 == 6:
        #yes
        print(6)
mode()
