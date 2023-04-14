import os
from dotenv import load_dotenv
import asyncio
from pyppeteer import launch
import keras_ocr
import csv
from instagrapi import Client # there's a heavy chance this might be broken in future then find a alternative
from PIL import Image, ImageDraw, ImageFont, ImageColor
import logging

#disabling logging and printing as it takes too much time ing github actions but not sure if thats the reason

load_dotenv()
# logger = logging.getLogger()

def setup_env():
    SLCM_USERNAME = os.getenv("SLCM_USERNAME")
    SLCM_PASSWORD = os.getenv("SLCM_PASSWORD")
    return SLCM_USERNAME, SLCM_PASSWORD

def setup_insta_env():
    INSTA_USERNAME = os.getenv("INSTAGRAM_USERNAME")
    INSTA_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")
    return INSTA_USERNAME, INSTA_PASSWORD

def login_insta():
    INSTA_USERNAME, INSTA_PASSWORD = setup_insta_env()
    cl = Client()
    session = cl.load_settings("session.json")

    login_via_session = False
    login_via_pw = False

    if session:
        try:
            cl.set_settings(session)
            c1.login(INSTA_USERNAME,INSTA_PASSWORD)

            try:
                cl.get_timeline_feed()
            except login_required:
                # logger.info("Session expired")
                # print  
                old_session = cl.get_settings()
                # use the same device uuids across logins
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])
                cl.login(INSTA_USERNAME, INSTA_PASSWORD)
                login_via_session = True
        except Exception as e:
            # logger.info("Session expired")
    
    if not login_via_session:
        try:
            if cl.login(INSTA_USERNAME, INSTA_PASSWORD):
                login_via_pw = True
                cl.dump_settings("session.json")
        except Exception as e:
            # logger.info("Login failed with password")

    if not login_via_pw and not login_via_session:
        raise Exception("Couldn't login user with either password or session")
    
    return cl

def post_story(new_list):
    cl = login_insta()
    # logger.info('logged in')
    for li in new_list:
        img = Image.new(mode="RGBA", size=(720, 1280), color='black')
        draw = ImageDraw.Draw(img)
        count = 0

        if len(li) > 22:
            lines = [li[i:i+22] for i in range(0, len(li), 22)]
            text = "\n".join(lines)
            count += 1
        
        if count == 0:
            font = ImageFont.truetype('fonts/Lora-Medium.ttf', 50)
        else:
            for i in range(count):
                font = ImageFont.truetype('fonts/Lora-Medium.ttf', 50 - (i*10))  
        
        text_bbox = draw.textbbox((0, 0), text, font=font)
        wd = text_bbox[2] - text_bbox[0]
        ht = text_bbox[3] - text_bbox[1]
        draw.text(((720-wd)/2, (1080-ht)/2), text, fill='white', font=font)

        automated_text = "Automated post"
        atmt_post_text_bbox = draw.textbbox((0, 0), automated_text, font=font)
        wd = atmt_post_text_bbox[2] - atmt_post_text_bbox[0]
        ht = atmt_post_text_bbox[3] - atmt_post_text_bbox[1]
        font = ImageFont.truetype('fonts/Lora-Medium.ttf', 20)
        draw.text(((720-wd)*1.5, 1080-ht-30), automated_text, fill='white', font=font)

        notice_text = "NEW NOTIFICATION"
        notice_text_bbox = draw.textbbox((0, 0), notice_text, font=font)
        wd = notice_text_bbox[2] - notice_text_bbox[0]
        ht = notice_text_bbox[3] - notice_text_bbox[1]
        font = ImageFont.truetype('fonts/Lora-Medium.ttf', 40)
        draw.text(((720-wd+50)/4, 250), notice_text, fill='white', font=font)

        img.save('images/dumps/insta_dump.png')
        png_img = Image.open('images/dumps/insta_dump.png')
        png_img.convert("RGB").save('images/dumps/insta_dump.jpg')
        path = 'images/dumps/insta_dump.jpg'
        cl.photo_upload_to_story(path)

        # logger.info('story posted')


async def decode_captcha(img_path):
    pipeline = keras_ocr.pipeline.Pipeline()
    img = keras_ocr.tools.read(img_path)
    for text, box in pipeline.recognize([img])[0]:
        # print(text)
        # logger.info('captcha decoded')
    return text

async def login(browser):
    SLCM_USERNAME, SLCM_PASSWORD = setup_env()
    # browser = await launch({"headless": False, "args": ["--start-maximized"]})
    page = await browser.newPage()
    await page.goto('https://slcm.manipal.edu')
    await page.type('input[name="txtUserid"]', SLCM_USERNAME)
    await page.type('input[name="txtpassword"]', SLCM_PASSWORD)
    img = await page.querySelector('img[id="imgCaptcha"]')
    img_src = await page.evaluate('(img) => img.src', img)
    page2 = await browser.newPage()
    await page2.goto(img_src)
    # <img style="-webkit-user-select: none;" src="https://slcm.manipal.edu/GenerateCaptcha.aspx?638169415399257246">
    fin_img = await page2.querySelector('img')
    rel_path = '../images/captcha.png'
    abs_path = os.path.join(os.path.dirname(__file__), rel_path)
    await fin_img.screenshot({'path': abs_path})
    await page2.close()
    captcha = await decode_captcha(abs_path)
    await page.type('input[name="txtCaptcha"]', captcha)
    await page.click('input[name="btnLogin"]')
    #its working finally lets go 😭 fuck selenium, pypupetteeeeeer ftw
    return page

async def get_imp_docs(browser,page):
    page3 = await browser.newPage()
    await page3.goto('https://slcm.manipal.edu/ImportantDocuments.aspx')
    await page.close()
    # await page3.waitFor(1000)
    table = await page3.querySelector('table[id="ContentPlaceHolder1_grvDocument"]')
    rows = await table.querySelectorAll('td')
    a_tags = await table.querySelectorAll('a')
    # for some reason the below way feels like shit later on modify and improve this
    count = 0
    list_ = []
    for row in rows:
        if count % 2 == 0:
            count += 1
            continue
        # elif count > 6:
        #     break
        else: 
            rrow_content = await page3.evaluate('(element) => element.innerHTML', row)
            rrow_content = rrow_content.strip()
            while '<a' in rrow_content and '</a>' in rrow_content:
                rrow_content = rrow_content[:(rrow_content.index('<a'))] + rrow_content[(rrow_content.index('</a>'))+len('</a>')-1:]
            # print(rrow_content)
            # list.push(rrow_content)
            list_.append(rrow_content)
    for i in range(len(list_)-1, -1, -1):
        li = list_[i]
        if len(li) < 3 or '<td>></td>' in li or '<span>1</span>' in li:
            list_.pop(i)
        else:
            continue
    # print(list_)
    # print(len(list_)) #its 10 perfect
    # logger.info("important_documents list extracted")
    return list_,page3

def set_ones_or_zeroes_in_csv(list_,csv_file_path):
    new_list = [] #contains only the ones that are set to 1

    with open(csv_file_path, 'r') as f:
        csv_reader = csv.reader(f)
        csv_rows = list(csv_reader) 
    for li in list_:
        is_present = False 
        for row in csv_rows:
            if row[0] == li:  
                is_present = True
                row[1] = '0'  
                break

        if not is_present:
            new_list.append(li)
            csv_rows.append([li, '1']) # doing outside for loop on puprose to not repeat over and over again

    with open(csv_file_path, 'w', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerows(csv_rows)

    return new_list

async def main():
    # logging.basicConfig(
    #     level=logging.INFO,
    #     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    #     datefmt='%Y-%m-%d %H:%M:%S',
    #     filename='logs/logs.log'
    # )
    #print('starting main test')
    #browser = await launch({"headless": False, "args": ["--start-maximized"]})
    # browser = await launch()
    browser = await launch(headless=True)
    page = await login(browser)
    imp_docs,page = await get_imp_docs(browser,page)
    imp_docs_path = os.path.join(os.path.dirname(__file__), '../data/important-documents.csv')
    new_list = set_ones_or_zeroes_in_csv(imp_docs,imp_docs_path)
    # if any value in csv is set to 1 then it will be published in insta
    if len(new_list) > 0:
        post_story(new_list)
    # while True:
    #     #do nothing
    #     pass

loop = asyncio.get_event_loop()
loop.run_until_complete(main())