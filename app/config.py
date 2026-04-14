import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

# Get DATABASE_URL from environment variable (required on production)
DATABASE_URL = os.getenv('DATABASE_URL')

# If DATABASE_URL not set in environment, try to use a fallback for development
if DATABASE_URL is None:
    # This fallback should only be used for local development
    # On production (Render), DATABASE_URL MUST be set as an environment variable
    DATABASE_URL = 'postgresql+psycopg://reactivate_user:06gm6LKLjlJGmfjGr8tEqpbYQnV7E3Cv@dpg-d78u7u95pdvs73banbh0-a/reactivate'
    print("⚠️  WARNING: DATABASE_URL not set in environment. Using fallback (development only).")
else:
    print("✅ DATABASE_URL loaded from environment variable")

# Ensure proper PostgreSQL URI format for SQLAlchemy with psycopg
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql+psycopg://', 1)
elif DATABASE_URL.startswith('postgresql://'):
    DATABASE_URL = DATABASE_URL.replace('postgresql://', 'postgresql+psycopg://', 1)

# Validate DATABASE_URL
if not DATABASE_URL:
    raise ValueError("DATABASE_URL must be set. Check environment variables or .env file.")
