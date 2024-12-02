from pymongo import MongoClient

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """
    
    def __init__(self, username, password, host='host.docker.internal', port=27017, db='AAC', collection='animals'):
        # Initializing the MongoClient. This helps to 
        # access the MongoDB databases and collections. 
        self.client = MongoClient(f'mongodb://{username}:{password}@{host}:{port}/?authSource=admin')
        self.database = self.client[db]
        self.collection = self.database[collection]

    # Create method to implement the C in CRUD
    def create(self, data):
        if data is not None:
            insert = self.collection.insert_one(data)  # data should be a dictionary
            return insert.acknowledged
        else:
            raise Exception("Nothing to save, because data parameter is empty")

    # Read method to implement the R in CRUD
    def read(self, criteria=None):
        if criteria is not None:
            data = self.collection.find(criteria, {"_id": False})
            return [document for document in data]
        else:
            data = self.collection.find({}, {"_id": False})
            return [document for document in data]

    # Update method to implement the U in CRUD
    def update(self, criteria, update_data):
        if criteria is not None and update_data is not None:
            result = self.collection.update_many(criteria, {'$set': update_data})
            return result.modified_count
        else:
            raise Exception("Update parameters cannot be empty")

    # Delete method to implement the D in CRUD
    def delete(self, criteria):
        if criteria is not None:
            result = self.collection.delete_many(criteria)
            return result.deleted_count
        else:
            raise Exception("Delete parameters cannot be empty")
