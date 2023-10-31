from os import getenv
import os
from dotenv import load_dotenv

load_dotenv()

API_ID = getenv("API_ID")
API_HASH = getenv("API_HASH")
SESSION = getenv("SESSION")
SEND_ID = getenv("SEND_ID")