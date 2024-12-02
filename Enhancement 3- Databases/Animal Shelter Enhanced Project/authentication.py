# User Authentication Test Script for EJG Animal Shelter Dashboard
# Author: Edward Garcia

# Overview:
# This script tests the authentication functionality of the `UserManagement` class for Enhancement 3 in the
# EJG Animal Shelter Dashboard.
# It verifies the login credentials provided by the user and determines access based on authentication status.
# This aligns with my Enhancement 3: Databases by implementing secure user authentication with password hashing.


from user_management import UserManagement

# Initialize the UserManagement class
# Establishes a connection to the MongoDB database for authentication checks.
user_manager = UserManagement("edwardgarcia5_snhu", "password", "host.docker.internal", 27017, "AAC")

# Prompt the user to input their username for authentication.
username = input("Enter username: ")

# Prompt the user to input their password for authentication.
password = input("Enter password: ")

# Call the authenticate_user method to validate the provided credentials.
response = user_manager.authenticate_user(username, password)

# Display the result of the authentication process.
if response["status"] == "success":
    # Print a success message with the user's role if authentication is successful.
    print(f"Login successful! Role: {response['role']}")
else:
    # Print an error message if authentication fails.
    print(response["message"])
