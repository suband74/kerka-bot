import os
from dotenv import load_dotenv


load_dotenv()

USER = "postgres"
PASSWORD = "postgres"
DATABASE = "postgres"
HOST = "db"
BOT_TOKEN = os.getenv('BOT_TOKEN')

POSTGRES_DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}/{DATABASE}"

QIWI_PRIV_KEY = os.getenv('PRIVED')

ID = os.getenv('ID')