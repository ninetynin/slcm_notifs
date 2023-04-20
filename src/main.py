import asyncio
import logging
from scraper.slcm_login import slcm_login
import os
from dotenv import load_dotenv

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
    logger.info("Starting main.py")
    SLCM_USERNAME, SLCM_PASSWORD = setup_env(env_fn)
    INSTA_USERNAME, INSTA_PASSWORD = setup_insta_env(env_fn)
    logger.info("Setting up slcm_login")
    slcm = await slcm_login(SLCM_USERNAME, SLCM_PASSWORD, logger).main()

if __name__ == '__main__':
    asyncio.run(main())