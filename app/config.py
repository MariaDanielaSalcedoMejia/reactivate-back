import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL is None:
    DATABASE_URL = 'postgresql://reactivate_user:06gm6LKLjlJGmfjGr8tEqpbYQnV7E3Cv@dpg-d78u7u95pdvs73banbh0-a/reactivate'
elif DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
