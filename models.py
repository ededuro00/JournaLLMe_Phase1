"""
DATABASE MODELS
This file defines the structure of our database tables using SQLAlchemy.
SQLAlchemy is an ORM (Object-Relational Mapping) tool that lets us work with 
databases using Python classes instead of writing SQL queries.
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Create a database instance that we'll use throughout the app
db = SQLAlchemy()


class User(db.Model):
    """
    USER TABLE
    Stores information about each participant who logs into the system.
    Each user has a unique ID and password for authentication.
    """
    __tablename__ = 'users'
    
    # Primary key - unique identifier for each user
    id = db.Column(db.Integer, primary_key=True)
    
    # Username - must be unique (no two users can have same username)
    username = db.Column(db.String(50), unique=True, nullable=False)
    
    # Password - stored as a hash for security (not plain text!)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Timestamp when user account was created
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships: Links to other tables
    # This allows us to easily access all responses from a user
    responses = db.relationship('Response', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """
        Convert plain text password to a secure hash.
        We never store passwords in plain text for security!
        """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """
        Check if the provided password matches the stored hash.
        Returns True if correct, False otherwise.
        """
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        """String representation of the User object (useful for debugging)"""
        return f'<User {self.username}>'


class Response(db.Model):
    """
    RESPONSE TABLE
    Stores each answer a user gives to a questionnaire item.
    Each response includes the rating (1-5 or 0-3) AND a text explanation.
    """
    __tablename__ = 'responses'
    
    # Primary key - unique identifier for each response
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign key - links this response to a specific user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Which questionnaire this response belongs to ('SWLS' or 'PHQ9')
    questionnaire_type = db.Column(db.String(10), nullable=False)
    
    # Which question number (1-5 for SWLS, 1-9 for PHQ9)
    question_number = db.Column(db.Integer, nullable=False)
    
    # The rating the user selected (numeric value)
    rating = db.Column(db.Integer, nullable=False)
    
    # The text explanation for why they gave that rating
    explanation = db.Column(db.Text, nullable=False)
    
    # Timestamp when this response was submitted
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        """String representation of the Response object"""
        return f'<Response user={self.user_id} q={self.questionnaire_type}-{self.question_number}>'


class QuestionnaireCompletion(db.Model):
    """
    QUESTIONNAIRE COMPLETION TABLE
    Tracks which questionnaires each user has completed.
    This helps us know if a user finished SWLS, PHQ9, or both.
    """
    __tablename__ = 'questionnaire_completions'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign key - which user completed this questionnaire
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Which questionnaire was completed ('SWLS' or 'PHQ9')
    questionnaire_type = db.Column(db.String(10), nullable=False)
    
    # When it was completed
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Make sure a user can only complete each questionnaire once
    __table_args__ = (db.UniqueConstraint('user_id', 'questionnaire_type', name='_user_questionnaire_uc'),)
    
    def __repr__(self):
        """String representation of the QuestionnaireCompletion object"""
        return f'<Completion user={self.user_id} type={self.questionnaire_type}>'
