import asyncio
import logging
from playwright.async_api import async_playwright
import os
import keras_ocr

class slcm_login:
    def __init__(self, username, password, context, logger):
        self.username = username
        self.password = password
        self.context = context
        self.logger = logger
        # self.loop = asyncio.get_event_loop()

    async def decode_captcha(self, img_path):
        pipeline = keras_ocr.pipeline.Pipeline()
        img = keras_ocr.tools.read(img_path)
        for text, box in pipeline.recognize([img])[0]:
            # print(text)
            self.logger.info('captcha decoded')
        self.logger.info(text)
        return text

    async def login(self):
        self.logger.info("Browser launched")
        page = await self.context.new_page()
        self.logger.info("New page opened")
        await page.goto("https://slcm.manipal.edu")  
        img_url = await page.locator('#imgCaptcha').get_attribute('src')
        self.logger.info("Captcha url: " + img_url)
        img_url = 'https://slcm.manipal.edu/' + img_url
        img_tab = await self.context.new_page()
        await img_tab.goto(img_url)
        abs_path = os.path.join(os.path.dirname(__file__), '../../images/captcha.png')
        await img_tab.get_by_role('img').screenshot(path=abs_path)
        self.logger.info("Captcha saved")
        await img_tab.close()
        captcha = await self.decode_captcha(abs_path)
        await page.locator('#txtUserid').type(self.username)
        await page.locator('#txtpassword').type(self.password)
        await page.locator('#txtCaptcha').type(captcha)
        # await page.get_by_role("btnLogin").click()
        await page.click('#btnLogin')
        self.logger.info("Login button clicked")
        # while True:
        #     pass
        return self.context,page

    # async def main(self):
    #     return await self.login()