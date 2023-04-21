import asyncio
import logging
from playwright.async_api import async_playwright, expect, Playwright
import os
import csv

#work on event calender later on

class extract:
    def __init__(self, context, logger):
        # self.page = page
        self.logger = logger
        self.context = context
        self.loop = asyncio.get_event_loop()

    def set_ones_and_zeroes_csv(self,lisy,path):
        new_list = [] #only for new entries i.e., value is 1

        with open(path, 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)

        for i in range(len(lisy)):
            is_present = False
            # count = 0
            for row in rows:
                # if count == 0:
                #     count += 1
                #     continue
                if row[0] == lisy[i]:
                    is_present = True
                    row[1] = '0'
                    break
            if not is_present:
                new_list.append(lisy[i])
                rows.append([lisy[i], '1'])

        with open(path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        return new_list

    async def imp_docs_extract(self):
        page = await self.context.new_page()
        await page.goto("https://slcm.manipal.edu/ImportantDocuments.aspx")
        self.logger.info("Navigated to Important Documents page")
        cells = await page.get_by_role("cell").all()
        # count = 0
        lisy = []
        for cell in cells:
            # count += 1
            text = await cell.text_content()
            #//todo there's a heavy chance this might break use some better method later on its not imp right now
            text = text.strip()
            if text != "":
                lisy.append(text)
        lisy = lisy[:20] #dont try inside loop
        self.logger.info(lisy)
        self.logger.info("Extracted all important documents")
        # for i in range(0, len(lisy), 2):
        #     print(lisy[i], lisy[i+1])
        # ---------👇 download link code not working if there is time later on try to use evaluate and upload the link
        # on a pdf viewer temp site and then get the url and store it instead of downloading it
        # and using it using github viewer 👍 ---------------
        # download_path = '../../downloads/'
        # abs_path = os.path.abspath(download_path)
        # for i in range(0, len(lisy), 2):
        #     async with page.expect_download() as download_info:
        #         await page.get_by_role("row",name=lisy[i+1]).get_by_role("link", name="").click() #same unsecure method for temp
        #         self.logger.info(f"Downloading {lisy[i]}")
        #     download = await download_info.value
        #     self.logger.info(f"Downloaded {lisy[i]},{download.path}")
        #     # await download.save_as(os.path.join(abs_path, lisy[i]))
        #     await download.save_as(download_path+'{}'.format(lisy[i]))
        #     self.logger.info(f"saved {lisy[i]}")
        return self.context,lisy

    async def uploded_docs_extract(self):
        page = await self.context.new_page()
        await page.goto("https://slcm.manipal.edu/DocumentDownload.aspx")
        self.logger.info("Navigated to Uploaded Documents page")
        cells = await page.get_by_role("cell").all()
        lisy = []
        for cell in cells:
            text = await cell.text_content()
            text = text.strip()
            if text != "":
                lisy.append(text)
        lisy = lisy[:30]
        self.logger.info(lisy)
        self.logger.info("Extracted all uploaded documents")
        return self.context,lisy