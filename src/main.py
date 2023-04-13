import os
from dotenv import load_dotenv
import asyncio
from pyppeteer import launch
import keras_ocr
import csv
from instagrapi import Client # there's a heavy chance this might be broken in future then find a alternative
from PIL import Image, ImageDraw, ImageFont, ImageColor


load_dotenv()

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
    cl.login(INSTA_USERNAME, INSTA_PASSWORD)
    return cl

def post_story(new_list):
    # bg_path = '../images/insta_bg_template.png'
    # abs_bg_path = os.path.join(os.path.dirname(__file__), bg_path)
    cl = login_insta()
    print('logged in')
    for li in new_list:
        img = Image.new(mode="RGBA", size=(720, 1280), color=(25, 25, 25, 1))
        draw = ImageDraw.Draw(img)
        img.save('images/dumps/insta_dump.png')
        # li_width, li_height = draw.textsize(li)
        # draw.text(((720-li_width)/2, (1280-li_height)/2), li, fill="#ffffff")
        draw.text((500,500),li,fill='white')
        img.save('images/dumps/insta_dump.png')
        # cl.photo_upload_to_story('/app/image.jpg')
        cl.photo_upload_to_story('images/dumps/insta_dump.png')
        print('set :' + li)

async def decode_captcha(img_path):
    pipeline = keras_ocr.pipeline.Pipeline()
    img = keras_ocr.tools.read(img_path)
    for text, box in pipeline.recognize([img])[0]:
        # print(text, box)
        print(text)
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
    print(list_)
    print(len(list_)) #its 10 perfect
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
    #print('starting main test')
    #browser = await launch({"headless": False, "args": ["--start-maximized"]})
    browser = await launch()
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