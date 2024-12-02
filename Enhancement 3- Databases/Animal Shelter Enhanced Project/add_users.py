# User Management Test Script for Adding Users
# Author: Edward Garcia

# Overview:
# This script demonstrates the use of the `UserManagement` class to add new users to the MongoDB database
# and retrieve a list of all users. It is part of my Enhancement 3: Databases, showcasing secure
# user management practices such as password hashing and role-based user addition.

# Key Features:
# 1. Adding new users with secure password hashing using bcrypt.
# 2. Assigning roles to users for Role-Based Access Control (RBAC).
# 3. Verifying user addition by retrieving and displaying all users from the database.

from user_management import UserManagement

# Initialize the UserManagement class
# Connects to the MongoDB database for user-related operations.
user_manager = UserManagement("edwardgarcia5_snhu", "password", "host.docker.internal", 27017, "AAC")

# Define the users to add
# List of dictionaries where each dictionary represents a user with their username, password, and role.
users = [
    {"username": "user1", "password": "Secret", "role": "Guest"},
    {"username": "user2", "password": "Houston77", "role": "Regular User"},
    {"username": "user3", "password": "Astros44", "role": "Admin"}
]

# Add users to the database
# Iterates through the user list, adds each user to the MongoDB database, and prints the result of the operation.
for user in users:
    response = user_manager.add_user(user["username"], user["password"], user["role"])
    print(f"{user['username']} - {response}")

# Retrieve and display all users in the database
# Fetches all users from the database using the `get_all_users` method and prints their information.
all_users = user_manager.get_all_users()
print("Current Users in Database:")
for u in all_users:
    print(u)
