import os
from dotenv import load_dotenv
import asyncio
from pyppeteer import launch

def setup_env():
    load_dotenv()
    SLCM_USERNAME = os.getenv("SLCM_USERNAME")
    SLCM_PASSWORD = os.getenv("SLCM_PASSWORD")
    return SLCM_USERNAME, SLCM_PASSWORD

async def login():
    SLCM_USERNAME, SLCM_PASSWORD = setup_env()
    browser = await launch(headless=False)  # Set headless=False to display browser window
    page = await browser.newPage()
    await page.goto('https://slcm.manipal.edu')
    await page.type('input[name="txtUserid"]', SLCM_USERNAME)
    await page.type('input[name="txtpassword"]', SLCM_PASSWORD)
    img = await page.querySelector('img[id="imgCaptcha"]')
    img_src = await page.evaluate('(img) => img.src', img)
    page = await browser.newPage()
    await page.goto(img_src)
    # <img style="-webkit-user-select: none;" src="https://slcm.manipal.edu/GenerateCaptcha.aspx?638169415399257246">
    # there is no class or image id just go to the img element and store it in a variable
    fin_img = await page.querySelector('img')
    # save the image
    await fin_img.screenshot({'path': 'captcha.png'})
    while True:
        #do nothing
        pass

async def main():
    await login()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())