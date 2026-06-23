# Settings store System wide options and variables

import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://qae-assignment-tau.vercel.app"
USER_ID = os.getenv("USER_ID", "") 
DEFAULT_TIMEOUT = 10
