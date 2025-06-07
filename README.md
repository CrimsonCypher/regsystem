# Furry Convention Registration System

This is a simple registration system for a furry convention built with Flask. It allows users to register with email or Telegram, edit their profile, and administrators to manage registrations.

## Features
- Email registration and login
- Telegram login via the Telegram Login Widget
- User profile with photo upload
- Admin dashboard with user statistics and management

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set environment variables as needed:
   - `SECRET_KEY` – secret key for Flask
   - `TELEGRAM_BOT_TOKEN` – token of your Telegram bot for login verification
   - `DATABASE_URL` – SQLAlchemy database URI (default uses SQLite `reg.db`)
3. Run the application:
   ```bash
   python run.py
   ```
4. Open `http://localhost:5000` in your browser.

To enable Telegram login, replace `YOUR_BOT_USERNAME` in `app/templates/login.html` with your bot's username and set `TELEGRAM_BOT_TOKEN` environment variable.

Uploaded profile photos are stored in the folder specified by `UPLOAD_FOLDER` (default `uploads/`).
