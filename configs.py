import os
from dotenv import load_dotenv

load_dotenv()


ADMIN_URL = os.getenv('ADMIN_URL')
GOOGLE_CLIENT_ID=os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')