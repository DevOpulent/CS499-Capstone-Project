# MongoDB Connection Test Script
# Author: Edward Garcia

# Overview:
# This script tests the connection to the MongoDB database.
# It checks that the MongoDB client can successfully connect to the specified database and lists the available collections.

from pymongo import MongoClient

# Test connection to MongoDB
try:
    # Initialize the MongoClient with the appropriate credentials and host information.
    client = MongoClient('mongodb://edwardgarcia5_snhu:password@host.docker.internal:27017/?authSource=admin')
    
    # If the connection is successful, print confirmation.
    print("Connected successfully!")
    
    # Access the specified database ('AAC') and print the available collections.
    db = client['AAC']
    print("Available collections:", db.list_collection_names())

# Handle and print any exceptions that occur during the connection attempt.
except Exception as e:
    print("Connection failed:", e)
