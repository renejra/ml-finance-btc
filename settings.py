# settings.py
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

QUANDLKEY = os.environ.get("QUANDLKEY")
