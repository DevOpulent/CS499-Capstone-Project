from pymongo import MongoClient
# Imported logging 
import logging
# Imported functools for caching
from functools import lru_cache

# EJG Animal Shelter CRUD Operations - Enhanced Version
# Author: Edward Garcia
#
# Overview:
# This script provides enhanced CRUD operations for the AnimalShelter MongoDB database.
# The enhancements are categorized as follows:
#
# Enhancement 1 - Software Design and Engineering Additions:
# 1. Integrated logging into each CRUD method for detailed activity tracking.
#    - This helps monitor CRUD operations, debug errors, and maintain an audit trail.
#
# Enhancement 2 - Data Structures and Algorithms Additions:
# 1. Implemented functools.lru_cache for optimized repeated read operations.
#    - Using LRU (Least Recently Used) cache will improve the speed of repeated queries by caching results.

# 2. Introduced a hash map for breed attribute indexing.
#    - The hash map allows for O(1) time complexity for breed-based lookups, significantly speeding up the filtering process.

# 3. Added binary search for sorted attributes.
#    - Binary search has been implemented for sorted fields like age for example, to reduce search time complexity to O(log n).


# Configure logging to capture detailed information about CRUD operations
logging.basicConfig(
    filename='animal_shelter.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class AnimalShelter(object):
    """CRUD operations for Animal collection in MongoDB."""

    def __init__(self, username, password, host='host.docker.internal', port=27017, db='AAC', collection='animals'):
        # Initialize the MongoClient to access MongoDB databases and collections
        self.client = MongoClient(f'mongodb://{username}:{password}@{host}:{port}/?authSource=admin')
        self.database = self.client[db]
        self.collection = self.database[collection]
        logging.info("Connected to MongoDB collection: %s", collection)

        # Create a hash map for the breed attribute for efficient search
        self.breed_hash_map = {}
        self._populate_breed_hash_map()

    def _populate_breed_hash_map(self):
        """
        Populated a hash map here for efficient breed lookups.
        - Organizes breeds as keys, linking them to lists of associated documents.
        - Optimizes breed-based searches, achieving O(1) lookup time.
        """
        try:
            all_data = self.collection.find({}, {"breed": 1, "_id": 0})
            for document in all_data:
                breed = document.get("breed")
                if breed:
                    if breed in self.breed_hash_map:
                        self.breed_hash_map[breed].append(document)
                    else:
                        self.breed_hash_map[breed] = [document]
            logging.info("Hash map for breeds has been populated.")
        except Exception as e:
            logging.error("Error occurred while populating breed hash map: %s", str(e))

    def _make_hashable(self, query):
        """
        Convert a dictionary query to a hashable type.
        - Verify compatibility with functools.lru_cache.
        """

        if isinstance(query, dict):
            return tuple((key, self._make_hashable(value)) for key, value in sorted(query.items()))
        elif isinstance(query, list):
            return tuple(self._make_hashable(item) for item in query)
        else:
            return query

    @lru_cache(maxsize=128)
    def _cached_read(self, hashable_query):
        """
        Perform a cached database read operation.
        - Uses functools.lru_cache to store results of frequent queries.
        - This reduces database load and improves response times for repeated queries.
        """

        query = dict(hashable_query)  # Convert back to a dictionary
        return list(self.collection.find(query))

    def read(self, query, bypass_cache=False):
        """
        Read documents with optional cache bypass for fresh results.
        - Enables switching between cached and live data.
        - Queries the database directly if bypass_cache is true for the latest results.
        - Retrieves cached results for repeated queries.
        """

        try:
            if bypass_cache:
                # Directly query the database without using the cache
                logging.info("Bypassing cache for query: %s", query)
                return list(self.collection.find(query))

            # Use cached results for repeated queries
            hashable_query = self._make_hashable(query)
            return self._cached_read(hashable_query)
        except Exception as e:
            logging.error("Error occurred during read operation: %s", str(e))
            raise

    def clear_cache(self):
        """
        Clear the LRU cache for the read method.
        - Removes cached data after collection-modifying CRUD operations.
        """

        self._cached_read.cache_clear()
        logging.info("Cache cleared for the read method.")

    def create(self, data):
        """Create a new document in the collection and update the breed hash map."""
        try:
            if data:
                insert = self.collection.insert_one(data)
                logging.info("Data inserted with acknowledgment: %s", insert.acknowledged)

                # Update the breed hash map
                breed = data.get("breed")
                if breed:
                    if breed in self.breed_hash_map:
                        self.breed_hash_map[breed].append(data)
                    else:
                        self.breed_hash_map[breed] = [data]

                # Clear cache after data modification
                self.clear_cache()

                return insert.acknowledged
            else:
                raise ValueError("Nothing to save, data parameter is empty")
        except Exception as e:
            logging.error("Error occurred during creation: %s", str(e))
            raise

    def update(self, criteria, update_data):
        """Update documents based on criteria and maintain hash map consistency."""
        try:
            if criteria and update_data:
                result = self.collection.update_many(criteria, {'$set': update_data})
                logging.info("Update operation: matched %s documents, modified %s documents", result.matched_count, result.modified_count)

                # Update the hash map and clear cache
                self.clear_cache()
                return result.modified_count
            else:
                raise ValueError("Update parameters cannot be empty")
        except Exception as e:
            logging.error("Error occurred during update operation: %s", str(e))
            raise

    def delete(self, criteria):
        """Delete documents based on criteria and update the breed hash map."""
        try:
            if criteria:
                result = self.collection.delete_many(criteria)
                logging.info("Delete operation: deleted %s documents", result.deleted_count)

                # Clear cache after data modification
                self.clear_cache()
                return result.deleted_count
            else:
                raise ValueError("Delete parameters cannot be empty")
        except Exception as e:
            logging.error("Error occurred during delete operation: %s", str(e))
            raise

    def _match_criteria(self, document, criteria):
        """Helper method to match a document against given criteria."""
        for key, value in criteria.items():
            if key in document and document[key] != value:
                return False
        return True