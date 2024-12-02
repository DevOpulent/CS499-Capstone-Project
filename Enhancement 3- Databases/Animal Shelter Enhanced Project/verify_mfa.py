# MFA Verification Script for EJG Animal Shelter Dashboard
# Author: Edward Garcia

# Overview:
# I created this script to test the Multi-Factor Authentication (MFA) verification feature of the `UserManagement` class.
# It validates the functionality of verifying a user's One-Time Password (OTP) against the stored MFA secret.
# This feature confirms that only authorized users can access the application.

# Key Features Tested:
# 1. Verification of OTPs generated using the user's stored MFA secret.
# 2. Integration of the `verify_mfa` method with the user management system.
# 3. Security validation through the correct handling of valid and invalid OTPs.

from user_management import UserManagement

# Initialize UserManagement instance
# Establish a connection to the MongoDB database to manage user accounts and validate MFA.
user_manager = UserManagement("edwardgarcia5_snhu", "password", "host.docker.internal", 27017, "AAC")

# Prompt the user to enter their username.
username = input("Enter username: ")

# Prompt the user to enter their One-Time Password (OTP).
otp = input("Enter OTP: ")

# Call the verify_mfa method to validate the entered OTP against the stored MFA secret.
if user_manager.verify_mfa(username, otp):
    # Print a success message if the OTP verification is successful.
    print(f"OTP verified successfully for user '{username}'!")
else:
    # Print an error message if the OTP verification fails.
    print(f"OTP verification failed for user '{username}'.")
