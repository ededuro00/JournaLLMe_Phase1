"""
MAIN FLASK APPLICATION
This is the heart of our web application. It creates the Flask app,
sets up routes (URLs), and handles all user interactions.
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, User, Response, QuestionnaireCompletion
from config import Config
import os

# Create the Flask application instance
app = Flask(__name__)

# Load configuration settings from config.py
app.config.from_object(Config)

# Initialize the database with our app
db.init_app(app)

# Create the instance folder if it doesn't exist
# This is where our SQLite database file will be stored
os.makedirs(os.path.join(app.root_path, 'instance'), exist_ok=True)


# QUESTIONNAIRE DATA
# These dictionaries contain all the questions for each questionnaire

# SATISFACTION WITH LIFE SCALE (SWLS)
# A 5-item scale measuring global life satisfaction.
# Each question uses a 7-point scale from 1 (Strongly Disagree) to 7 (Strongly Agree).
SWLS_QUESTIONS = {
    1: "In most ways my life is close to my ideal.",
    2: "The conditions of my life are excellent.",
    3: "I am satisfied with my life.",
    4: "So far I have gotten the important things I want in life.",
    5: "If I could live my life over, I would change almost nothing."
}

# Rating scale for SWLS questions.
# Users select a number from 1 to 7.
SWLS_SCALE = {
    1: "Strongly Disagree",
    2: "Disagree",
    3: "Slightly Disagree",
    4: "Neither Agree nor Disagree",
    5: "Slightly Agree",
    6: "Agree",
    7: "Strongly Agree"
}

# PATIENT HEALTH QUESTIONNAIRE-9 (PHQ-9)
# A 9-item scale for measuring depression severity.
# Users rate how often they've experienced each symptom over the last 2 weeks.
# Scale: 0 (Not at all) to 3 (Nearly every day)
PHQ9_QUESTIONS = {
    1: "Little interest or pleasure in doing things",
    2: "Feeling down, depressed, or hopeless",
    3: "Trouble falling or staying asleep, or sleeping too much",
    4: "Feeling tired or having little energy",
    5: "Poor appetite or overeating",
    6: "Feeling bad about yourself - or that you are a failure or have let yourself or your family down",
    7: "Trouble concentrating on things, such as reading the newspaper or watching television",
    8: "Moving or speaking so slowly that other people could have noticed. Or the opposite - being so fidgety or restless that you have been moving around a lot more than usual",
    9: "Thoughts that you would be better off dead, or of hurting yourself in some way"
}

# Rating scale for PHQ-9 questions.
# Measures frequency of symptoms over the past 2 weeks.
PHQ9_SCALE = {
    0: "Not at all",
    1: "Several days",
    2: "More than half the days",
    3: "Nearly every day"
}


# HELPER FUNCTIONS

def login_required(f):
    """
    DECORATOR FUNCTION
    This is a wrapper that protects routes - users must be logged in to access them.
    If not logged in, they're redirected to the login page.
    """
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def get_user_completion_status(user_id):
    """
    Check which questionnaires a user has completed.
    Returns a dictionary with True/False for each questionnaire.
    """
    completions = QuestionnaireCompletion.query.filter_by(user_id=user_id).all()
    return {
        'swls': any(c.questionnaire_type == 'SWLS' for c in completions),
        'phq9': any(c.questionnaire_type == 'PHQ9' for c in completions)
    }


# ROUTES (URL Endpoints)
# Each route handles a different page or action in our app

@app.route('/')
def index():
    """
    HOME PAGE / ROOT URL
    If user is logged in, redirect to dashboard.
    Otherwise, show the login page.
    """
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    LOGIN PAGE
    GET request: Show the login form
    POST request: Process login credentials and authenticate user
    """
    # If already logged in, go to dashboard
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        # Get username and password from the form
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Look up user in database
        user = User.query.filter_by(username=username).first()
        
        # Check if user exists and password is correct
        if user and user.check_password(password):
            # Success! Store user_id in session (this keeps them logged in)
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'Welcome, {user.username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            # Login failed
            flash('Invalid username or password. Please try again.', 'danger')
    
    # Show the login form
    return render_template('login.html')


@app.route('/logout')
def logout():
    """
    LOGOUT
    Clear the session (log user out) and redirect to login page.
    """
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    """
    DASHBOARD PAGE
    Shows the user which questionnaires are available and which they've completed.
    This is the main hub where users choose which questionnaire to take.
    """
    user_id = session['user_id']
    completion_status = get_user_completion_status(user_id)
    
    return render_template('dashboard.html', 
                         completion_status=completion_status,
                         username=session['username'])


@app.route('/swls', methods=['GET', 'POST'])
@login_required
def swls():
    """
    SATISFACTION WITH LIFE SCALE (SWLS) QUESTIONNAIRE
    GET: Show the questionnaire form
    POST: Save responses and mark as complete
    """
    user_id = session['user_id']
    
    # Check if already completed
    already_completed = QuestionnaireCompletion.query.filter_by(
        user_id=user_id, 
        questionnaire_type='SWLS'
    ).first()
    
    if already_completed:
        flash('You have already completed the SWLS questionnaire.', 'info')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        # Process the submitted questionnaire
        try:
            # Loop through each question and save the response
            for q_num in range(1, 6):  # SWLS has 5 questions
                rating = request.form.get(f'q{q_num}_rating')
                explanation = request.form.get(f'q{q_num}_explanation')
                
                # Validate that both rating and explanation are provided
                if not rating or not explanation:
                    flash(f'Please complete question {q_num} (both rating and explanation).', 'danger')
                    return redirect(url_for('swls'))
                
                # Create a new Response record
                response = Response(
                    user_id=user_id,
                    questionnaire_type='SWLS',
                    question_number=q_num,
                    rating=int(rating),
                    explanation=explanation.strip()
                )
                db.session.add(response)
            
            # Mark questionnaire as completed
            completion = QuestionnaireCompletion(
                user_id=user_id,
                questionnaire_type='SWLS'
            )
            db.session.add(completion)
            
            # Save everything to database
            db.session.commit()
            
            flash('SWLS questionnaire completed successfully!', 'success')
            return redirect(url_for('complete', q_type='swls'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')
            return redirect(url_for('swls'))
    
    # Show the questionnaire form
    return render_template('swls.html', 
                         questions=SWLS_QUESTIONS,
                         scale=SWLS_SCALE)


@app.route('/phq9', methods=['GET', 'POST'])
@login_required
def phq9():
    """
    PATIENT HEALTH QUESTIONNAIRE-9 (PHQ-9)
    GET: Show the questionnaire form
    POST: Save responses and mark as complete
    """
    user_id = session['user_id']
    
    # Check if already completed
    already_completed = QuestionnaireCompletion.query.filter_by(
        user_id=user_id, 
        questionnaire_type='PHQ9'
    ).first()
    
    if already_completed:
        flash('You have already completed the PHQ-9 questionnaire.', 'info')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        # Process the submitted questionnaire
        try:
            # Loop through each question and save the response
            for q_num in range(1, 10):  # PHQ-9 has 9 questions
                rating = request.form.get(f'q{q_num}_rating')
                explanation = request.form.get(f'q{q_num}_explanation')
                
                # Validate that both rating and explanation are provided
                if not rating or not explanation:
                    flash(f'Please complete question {q_num} (both rating and explanation).', 'danger')
                    return redirect(url_for('phq9'))
                
                # Create a new Response record
                response = Response(
                    user_id=user_id,
                    questionnaire_type='PHQ9',
                    question_number=q_num,
                    rating=int(rating),
                    explanation=explanation.strip()
                )
                db.session.add(response)
            
            # Mark questionnaire as completed
            completion = QuestionnaireCompletion(
                user_id=user_id,
                questionnaire_type='PHQ9'
            )
            db.session.add(completion)
            
            # Save everything to database
            db.session.commit()
            
            flash('PHQ-9 questionnaire completed successfully!', 'success')
            return redirect(url_for('complete', q_type='phq9'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')
            return redirect(url_for('phq9'))
    
    # Show the questionnaire form
    return render_template('phq9.html', 
                         questions=PHQ9_QUESTIONS,
                         scale=PHQ9_SCALE)


@app.route('/complete/<q_type>')
@login_required
def complete(q_type):
    """
    COMPLETION PAGE
    Shows a thank you message after completing a questionnaire.
    Users can return to dashboard to take the other questionnaire.
    """
    questionnaire_name = 'SWLS' if q_type == 'swls' else 'PHQ-9'
    return render_template('complete.html', 
                         questionnaire_name=questionnaire_name)


# DATABASE INITIALIZATION
# This creates all the tables when the app first runs

with app.app_context():
    """
    app.app_context() is needed to access the database.
    This block runs when the application starts.
    """
    db.create_all()  # Create all database tables if they don't exist
    print("Database tables created successfully!")


# RUN THE APPLICATION
# This starts the web server when you run this file directly

if __name__ == '__main__':
    """
    Start the Flask development server.
    debug=True means:
    - The server restarts automatically when you change code
    - You see detailed error messages
    - DON'T use debug=True in production!
    """
    app.run(debug=True, host='127.0.0.1', port=5000)
