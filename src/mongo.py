try:
    from config import mongo_timeout
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure
except ImportError as e:
    print("Import Error in mongo.py:", e)
    quit()


_client = None  # Access to client
_connected = False  # Connection status


def mongo_connection(connect_only=False):
    # Connects/disconnects from MongoDB service
    global _client,_connected
    if is_connected() and not connect_only:
        print("*Disconnected from MongoDB.")
        _client.close()
        _client = None
        _connected = False
    else:
        print("*Attempting connection to MongoDB")
        try:
            _client = MongoClient(serverSelectionTimeoutMS=mongo_timeout)  # localhost timeout
            _client.server_info()  # forces connection verification
            print("*Connection Succeeded!")
            _connected = True
        except (ConnectionFailure, KeyboardInterrupt) as e:
            print("*MongoDB connection failed:", e)
        except Exception as e:
            print("Error in mongo.py:", e)


def get_db_names():
    # Returns List of DB names
    return _client.database_names()


def get_collections(db_name):
    # Returns list of collections in the DB
    return _client[db_name].collection_names()


def get_client():
    # Returns client
    return _client


def is_connected():
    # Returns True if connected to mongod
    if _connected:
        return True
    return False
