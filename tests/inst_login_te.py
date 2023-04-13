import os
from dotenv import load_dotenv
from instagrapi import Client
import unittest

def setup_insta_env():
    load_dotenv()
    INSTA_USERNAME = os.getenv("INSTA_USERNAME")
    INSTA_PASSWORD = os.getenv("INSTA_PASSWORD")
    print(INSTA_USERNAME, INSTA_PASSWORD)
    return INSTA_USERNAME, INSTA_PASSWORD

def login_insta():
    INSTA_USERNAME, INSTA_PASSWORD = setup_insta_env()
    cl = Client()
    cl.login(INSTA_USERNAME, INSTA_PASSWORD)
    print('logged in')

login_insta()

#i should kms after debugging it was a wrong var name in .env file fml