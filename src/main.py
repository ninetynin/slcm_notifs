import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://www.google.com")
        await page.screenshot(path="example.png")
        while True:
            await asyncio.sleep(1)

asyncio.run(main())