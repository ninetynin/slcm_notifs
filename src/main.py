import asyncio
from pyppeteer import launch
# from instagrapi import Client 

print("entered into script")

async def main():
    print("entered main fn")
    browser = await launch()
    print("browser launched")

    try:
        print("entered try block")
        page = await browser.newPage()
        print("new page created")
        await page.goto('https://slcm.manipal.edu')
        print("page loaded")
        print(await page.title())
        print("page title printed")
        await page.waitForSelector('input[name="txtUserName"]', timeout=40000)
    except Exception as e:
        print(e)
        await browser.close()
        print("browser closed")

asyncio.get_event_loop().run_until_complete(main())
