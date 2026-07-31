from playwright.sync_api import Playwright
import os
from dotenv import load_dotenv
import requests
Back_end_url = os.getenv("BASE_URL")
def get_token():
    response =requests.post(f"{Back_end_url}users/login" , json = {"email": "saiviveksapelly@gmail.com", "password": "142536475869"})
    return response.json().get("data").get("token")
    
    