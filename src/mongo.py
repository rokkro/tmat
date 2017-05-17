try:
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure
except ImportError as e:
    print("Install missing modules with pip!\nError:", e)
    quit()

client = None
connected = False


def mongo_connection():
    global client, connected
    if connected:
        print("Disconnected from MongoDB.")
        client.close()
        client = None
        connected = False
    else:
        print("Attempting connection to MongoDB...")
        try:
            client = MongoClient(serverSelectionTimeoutMS=30)  # localhost timeout
            client.server_info()  # forces connection verification
            print("Connection Succeeded!")
            connected = True
        except (ConnectionFailure, KeyboardInterrupt) as e:
            print("Error: MongoDB not connected:", e)
        except Exception as e:
            print("Error:", e)


def get_dbnames():
    return client.database_names()

def get_collections(db_name):
    return client[db_name].collection_names()
