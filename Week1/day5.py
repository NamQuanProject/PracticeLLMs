import os
import requests
import json
from typing import Literal, List
from dotenv import load_dotenv
from IPython.display import Markdown, display, update_display
from openai import OpenAI
from bs4 import BeautifulSoup



api_key = os.getenv("OPENAI_API_KEY")
class Website:
    def __init__(self, url):
        self.url = url
        

load_dotenv()
