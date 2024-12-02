# User Management Module for EJG Animal Shelter Dashboard
# Author: Edward Garcia

# Overview:
# This module, `UserManagement`, I designed to handle secure user-related operations for the MongoDB database used in the EJG Animal Shelter Dashboard application. 
# The class provides functionality for managing user accounts, including authentication, role-based access control (RBAC), and multi-factor authentication (MFA). 

# Enhancement 3 additions:
# 1. **Security**: Implements bcrypt for secure password hashing and pyotp for MFA to enhance login security and mitigate unauthorized access.
# 2. **Logging**: Uses logging to track and record user-related activities like login attempts, role validation, MFA verification.
# 3. **Scalability**: Offers an extensible design for future enhancements to user management within the application.

# Enhancment 3 Imports:
# - **bcrypt**: Implements secure hashing of passwords with salt, ensuring protection against brute-force attacks.
# - **logging**: Facilitates structured logging of user management activities, aiding in debugging and auditing.
# - **pyotp**: Generates and verifies time-based one-time passwords (TOTP) for implementing MFA.


from pymongo import MongoClient
import bcrypt
import logging
import pyotp  # Import pyotp for MFA

# Configure a specific logger for user management
user_management_logger = logging.getLogger("user_management")
user_management_logger.setLevel(logging.INFO)

# Create a file handler for the user management log file
file_handler = logging.FileHandler("user_management.log")
file_handler.setLevel(logging.INFO)

# Create a formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the handler to the logger
user_management_logger.addHandler(file_handler)


class UserManagement:
    """
    Handles user-related operations for MongoDB.

    Features:
    - Add user accounts with hashed passwords and roles.
    - Authenticate users with optional multi-factor authentication (MFA).
    - Verify roles for role-based access control (RBAC).
    - Enable MFA for additional login security.
    - Log all significant events for auditing and debugging.
    """

    def __init__(self, username='edwardgarcia5_snhu', password='password', host='host.docker.internal', port=27017, db='AAC'):
        """
        Initializes the UserManagement class by connecting to the MongoDB database.

        """
        # Connect to the MongoDB database
        self.client = MongoClient(f'mongodb://{username}:{password}@{host}:{port}/?authSource=admin')
        self.database = self.client[db]
        # Define the collection for user data
        self.users_collection = self.database['users']
        user_management_logger.info("Connected to MongoDB 'users' collection.")

    def add_user(self, username, password, role):
        """
        Adds a new user with hashed password and assigned role.

        Input:
            username (str): Username of the new user.
            password (str): Plaintext password of the new user.
            role (str): Role assigned to the user.

        Returns:
            str: Success or error message.
        """
        try:
            # Check if the user already exists
            if self.users_collection.find_one({"username": username}):
                user_management_logger.warning("User with username '%s' already exists.", username)
                return "User already exists!"
            
            # Hash the password securely with bcrypt
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            user_data = {
                "username": username,
                "password": hashed_password.decode('utf-8'),  # Store as a string
                "role": role
            }
            # Insert the new user into the collection
            self.users_collection.insert_one(user_data)
            user_management_logger.info("User '%s' added successfully.", username)
            return "User added successfully!"
        except Exception as e:
            user_management_logger.error("Error adding user: %s", str(e))
            raise

    def get_all_users(self):
        """
        Retrieves all users with their roles for verification purposes.

        Returns:
            list: List of user dictionaries (excluding passwords).
        """
        try:
            # Retrieve all users, excluding sensitive fields like passwords
            return list(self.users_collection.find({}, {"_id": 0, "username": 1, "role": 1}))
        except Exception as e:
            user_management_logger.error("Error retrieving users: %s", str(e))
            raise

    def authenticate_user(self, username, password, otp=None):
        """
        Authenticates a user by verifying their credentials and optional MFA OTP.

        Input:
            username (str): Username to authenticate.
            password (str): Plaintext password.
            otp (str, optional): One-time password for MFA.

        Returns:
            dict: Authentication status and user role, or an error message.
        """
        try:
            # Retrieve the user from the database
            user = self.users_collection.find_one({"username": username})
            if user and bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
                user_management_logger.info("Password authentication successful for user '%s'.", username)
                if "mfa_secret" in user:
                    if otp and self.verify_mfa(username, otp):
                        user_management_logger.info("MFA verification successful for user '%s'.", username)
                        return {"status": "success", "role": user["role"]}
                    else:
                        user_management_logger.warning("MFA required or invalid OTP for user '%s'.", username)
                        return {"status": "fail", "message": "MFA required or invalid OTP."}
                return {"status": "success", "role": user["role"]}
            user_management_logger.warning("Authentication failed for username '%s'.", username)
            return {"status": "fail", "message": "Invalid username or password."}
        except Exception as e:
            user_management_logger.error("Error during authentication: %s", str(e))
            raise

    def check_permissions(self, username, required_role):
        """
        Checks if a user has the required role for access control.

        Input:
            username (str): Username to check.
            required_role (str): Role required to access a resource.

        Returns:
            bool: True if the user has the required role, False otherwise.
        """
        try:
            user = self.users_collection.find_one({"username": username})
            if user and user["role"].lower() == required_role.lower():
                user_management_logger.info("User '%s' has the required role '%s'.", username, required_role)
                return True
            user_management_logger.warning("User '%s' does not have the required role '%s'.", username, required_role)
            return False
        except Exception as e:
            user_management_logger.error("Error checking permissions for user '%s': %s", username, str(e))
            raise

    def enable_mfa(self, username):
        """
        Enables multi-factor authentication (MFA) for a user.

        Input:
            username (str): Username for whom to enable MFA.

        Returns:
            dict: Status and secret for MFA.
        """
        try:
            secret = pyotp.random_base32()  # Generate a unique MFA secret
            result = self.users_collection.update_one({"username": username}, {"$set": {"mfa_secret": secret}})
            if result.modified_count == 1:
                user_management_logger.info("MFA enabled for user '%s'.", username)
                return {"status": "success", "secret": secret}
            user_management_logger.warning("Failed to enable MFA for user '%s'.", username)
            return {"status": "fail", "message": "User not found or MFA already enabled."}
        except Exception as e:
            user_management_logger.error("Error enabling MFA: %s", str(e))
            raise

    def verify_mfa(self, username, otp):
        """
        Verifies a one-time password (OTP) for MFA.

        Input:
            username (str): Username for whom to verify MFA.
            otp (str): One-time password provided by the user.

        Returns:
            bool: True if the OTP is valid, False otherwise.
        """
        try:
            user = self.users_collection.find_one({"username": username})
            if user and "mfa_secret" in user:
                totp = pyotp.TOTP(user["mfa_secret"])
                if totp.verify(otp):
                    user_management_logger.info("MFA verification successful for user '%s'.", username)
                    return True
            user_management_logger.warning("MFA verification failed for user '%s'.", username)
            return False
        except Exception as e:
            user_management_logger.error("Error verifying MFA for user '%s': %s", username, str(e))
            raise


# Expose the logger for external use
__all__ = ["UserManagement", "user_management_logger"]
