# import asyncio
# from pyppeteer import launch
# # from instagrapi import Client 

# print("entered into script")

# async def main():
#     print("entered main fn")
#     # browser = await launch(headless=False)
#     browser = await launch()
#     print("browser launched")
#     # page = await browser.newPage()
#     # print("new page created")
#     # await page.goto('https://slcm.manipal.edu')
#     # print("page loaded")
#     # print(await page.title())
#     # print("page title printed")
#     # await browser.close()
#     # print("browser closed")
#     context = await browser.


# asyncio.get_event_loop().run_until_complete(main())

import asyncio
from pyppeteer import launch

async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('http://example.com')
    await page.screenshot({'path': 'example.png'})

    dimensions = await page.evaluate('''() => {
        return {
            width: document.documentElement.clientWidth,
            height: document.documentElement.clientHeight,
            deviceScaleFactor: window.devicePixelRatio,
        }
    }''')

    print(dimensions)
    # >>> {'width': 800, 'height': 600, 'deviceScaleFactor': 1}
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())