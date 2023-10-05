import os
import logger
import requests
from dotenv import load_dotenv


load_dotenv()
logger = logger.get_logger(__name__)

ENDPOINT = "http://walletgpt.info:5050"
# Retrieve/Replace this with your actual token 
TOKEN = "7067d4393182f1a06e3d6628cd492168" 
HEADERS = {
    'Authorization': f'Bearer {TOKEN}'
    }
