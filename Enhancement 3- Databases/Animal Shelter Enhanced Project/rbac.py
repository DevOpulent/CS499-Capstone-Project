# Role-Based Access Control (RBAC) Script for EJG Animal Shelter Dashboard
# Author: Edward Garcia

# Overview:
# This script illustrates the Role-Based Access Control (RBAC) functionality of the `UserManagement` class.
# RBAC makes sure users can only access features and functionalities that align with their assigned roles such as
# guest, regular user, and admin. 

# Key Features Tested:
# 1. Validation of user roles to determine access permissions.
# 2. Integration of the `check_permissions` method with the user management system.

from user_management import UserManagement

# Initialize UserManagement instance
# Establishes a connection to the MongoDB database for user role verification.
user_manager = UserManagement("edwardgarcia5_snhu", "password", "host.docker.internal", 27017, "AAC")

# Prompt the user to enter their username for role verification.
username = input("Enter username: ")

# Prompt the user to specify the required role for access.
required_role = input("Enter the required role: ")

# Call the check_permissions method to verify if the user has the required role.
if user_manager.check_permissions(username, required_role):
    # Print a success message if the user has the necessary permissions.
    print(f"Access granted for {username} to {required_role} features.")
else:
    # Print an error message if the user lacks the necessary permissions.
    print(f"Access denied for {username}. Insufficient permissions.")
