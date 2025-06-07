# Furry Convention Registration System

This is a simple registration system for a furry convention built with Flask. It
allows users to register with email (and optionally Telegram), edit their
profile, and administrators to manage registrations.

## Features
- Email registration and login
- Telegram login via the Telegram Login Widget (optional)
- User profile with photo upload
- Admin dashboard with user statistics and management

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. (Optional) Set environment variables if you want to override the defaults:
   - `SECRET_KEY` – secret key for Flask (defaults to `dev-secret-key`)
   - `TELEGRAM_BOT_TOKEN` – token of your Telegram bot for login verification
   - `DATABASE_URL` – SQLAlchemy database URI (defaults to the local `reg.db`)
   - `UPLOAD_FOLDER` – path for uploaded photos (defaults to `uploads/`)
3. Run the application:
   ```bash
   python run.py
   ```
4. Open `http://localhost:5000` in your browser.

Telegram login is disabled by default.  To enable it, replace `YOUR_BOT_USERNAME`
in `app/templates/login.html` with your bot's username and set the
`TELEGRAM_BOT_TOKEN` environment variable.

Uploaded profile photos are stored in the folder specified by `UPLOAD_FOLDER` (default `uploads/`).
