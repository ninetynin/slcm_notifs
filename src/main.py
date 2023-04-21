import asyncio
import logging
from scraper.slcm_login import slcm_login
from scraper.extract import extract
import os
from dotenv import load_dotenv
from playwright.async_api import async_playwright

def setup_env(env_fn):
    SLCM_USERNAME = os.getenv("SLCM_USERNAME")
    SLCM_PASSWORD = os.getenv("SLCM_PASSWORD")
    if SLCM_USERNAME == None or SLCM_PASSWORD == None:
        print("One or more env variables are not set")
        exit(1)
    return SLCM_USERNAME, SLCM_PASSWORD

def setup_insta_env(env_fn):
    INSTA_USERNAME = os.getenv("INSTAGRAM_USERNAME")
    INSTA_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")
    if INSTA_USERNAME == None or INSTA_PASSWORD == None:
        print("One or more env variables are not set")
        exit(1)
    return INSTA_USERNAME, INSTA_PASSWORD

async def main():
    env_fn = load_dotenv()
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename='logs/logs.log'
    )
    logger = logging.getLogger(__name__)
    SLCM_USERNAME, SLCM_PASSWORD = setup_env(env_fn)
    INSTA_USERNAME, INSTA_PASSWORD = setup_insta_env(env_fn)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        context = await slcm_login(SLCM_USERNAME, SLCM_PASSWORD, context, logger).login()
        context = await extract(context, logger).imp_docs_extract()

if __name__ == '__main__':
    # asyncio.run(main())
    asyncio.get_event_loop().run_until_complete(main())