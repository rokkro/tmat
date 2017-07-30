try:
    from config import mongo_timeout
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure
except ImportError as e:
    print("Import Error in mongo.py:", e)
    quit()

class Mongo:
    _client = None  # Access to client

    def mongo_connection(self):
        # Connects/disconnects from MongoDB service
        if self.is_connected():
            Mongo._client.close()
            Mongo._client = None
            return False
        else:
            try:
                Mongo._client = MongoClient(serverSelectionTimeoutMS=mongo_timeout)  # localhost timeout
                status = self.test_connection()
                if status is True:
                    return True
                return status
            except Exception as e:
                return e

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
        if self.test_connection() is True:
            return True
        return False

    def test_connection(self):
        try:
            Mongo._client.server_info()
            return True
        except AttributeError as e:
            return e
        except ConnectionFailure as e:
            return e