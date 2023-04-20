import asyncio
import logging
from pyppeteer import launch

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def main():
    logger.info('Entered main function')
    try:
        logger.info('Launching browser...')
        browser = await launch()
        logger.info('Browser launched')
        page = await browser.newPage()
        logger.info('New page created')
        await page.goto('https://slcm.manipal.edu')
        logger.info('Page loaded')
        logger.info(f'Page title: {await page.title()}')
        await browser.close()
        logger.info('Browser closed')
        await page.waitForSelector('input[name="txtUserName"]', timeout=40000)
    except Exception as e:
        logger.error(f'Error occurred: {e}')
        await browser.close()
        logger.info('Browser closed')

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
