import asyncio
import logging
from playwright.async_api import async_playwright

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def main():
    logger.info('Entered main function')
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch()
            logger.info('Browser launched')
            page = await browser.new_page()
            logger.info('New page created')
            await page.goto("https://www.google.com")
            logger.info(f'Page title: {await page.title()}')
            await browser.close()
            logger.info('Browser closed')
        except Exception as e:
            logger.error(f'Error occurred: {e}')
            await browser.close()
            logger.info('Browser closed')

if __name__ == '__main__':
    asyncio.run(main())
