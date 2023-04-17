import asyncio
from pyppeteer import launch
# from instagrapi import Client 

print("entered into script")

async def main():
    print("entered main fn")
    # browser = await launch(headless=False)
    browser = await launch()
    print("browser launched")
    # page = await browser.newPage()
    # print("new page created")
    # await page.goto('https://slcm.manipal.edu')
    # print("page loaded")
    # print(await page.title())
    # print("page title printed")
    # await browser.close()
    # print("browser closed")

    try:
        page = await browser.newPage()
        print("new page created")
        await page.goto('https://slcm.manipal.edu')
        print("page loaded")
        print(await page.title())
        print("page title printed")
        await browser.close()
        print("browser closed")
        await page.waitForSelector('input[name="txtUserName"]', timeout=40000)
    except Exception as e:
        print(e)
        await browser.close()
        print("browser closed")

asyncio.get_event_loop().run_until_complete(main())
