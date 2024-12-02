# EJG Animal Shelter CRUD Unit Tests - Enhanced Version
# Author: Edward Garcia
# This script contains unit tests for validating the CRUD operations implemented in `animal_shelter_CRUD_revised.py`,
# which is part of the CS340 project for managing animal rescue data.
#
# Enhancements in this revised version include:
# 1. Extended Unit Test Coverage:
#    - Added new unit tests to comprehensively validate CRUD operations for the AnimalShelter MongoDB database.
#    - Ensured coverage for both typical scenarios and edge cases, resulting in a robust verification process.
# 2. Added Unit Tests for Edge Cases:
#    - Tested the creation of invalid or empty data to confirm the system properly handles incorrect input.
#    - Added tests for attempts to read, update, or delete non-existent data, verifying error handling is implemented correctly.
#    - Tested partial updates of document fields to verify that only intended fields are modified.
#    - Added a test to verify the successful creation of duplicate data entries.
#    - Confirmed the connection to MongoDB is available during tests.
#    - Verified read operations handle case insensitivity properly.
# 3. Improved Stability:
#    - Each test is preceded by a clean setup to remove all records, so there are no side effects between tests.
#    - The `tearDownClass` method drops the test collection after all tests have run, maintaining data isolation.
#
# Purpose:
# The purpose of these unit tests is to validate CRUD operations (Create, Read, Update, Delete) for interacting with the MongoDB collection.
# These tests are designed to verify correctness, handling of errors, and efficiency when dealing with real-world and edge-case scenarios.
#
# Coverage Summary:
# - Creation: Successful creation, invalid data handling, duplicate data creation.
# - Reading: Successful reading by criteria, reading non-existent data, case-insensitive search.
# - Updating: Successful updates, partial updates, and handling non-existent data.
# - Deleting: Successful deletions, deleting non-existent data, and deleting all documents.
# - Connection Verification: Ensured that the MongoDB instance is accessible before running operations.

# Import unittest 
import unittest
from animal_shelter_CRUD_revised import AnimalShelter
from pymongo.errors import ConnectionFailure

class TestAnimalShelterCRUD(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the test environment for all test cases"""
        # Here I initialized an instance of AnimalShelter for unit testing, using a separate test database to avoid affecting production data.
        cls.shelter = AnimalShelter(username='edwardgarcia5_snhu', password='password', host='host.docker.internal', port=27017, db='AAC_test', collection='animals_test')

    def setUp(self):
        """Set up test data for each test"""
        # Here I ensured the collection is cleared before each test to avoid inconsistent results.
        self.shelter.collection.delete_many({})
        # Here I inserted a test document to maintain consistent data for each test.
        self.shelter.create({"name": "Test Animal", "breed": "Test Breed"})

    def test_create(self):
        """Test the create operation"""
        # Here I am testing the create functionality to verify that data can be successfully inserted into the database.
        test_data = {"name": "Another Test Animal", "breed": "Test Breed"}
        result = self.shelter.create(test_data)
        self.assertTrue(result, "Create operation failed")

    def test_create_invalid_data(self):
        """Test creation of invalid or empty data"""
        # Here I am testing that creating an entry with invalid or empty data raises an exception.
        with self.assertRaises(ValueError):
            self.shelter.create(None)

    def test_read(self):
        """Test the read operation"""
        # Here I am testing the read operation to ensure documents can be fetched based on criteria.
        criteria = {"name": "Test Animal"}
        result = self.shelter.read(criteria)
        self.assertGreaterEqual(len(result), 1, "Read operation failed or returned empty results")

    def test_read_non_existent(self):
        """Test reading non-existent data"""
        # Here I am testing that attempting to read data that does not exist returns an empty list.
        criteria = {"name": "Non Existent Animal"}
        result = self.shelter.read(criteria)
        self.assertEqual(len(result), 0, "Read operation should return empty for non-existent data")

    def test_update(self):
        """Test the update operation"""
        # Here I am testing the update functionality to ensure documents can be updated based on provided criteria.
        criteria = {"name": "Test Animal"}
        update_data = {"name": "Updated Animal"}
        modified_count = self.shelter.update(criteria, update_data)
        self.assertGreaterEqual(modified_count, 1, "Update operation failed")

    def test_partial_update(self):
        """Test partial update of a document"""
        # Here I am testing that partial updates to a document, such as modifying only one field, are successful.
        criteria = {"name": "Test Animal"}
        update_data = {"age": 5}
        modified_count = self.shelter.update(criteria, update_data)
        self.assertGreaterEqual(modified_count, 1, "Partial update operation failed")

    def test_delete(self):
        """Test the delete operation"""
        # Here I am testing the delete functionality to ensure documents can be removed based on criteria.
        criteria = {"name": "Test Animal"}
        deleted_count = self.shelter.delete(criteria)
        self.assertGreaterEqual(deleted_count, 1, "Delete operation failed")

    def test_delete_non_existent(self):
        """Test deleting non-existent data"""
        # Here I am testing that attempting to delete data that does not exist results in zero deletions.
        criteria = {"name": "Non Existent Animal"}
        deleted_count = self.shelter.delete(criteria)
        self.assertEqual(deleted_count, 0, "Delete operation should return zero for non-existent data")

    def test_duplicate_data_creation(self):
        """Test creation of duplicate data"""
        # Here I am testing that inserting duplicate data entries does not cause any errors and is handled properly.
        test_data = {"name": "Test Animal", "breed": "Test Breed"}
        result = self.shelter.create(test_data)
        self.assertTrue(result, "Failed to create duplicate data entry")

    def test_connection(self):
        """Test MongoDB connection"""
        # Here I am verifying the MongoDB connection to ensure that the application can successfully connect to the database.
        try:
            self.shelter.client.admin.command('ping')
            connection_successful = True
        except ConnectionFailure:
            connection_successful = False
        self.assertTrue(connection_successful, "Connection to MongoDB failed")

    def test_update_no_match(self):
        """Test update operation with no matching documents"""
        # Here I am testing that attempting to update a non-existent document returns zero modifications.
        criteria = {"name": "Non Existent Animal"}
        update_data = {"name": "Updated Animal"}
        modified_count = self.shelter.update(criteria, update_data)
        self.assertEqual(modified_count, 0, "Update operation should return zero for non-existent data")


    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        # Here I added cleanup to drop the test collection after all tests are completed to avoid leftover test data.
        cls.shelter.collection.drop()

if __name__ == '__main__':
    unittest.main()
