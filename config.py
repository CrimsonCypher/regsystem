class Config:
    """Basic configuration for running the app locally."""

    # Use a local SQLite database by default. No external database URL is
    # required to get started.
    SQLALCHEMY_DATABASE_URI = "sqlite:///reg.db"

    # Flask's secret key for session management.  This default value makes the
    # application runnable without setting environment variables.
    SECRET_KEY = "dev-secret-key"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Store uploaded files in a local folder.
    UPLOAD_FOLDER = "uploads"

    # Telegram integration is disabled by default.  Set this value if you wish
    # to enable Telegram login.
    TELEGRAM_BOT_TOKEN = ""
