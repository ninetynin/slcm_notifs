from instagrapi import Client
import os
from dotenv import load_dotenv

# load_dotenv()

# INSTA_USERNAME = os.getenv("INSTAGRAM_USERNAME")
# INSTA_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

cl = Client()
try:
    cl.load_settings("session.json")
    print('logged in without password')
except:
    print('session.json not found')
# cl.login(INSTA_USERNAME, INSTA_PASSWORD)
# cl.dump_settings("session.json")
cl.get_timeline_feed()

#fuck u can login with just session.json now icant upload this on github