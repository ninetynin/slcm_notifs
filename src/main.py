import os
from dotenv import load_dotenv
import asyncio
from pyppeteer import launch
import keras_ocr

def setup_env():
    load_dotenv()
    SLCM_USERNAME = os.getenv("SLCM_USERNAME")
    SLCM_PASSWORD = os.getenv("SLCM_PASSWORD")
    return SLCM_USERNAME, SLCM_PASSWORD

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

async def main():
    browser = await launch({"headless": False, "args": ["--start-maximized"]})
    page = await login(browser)
    await get_imp_docs(browser,page)
    while True:
        #do nothing
        pass

loop = asyncio.get_event_loop()
loop.run_until_complete(main())