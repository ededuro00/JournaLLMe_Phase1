# 📋 Flask Questionnaire Application

A complete web application for conducting psychological research with the Satisfaction With Life Scale (SWLS) and Patient Health Questionnaire-9 (PHQ-9). Each response requires both a rating and a text explanation.

## 🌟 Features

- **User Authentication**: Secure login system with pre-generated credentials for 100 participants
- **Two Validated Questionnaires**:
  - **SWLS**: 5-item life satisfaction assessment (7-point scale)
  - **PHQ-9**: 9-item depression screening tool (4-point frequency scale)
- **Text Explanations**: Every question requires both a numerical rating AND a text explanation
- **Progress Tracking**: Dashboard shows completion status for each questionnaire
- **Beautiful UI**: Modern, responsive design that works on all devices
- **SQLite Database**: All responses securely stored in a local database
- **Data Privacy**: Anonymous, confidential data collection

## 📁 Project Structure

```
questionnaire-app/
├── app.py                      # Main Flask application (routes, logic)
├── models.py                   # Database models (User, Response, QuestionnaireCompletion)
├── config.py                   # Application configuration settings
├── generate_users.py           # Script to create 100 user accounts
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── instance/                   # Database storage folder (created automatically)
│   └── questionnaire.db        # SQLite database (created on first run)
├── templates/                  # HTML templates (Jinja2)
│   ├── base.html              # Base template (navigation, footer)
│   ├── login.html             # Login page
│   ├── dashboard.html         # Main dashboard
│   ├── swls.html              # SWLS questionnaire form
│   ├── phq9.html              # PHQ-9 questionnaire form
│   └── complete.html          # Completion confirmation page
└── static/                     # Static files (CSS, JavaScript)
    ├── css/
    │   └── style.css          # All styling
    └── js/
        └── main.js            # JavaScript functionality
```

## 🚀 Installation & Setup

### Prerequisites

- **Python 3.8 or higher** ([Download Python](https://www.python.org/downloads/))
- **pip** (usually comes with Python)
- **Terminal/Command Prompt**

### Step-by-Step Setup

#### 1. Open Terminal and Navigate to Project Folder

```bash
cd "/Users/edoardo/Desktop/untitled folder/untitled folder/folder/.github/untitled folder"
```

#### 2. Create a Virtual Environment (Recommended)

**Why?** This keeps your project dependencies isolated from other Python projects.

```bash
# Create virtual environment
python3 -m venv venv

# Activate it (macOS/Linux)
source venv/bin/activate

# You'll see (venv) appear in your terminal prompt
```

#### 3. Install Required Packages

```bash
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- Flask-SQLAlchemy (database management)
- Werkzeug (security utilities)

#### 4. Generate User Credentials

This creates 100 participant accounts with random passwords:

```bash
python generate_users.py
```

**Output**: A file called `user_credentials.txt` containing all 100 username/password pairs.

**Example credentials:**
```
Username: participant_001
Password: aB3#xY9mP2
--------------------
Username: participant_002
Password: kL8$qR5nW4
```

#### 5. Run the Application

```bash
python app.py
```

You should see:
```
Database tables created successfully!
 * Running on http://127.0.0.1:5000
 * Restarting with stat
```

#### 6. Open in Your Browser

Navigate to: **http://127.0.0.1:5000** or **http://localhost:5000**

## 👥 Using the Application

### For Researchers

1. **Distribute Credentials**: Give each participant their unique username and password from `user_credentials.txt`
2. **Share the URL**: Provide participants with the application URL
3. **Monitor Progress**: (Optional) Add an admin panel to track completion rates
4. **Export Data**: Access the SQLite database to retrieve all responses

### For Participants

1. **Login**: Use the provided username and password
2. **Dashboard**: View available questionnaires
3. **Complete Questionnaires**: Answer all questions with ratings AND explanations
4. **Switch Between Questionnaires**: Can complete in any order
5. **Logout**: Click logout when finished

## 📊 Database Structure

### Tables

#### **users**
- `id`: Unique user identifier
- `username`: Login username (e.g., participant_001)
- `password_hash`: Securely hashed password
- `created_at`: Account creation timestamp

#### **responses**
- `id`: Response ID
- `user_id`: Which user submitted this response
- `questionnaire_type`: 'SWLS' or 'PHQ9'
- `question_number`: Which question (1-5 for SWLS, 1-9 for PHQ-9)
- `rating`: The numerical rating selected
- `explanation`: The text explanation provided
- `submitted_at`: Timestamp

#### **questionnaire_completions**
- `id`: Completion record ID
- `user_id`: Which user completed
- `questionnaire_type`: Which questionnaire ('SWLS' or 'PHQ9')
- `completed_at`: Completion timestamp

## 🔧 How It Works (For Flask Beginners)

### What is Flask?

Flask is a **web framework** - it handles:
- **Routing**: Mapping URLs to functions (e.g., `/login` shows login page)
- **Templates**: Generating HTML pages with dynamic data
- **Sessions**: Keeping users logged in as they navigate
- **Forms**: Processing user input from web forms

### Key Concepts

#### 1. Routes (in app.py)

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    # This function runs when someone visits /login
    # GET: Show the login form
    # POST: Process login credentials
```

#### 2. Templates (HTML files)

Templates use **Jinja2** syntax to insert Python data into HTML:
```html
<h2>Welcome, {{ username }}!</h2>
<!-- {{ }} means: insert the value of username here -->
```

#### 3. Database Models (models.py)

Instead of writing SQL, we define Python classes:
```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
```

SQLAlchemy automatically creates the database tables!

#### 4. Sessions

Flask sessions keep track of logged-in users:
```python
session['user_id'] = user.id  # Log in
del session['user_id']         # Log out
```

### Application Flow

1. **User visits /** → Redirected to `/login`
2. **User submits login form** → Check credentials → Create session → Redirect to `/dashboard`
3. **User clicks "Start SWLS"** → Redirected to `/swls` → Form displayed
4. **User fills out SWLS** → POST to `/swls` → Validate → Save to database → Redirect to `/complete`
5. **User clicks "Dashboard"** → Shows completion status
6. **User clicks "Logout"** → Clear session → Redirect to `/login`

## 🛠️ Customization

### Change Number of Users

Edit `generate_users.py`:
```python
credentials = create_users(200)  # Change 100 to any number
```

### Add Questions

Edit `app.py`:
```python
SWLS_QUESTIONS = {
    1: "Your question here",
    2: "Another question",
    # Add more...
}
```

### Change Colors

Edit `static/css/style.css`:
```css
:root {
    --primary-color: #4A90E2;  /* Change this hex code */
    --success-color: #28A745;  /* And this */
}
```

### Add Email Notifications

Install Flask-Mail:
```bash
pip install Flask-Mail
```

Then add email configuration in `config.py` and email sending logic in `app.py`.

## 📈 Accessing Research Data

### Option 1: Using DB Browser for SQLite (Recommended)

1. Download [DB Browser for SQLite](https://sqlitebrowser.org/)
2. Open `instance/questionnaire.db`
3. Browse, query, and export data

### Option 2: Python Script

```python
from app import app, db
from models import User, Response, QuestionnaireCompletion

with app.app_context():
    # Get all responses
    responses = Response.query.all()
    
    # Export to CSV
    import csv
    with open('responses.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['User ID', 'Questionnaire', 'Question', 'Rating', 'Explanation'])
        for r in responses:
            writer.writerow([r.user_id, r.questionnaire_type, r.question_number, 
                           r.rating, r.explanation])
```

### Option 3: SQL Queries

```bash
sqlite3 instance/questionnaire.db

# Example queries:
SELECT COUNT(*) FROM users;
SELECT * FROM responses WHERE questionnaire_type = 'SWLS';
SELECT user_id, COUNT(*) FROM responses GROUP BY user_id;
```

## 🐛 Troubleshooting

### "Port 5000 already in use"

Change the port in `app.py`:
```python
app.run(debug=True, port=5001)  # Use 5001 instead
```

### "No module named 'flask'"

Your virtual environment isn't activated or packages aren't installed:
```bash
source venv/bin/activate  # Activate venv
pip install -r requirements.txt  # Reinstall
```

### "Database is locked"

Close any other programs accessing the database. Or restart the Flask app.

### Lost user_credentials.txt

Just run `generate_users.py` again - it will regenerate all credentials.

## 🔒 Security Notes

### For Development (Current Setup)

- ✅ Passwords are hashed (not stored in plain text)
- ✅ Sessions are signed and encrypted
- ✅ SQL injection protection (via SQLAlchemy)
- ⚠️ Using development server (not production-ready)
- ⚠️ Debug mode enabled (shows detailed errors)

### For Production Deployment

If deploying to a real server:

1. **Change SECRET_KEY** in `config.py` to a random secret value
2. **Disable debug mode**: `app.run(debug=False)`
3. **Use a production server**: Install `gunicorn` or `waitress`
4. **Enable HTTPS**: Use SSL certificates
5. **Set up proper authentication**: Consider adding CAPTCHA, rate limiting
6. **Regular backups**: Backup `questionnaire.db` regularly

## 📚 Learning Resources

### Flask Basics
- [Official Flask Tutorial](https://flask.palletsprojects.com/en/3.0.x/tutorial/)
- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

### SQLAlchemy
- [SQLAlchemy Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/)
- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/)

### HTML/CSS
- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Learn)
- [W3Schools](https://www.w3schools.com/)

## 📞 Support

If you encounter issues:

1. Check the terminal for error messages
2. Review this README
3. Check Flask documentation
4. Google the specific error message

## 📄 License

This project is provided for research and educational purposes. Feel free to modify and adapt for your needs.

---

## 🎉 You're All Set!

Your questionnaire application is ready to use. Participants can now:
- ✅ Log in with their credentials
- ✅ Complete SWLS and PHQ-9 questionnaires
- ✅ Provide detailed explanations for each response
- ✅ Track their progress

All data is automatically saved to the database for your research analysis.

**Good luck with your study! 📊🔬**
