import asyncio
import logging
from playwright.async_api import async_playwright
from scraper.slcm_login import slcm_login

async def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    slcm_login()

if __name__ == '__main__':
    asyncio.run(main())
