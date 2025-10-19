import requests
import os
from utils import log_info, log_error
from dotenv import load_dotenv

load_dotenv()
CHROME_EXTENSION_URL = os.getenv("CHROME_EXTENSION_URL")

async def send_to_chrome(parsed_plan: dict):
    log_info(f"Sending plan to Chrome: {parsed_plan}")
    try:
        response = requests.post(CHROME_EXTENSION_URL, json=parsed_plan)
        log_info(f"Chrome response: {response.status_code}")
        return response.json()
    except Exception as e:
        log_error(f"Chrome communication failed: {e}")
        return {"error": str(e)}
