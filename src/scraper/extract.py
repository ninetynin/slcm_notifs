import asyncio
import logging
from playwright.async_api import async_playwright
import os

# class extract:
#     def __init__(self, page, context, logger):
#         self.page = page
#         self.logger = logger
#         self.context = context

#     async def extract(self):
#         await extract_imp_docs(self.page, self.context, self.logger).extract()

class extract:
    def __init__(self, context, logger):
        # self.page = page
        self.logger = logger
        self.context = context
        self.loop = asyncio.get_event_loop()

    async def imp_docs_extract(self):
        page = await self.context.new_page()
        self.logger.info("New page opened")
        await page.goto("https://slcm.manipal.edu/ImportantDocuments.aspx")
        self.logger.info("Navigated to Important Documents page")
        # table = await page.query_selector("table#ctl00_ContentPlaceHolder1_GridView1")
        # table = page.locator("#ContentPlaceHolder1_grvDocuments")
        table = page.get_by_role("table")
        # # table2 = await page.query_selector("table#ContentPlaceHolder1_grvDocument")
        # print(await table.get_attribute('innerHTML'))
        # print(await table2.get_attribute('innerHTML'))
        rows = await table.query_selector_all("tr")
        for row in rows:
            print(row.get_attribute('innerHTML'))
        while True:
            pass