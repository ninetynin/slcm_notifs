import os
from dotenv import load_dotenv
from instagrapi import Client
from PIL import Image, ImageDraw, ImageFont, ImageColor


load_dotenv()

def setup_insta_env():
    INSTA_USERNAME = os.getenv("INSTAGRAM_USERNAME")
    INSTA_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")
    return INSTA_USERNAME, INSTA_PASSWORD

def login_insta():
    INSTA_USERNAME, INSTA_PASSWORD = setup_insta_env()
    cl = Client()
    #cl.load_settings("session.json")
    try:
        cl.load_settings("session.json")
    except:
        print('session.json not found')
    cl.login(INSTA_USERNAME, INSTA_PASSWORD)
    cl.dump_settings("session.json")
    cl.get_timeline_feed()
    return cl

def post_story(new_list):
    cl = login_insta()
    print('logged in')
    img = Image.new(mode="RGBA", size=(720,1080), color='black')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('arial.ttf', 50)
    text = 'hello'
    text_bbox = draw.textbbox((0, 0), text, font=font)
    wd = text_bbox[2] - text_bbox[0]
    ht = text_bbox[3] - text_bbox[1]
    draw.text(((720-wd)/2, (1080-ht)/2), text, fill='white', font=font)
    img.show()
    img.save('images/dumps/insta_dump.png')
    png_img = Image.open('images/dumps/insta_dump.png')
    png_img.convert("RGB").save('images/dumps/insta_dump.jpg')    
    # abs_path = os.path.join(os.path.dirname(__file__), path)
    path = 'images/dumps/insta_dump.jpg'
    cl.photo_upload_to_story(path)

    #its working the error was the fieltype why are all errors like this i should read docs properly fml


post_story(['hello'])