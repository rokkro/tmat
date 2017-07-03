try:
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure
except ImportError as e:
    print("Import Error in mongo.py:", e)
    quit()

client = None # Access to client
connected = False # Connection status


def mongo_connection():
    # Connects/disconnects from MongoDB service
    global client, connected
    if connected:
        print("*Disconnected from MongoDB.")
        client.close()
        client = None
        connected = False
    else:
        print("*Attempting connection to MongoDB")
        try:
            client = MongoClient(serverSelectionTimeoutMS=30)  # localhost timeout, increase if necessary
            client.server_info()  # forces connection verification
            print("*Connection Succeeded!")
            connected = True
        except (ConnectionFailure, KeyboardInterrupt) as e:
            print("*MongoDB connection failed:", e)
        except Exception as e:
            print("Error:", e)


def get_dbnames():
    # Returns List of DB names
    return client.database_names()

def get_collections(db_name):
    # Returns list of collections in the DB
    return client[db_name].collection_names()
