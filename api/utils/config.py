import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("API_BASE_URL", "https://petstore.swagger.io/v2")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))
WEB_BASE_URL = os.getenv("WEB_BASE_URL", "https://www.saucedemo.com/")
WEB_TIMEOUT = int(os.getenv("WEB_TIMEOUT", "10"))
