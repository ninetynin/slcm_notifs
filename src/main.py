import asyncio
import logging
from scraper.slcm_login import slcm_login
from scraper.extract import extract
from instagram.login import InstagramClient
from instagram.story import PostStory
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

async def main() -> None:
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
    i_list,u_list = [],[]
    async with async_playwright() as p:
        # browser = await p.chromium.launch(headless=False)
        browser = await p.chromium.launch()
        context = await browser.new_context()
        context = await slcm_login(SLCM_USERNAME, SLCM_PASSWORD, context, logger).login()
        context, i_list = await extract(context, logger).imp_docs_extract()
        context, u_list = await extract(context, logger).uploded_docs_extract()
        await context.close()
        await browser.close()
        logger.info("Browser closed & context closed, scraping complete")
    i_list = i_list[1::2]
    logger.info("i_list: " + str(i_list))
    u_list = u_list[1::3]
    logger.info("u_list: " + str(u_list))
    i_path = os.path.join(os.path.dirname(__file__), '../data/important-documents.csv')
    new_only_i_list = extract(context, logger).set_ones_and_zeroes_csv(i_list, i_path)
    u_path = os.path.join(os.path.dirname(__file__), '../data/uploaded-documents.csv')
    new_only_u_list = extract(context, logger).set_ones_and_zeroes_csv(u_list, u_path)
    logger.info("successfully updated csv files") #40sec local exec time -> if inst + assume 2min then max 3/2 times per day

    Inst_Client = InstagramClient(INSTA_USERNAME, INSTA_PASSWORD).login_user()
    logger.info("successfully logged in to instagram")
    Inst_Client = PostStory(Inst_Client, logger).post_story(new_only_i_list)
    Inst_Client = PostStory(Inst_Client, logger).post_story(new_only_u_list)
    logger.info("successfully posted stories to instagram")

    logger.info("exiting")
    exit(0)


if __name__ == '__main__':
    # asyncio.run(main())
    asyncio.get_event_loop().run_until_complete(main())