import asyncio
from pyppeteer import launch
# from instagrapi import Client 

async def main():
    # browser = await launch(headless=False)
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://slcm.manipal.edu')
    print(await page.title())
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())