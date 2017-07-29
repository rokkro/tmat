try:
    from config import mongo_timeout
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure
except ImportError as e:
    print("Import Error in mongo.py:", e)
    quit()

class Mongo:
    _client = None  # Access to client
    _connected = False  # Connection status

    def mongo_connection(self,connect_only=False):
        # Connects/disconnects from MongoDB service
        if self.is_connected() and connect_only:
            return
        if self.is_connected():
            Mongo._client.close()
            Mongo._client = None
            Mongo._connected = False
            return "*MongoDB Disconnected."
        else:
            try:
                Mongo._client = MongoClient(serverSelectionTimeoutMS=mongo_timeout)  # localhost timeout
                Mongo._client.server_info()  # forces connection verification
                Mongo._connected = True
                return "*MongoDB Connection Succeeded!"
            except (ConnectionFailure, KeyboardInterrupt) as e:
                return "*MongoDB Connection Failed:" + str(e)
            except Exception as e:
                return "Error in mongo.py:" + str(e)

    def get_db_names(self):
        # Returns List of DB names
        return Mongo._client.database_names()

    def get_collections(self,db_name):
        # Returns list of collections in the DB
        return Mongo._client[db_name].collection_names()

    def get_client(self):
        # Returns client
        return Mongo._client

    def is_connected(self):
        # Returns True if connected to mongod
        if Mongo._connected:
            return True
        return False