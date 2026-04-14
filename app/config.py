import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL is None:
    DATABASE_URL = 'postgresql://reactivate_q9ms_user:6RfYltaUu10ME0w6gFf46aTo7mWAu3Jg@dpg-d7f9047lk1mc73d82mag-a/reactivate_q9ms'
elif DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql+psycopg://', 1)
elif DATABASE_URL.startswith('postgresql://'):
    DATABASE_URL = DATABASE_URL.replace('postgresql://', 'postgresql+psycopg://', 1)
