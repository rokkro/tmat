from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

client = None
connected = False

def mongo_handler():
    global client, connected
    if connected:
        print("Disconnected from MongoDB.")
        client.close()
        connected = False
    else:
        print("Attempting connection to MongoDB...")
        try:
            client = MongoClient()
            print("Connection Succeeded!")
            connected = True
        except ConnectionFailure as e:
            print("Error: MongoDB not connected:", e)
        except Exception as e:
            print("Error:", e)
