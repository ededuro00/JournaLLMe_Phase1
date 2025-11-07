"""
APPLICATION CONFIGURATION
This file contains all the configuration settings for our Flask app.
Configuration keeps all our settings in one place for easy management.
"""

import os

class Config:
    """
    Base configuration class.
    All settings that our Flask app needs are defined here.
    """
    
    # SECRET KEY - Used by Flask for session security and encryption
    # In production, this should be a random, secret value
    # Never share this key publicly!
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production-12345'
    
    # DATABASE CONFIGURATION
    # We're using SQLite, which stores everything in a single file
    # The database file will be created in the 'instance' folder
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'questionnaire.db')
    
    # Turn off Flask-SQLAlchemy's modification tracking feature
    # (We don't need it and it uses extra memory)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # SESSION CONFIGURATION
    # Sessions keep users logged in as they navigate between pages
    SESSION_COOKIE_HTTPONLY = True  # Protect cookies from JavaScript access
    SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
    PERMANENT_SESSION_LIFETIME = 3600  # Session expires after 1 hour (3600 seconds)
