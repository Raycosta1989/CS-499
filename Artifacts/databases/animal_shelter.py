from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):
    """CRUD operations for Animal collection in MongoDB"""

    def __init__(self, username, password):
        # MongoDB connection credentials passed dynamically
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 30273
        DB = 'AAC'
        COL = 'animals'

        # Connect to MongoDB using dynamic user authentication
        uri = f'mongodb://{username}:{password}@{HOST}:{PORT}'
        self.client = MongoClient(uri)
        self.database = self.client[DB]
        self.collection = self.database[COL]

    # Create method to implement the C in CRUD
    def create(self, data):
        if data is not None:
            try:
                result = self.collection.insert_one(data)
                return True
            except Exception as e:
                print(f"Insert failed: {e}")
                return False
        else:
            raise Exception("Nothing to save, because data parameter is empty")

    # Read method to implement the R in CRUD
    def read(self, criteria=None):
        try:
            if criteria is not None:
                data = list(self.collection.find(criteria, {"_id": False}))
            else:
                data = list(self.collection.find({}, {"_id": False}))
            return data
        except Exception as e:
            print(f"Read failed: {e}")
            return []

    # Update method to implement the U in CRUD
    def update(self, filter_criteria, update_values):
        if filter_criteria is not None and update_values is not None:
            try:
                result = self.collection.update_many(filter_criteria, {"$set": update_values})
                return result.modified_count
            except Exception as e:
                print(f"Update failed: {e}")
                return 0
        else:
            raise Exception("Update failed: Missing criteria or update values")

    # Delete method to implement the D in CRUD
    def delete(self, delete_criteria):
        if delete_criteria is not None:
            try:
                result = self.collection.delete_many(delete_criteria)
                return result.deleted_count
            except Exception as e:
                print(f"Delete failed: {e}")
                return 0
        else:
            raise Exception("Delete failed: No criteria provided")