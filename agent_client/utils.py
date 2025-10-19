import os
import logging
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv("DEBUG", "false").lower() == "true"

logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def log_debug(msg):
    if DEBUG:
        logging.debug(msg)

def log_info(msg):
    logging.info(msg)

def log_error(msg):
    logging.error(msg)
