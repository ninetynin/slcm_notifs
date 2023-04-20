import asyncio
import logging
from playwright.async_api import async_playwright


class slcm_login:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    async def main(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logger = logging.getLogger(__name__)
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            await page.goto("https://slcm.manipal.edu")
            await page.click("text=Login")
            await page.fill("input[name=\"username\"]", self.username)
            await page.fill("input[name=\"password\"]", self.passwor