"""
USER GENERATOR SCRIPT
This script generates 100 random user accounts with secure passwords.
It creates unique usernames and passwords that you can distribute to participants.

HOW TO USE:
1. Make sure the Flask app has been run at least once (to create the database)
2. Run this script: python generate_users.py
3. The script will create 'user_credentials.txt' with all the login information
4. Give each participant their unique username and password
"""

import random
import string
from app import app, db
from models import User

def generate_username(number):
    """
    Generate a username in the format: participant_001, participant_002, etc.
    This makes it easy to track which participant is which.
    """
    return f"participant_{number:03d}"  # :03d means 3 digits with leading zeros

def generate_password(length=10):
    """
    Generate a random secure password.
    The password will contain:
    - Lowercase letters (a-z)
    - Uppercase letters (A-Z) 
    - Digits (0-9)
    - Special characters (!@#$%^&*)
    
    This makes passwords hard to guess.
    """
    # Define the character sets to use
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special = "!@#$%^&*"
    
    # Combine all characters
    all_characters = lowercase + uppercase + digits + special
    
    # Ensure at least one of each type is included
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(special)
    ]
    
    # Fill the rest with random characters
    password += random.choices(all_characters, k=length-4)
    
    # Shuffle to make it random
    random.shuffle(password)
    
    return ''.join(password)

def create_users(count=100):
    """
    Create the specified number of user accounts.
    
    Args:
        count: Number of users to create (default: 100)
    
    Returns:
        A list of tuples containing (username, password) for each user
    """
    credentials = []
    
    # Use Flask's app context to access the database
    with app.app_context():
        # Clear existing users (optional - remove this if you want to keep existing users)
        print("Clearing existing users...")
        User.query.delete()
        db.session.commit()
        
        print(f"Creating {count} new user accounts...")
        
        for i in range(1, count + 1):
            # Generate username and password
            username = generate_username(i)
            password = generate_password()
            
            # Create new user
            user = User(username=username)
            user.set_password(password)  # Hash the password
            
            # Add to database
            db.session.add(user)
            
            # Store credentials for the output file
            credentials.append((username, password))
            
            # Show progress every 10 users
            if i % 10 == 0:
                print(f"  Created {i} users...")
        
        # Save all users to database
        db.session.commit()
        print(f"✓ Successfully created {count} users in the database!")
    
    return credentials

def save_credentials_to_file(credentials, filename='user_credentials.txt'):
    """
    Save all usernames and passwords to a text file.
    This file can be printed or distributed to participants.
    
    Args:
        credentials: List of (username, password) tuples
        filename: Name of the output file
    """
    with open(filename, 'w') as f:
        # Write header
        f.write("=" * 80 + "\n")
        f.write("QUESTIONNAIRE STUDY - PARTICIPANT LOGIN CREDENTIALS\n")
        f.write("=" * 80 + "\n\n")
        f.write("Please distribute these credentials to participants.\n")
        f.write("Each participant should receive ONE unique username and password.\n\n")
        f.write("=" * 80 + "\n\n")
        
        # Write each credential
        for username, password in credentials:
            f.write(f"Username: {username}\n")
            f.write(f"Password: {password}\n")
            f.write("-" * 80 + "\n")
        
        # Write footer
        f.write("\n" + "=" * 80 + "\n")
        f.write(f"Total: {len(credentials)} participant accounts\n")
        f.write("=" * 80 + "\n")
    
    print(f"✓ Credentials saved to '{filename}'")

def main():
    """
    Main function - runs when the script is executed.
    """
    print("\n" + "=" * 80)
    print("USER GENERATOR FOR QUESTIONNAIRE APP")
    print("=" * 80 + "\n")
    
    # Generate 100 users
    credentials = create_users(100)
    
    # Save to file
    save_credentials_to_file(credentials)
    
    print("\n" + "=" * 80)
    print("DONE!")
    print("=" * 80)
    print("\nNext steps:")
    print("1. Open 'user_credentials.txt' to see all login credentials")
    print("2. Distribute credentials to your 100 participants")
    print("3. Participants can now log in and complete the questionnaires")
    print("\n")

if __name__ == '__main__':
    main()
