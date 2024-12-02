# MFA Enablement Script for EJG Animal Shelter Dashboard
# Author: Edward Garcia

# Overview:
# This script tests the Multi-Factor Authentication (MFA) enablement feature of the `UserManagement` class.
# It demonstrates the process of enabling MFA for a user and generating a corresponding QR code for easy setup in an MFA app.

# Key Features Tested:
# 1. MFA secret generation and storage in the database utilizing pyotp.
# 2. Displaying a QR code for easy configuration in MFA apps.
# 3. Verifying the functionality of the `enable_mfa` method in `UserManagement`.

from user_management import UserManagement
import pyotp
import qrcode

# Initialize UserManagement instance
# Establish a connection to the MongoDB database to manage user accounts.
user_manager = UserManagement("edwardgarcia5_snhu", "password", "host.docker.internal", 27017, "AAC")

# Prompt the user to enter a username for MFA enablement.
username = input("Enter username: ")

# Call the enable_mfa method to enable MFA for the specified user.
response = user_manager.enable_mfa(username)

if response["status"] == "success":
    # Print a success message and display the generated MFA secret for the user.
    print(f"MFA enabled for {username}.")
    print(f"Use the following secret to configure your MFA app: {response['secret']}")
    
    # Generate a TOTP object for the user's MFA secret.
    totp = pyotp.TOTP(response["secret"])
    
    # Create a provisioning URI that includes the username and app name for QR code generation.
    qr_data = totp.provisioning_uri(username, issuer_name="AnimalShelterApp")
    
    # Generate and display a QR code for the user to scan with their MFA app.
    print("Scan the QR code below in your MFA app:")
    qrcode.make(qr_data).show()
else:
    # Print an error message if the MFA enablement process failed.
    print(response["message"])
