"""
QUICK START SCRIPT
Run this file to set up and start the questionnaire app.
Usage: python quick_start.py
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a shell command and display the result"""
    print(f"\n{'='*60}")
    print(f"🔧 {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        print(f"✓ {description} - DONE!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False

def main():
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║   FLASK QUESTIONNAIRE APP - AUTOMATIC SETUP                ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    # Step 1: Install packages
    print("\n📦 Installing required Python packages...")
    if not run_command(
        f"{sys.executable} -m pip install Flask Flask-SQLAlchemy Werkzeug",
        "Installing Flask and dependencies"
    ):
        print("\n⚠️  Package installation failed. You may need to run:")
        print(f"    {sys.executable} -m pip install --user Flask Flask-SQLAlchemy Werkzeug")
        response = input("\nDo you want to continue anyway? (y/n): ")
        if response.lower() != 'y':
            return
    
    # Step 2: Generate users
    print("\n\n👥 Generating 100 participant accounts...")
    if not run_command(
        f"{sys.executable} generate_users.py",
        "Creating user accounts"
    ):
        print("\n⚠️  User generation failed. The app may still work if users exist.")
    
    # Step 3: Instructions
    print("\n\n" + "="*60)
    print("✨ SETUP COMPLETE! ✨")
    print("="*60)
    
    print("\n📋 What was created:")
    print("  • Database with all tables (instance/questionnaire.db)")
    print("  • 100 user accounts with random passwords")
    print("  • user_credentials.txt file with all login information")
    
    print("\n🚀 To start the application:")
    print(f"  1. Run: {sys.executable} app.py")
    print("  2. Open: http://127.0.0.1:5000 in your browser")
    print("  3. Login with any credentials from user_credentials.txt")
    
    print("\n📖 For detailed instructions, see README.md")
    
    # Ask if user wants to start now
    print("\n" + "="*60)
    response = input("Do you want to start the Flask app now? (y/n): ")
    
    if response.lower() == 'y':
        print("\n🚀 Starting Flask application...")
        print("Press Ctrl+C to stop the server\n")
        try:
            subprocess.run([sys.executable, "app.py"])
        except KeyboardInterrupt:
            print("\n\n👋 Application stopped. Goodbye!")
    else:
        print("\n👋 Setup complete! Start the app anytime with: python app.py")

if __name__ == '__main__':
    main()
