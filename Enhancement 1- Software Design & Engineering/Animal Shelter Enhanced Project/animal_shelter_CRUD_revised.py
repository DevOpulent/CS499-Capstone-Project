from pymongo import MongoClient
# Imported loggin here
import logging

# EJG Animal Shelter CRUD Operations - Enhanced Version
# Author: Edward Garcia
#
# This script provides CRUD operations for the AnimalShelter MongoDB database.
# Enhancements include:
# 1. Integrated logging into each method to provide detailed activity tracking.
# 2. Handled both typical and edge-case scenarios for CRUD operations.
#
# Purpose:
# This class is used to interact with the MongoDB collection for managing animal rescue data.
# Methods include create, read, update, and delete, each with enhanced logging to ensure reliable operation.

# Configure logging to capture detailed information about CRUD operations
logging.basicConfig(
    filename='animal_shelter.log',  # File to save logs to
    level=logging.INFO,  # Set logging level to INFO to capture info, warning, and error messages
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'  # Format of the log message
)

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, username, password, host='host.docker.internal', port=27017, db='AAC', collection='animals'):
        # Initialize the MongoClient to access MongoDB databases and collections.
        self.client = MongoClient(f'mongodb://{username}:{password}@{host}:{port}/?authSource=admin')
        self.database = self.client[db]
        self.collection = self.database[collection]
        logging.info("Connected to MongoDB collection: %s", collection)

    # Create method to implement the C in CRUD
    def create(self, data):
        """ Create a new document in the collection """
        try:
            if data is not None:
                # Insert operation to add new data to the collection.
                insert = self.collection.insert_one(data)  # Data should be a dictionary
                logging.info("Data inserted with acknowledgment: %s", insert.acknowledged)
                return insert.acknowledged
            else:
                raise ValueError("Nothing to save, data parameter is empty")
        except Exception as e:
            logging.error("Error occurred during creation: %s", str(e))
            raise

    # Read method to implement the R in CRUD
    def read(self, criteria=None):
        """ Read documents from the collection based on criteria """
        try:
            if criteria is not None:
                # Use regular expressions for case-insensitive search where necessary
                modified_criteria = {k: {"$regex": f"^{v}$", "$options": "i"} if isinstance(v, str) else v for k, v in criteria.items()}
                data = self.collection.find(modified_criteria, {"_id": False})
                logging.info("Read operation with criteria: %s", modified_criteria)
                return [document for document in data]
            else:
                # Read all documents if no criteria are provided.
                data = self.collection.find({}, {"_id": False})
                logging.info("Read operation with no criteria")
                return [document for document in data]
        except Exception as e:
            logging.error("Error occurred during read operation: %s", str(e))
            raise

    # Update method to implement the U in CRUD
    def update(self, criteria, update_data):
        """ Update documents based on criteria """
        try:
            if criteria is not None and update_data is not None:
                # Update operation to modify documents matching the criteria.
                result = self.collection.update_many(criteria, {'$set': update_data})
                logging.info("Update operation: matched %s documents, modified %s documents", result.matched_count, result.modified_count)
                return result.modified_count
            else:
                raise ValueError("Update parameters cannot be empty")
        except Exception as e:
            logging.error("Error occurred during update operation: %s", str(e))
            raise

    # Delete method to implement the D in CRUD
    def delete(self, criteria):
        """ Delete documents based on criteria """
        try:
            if criteria is not None:
                # Delete operation to remove documents that match the criteria.
                result = self.collection.delete_many(criteria)
                logging.info("Delete operation: deleted %s documents", result.deleted_count)
                return result.deleted_count
            else:
                raise ValueError("Delete parameters cannot be empty")
        except Exception as e:
            logging.error("Error occurred during delete operation: %s", str(e))
            raise
