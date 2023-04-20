#important things to deal

#1. delay between each request
#2. fix and use session.json everytime

import logging
from instagrapi import Client

logger = logging.getLogger()

class InstagramBot:
    def __init__(self, username, password, session_file=None):
        self.username = username
        self.password = password
        self.session_file = session_file
        self.client = Client()

    def login(self):
        if self.session_file:
            session = self.client.load_settings(self.session_file)
            if session:
                try:
                    self.client.set_settings(session)
                    self.client.login(self.username, self.password)
                    try:
                        self.client.get_timeline_feed()
                        logger.info("Session is valid, no need to login")
                    except LoginRequired:
                        logger.info("Session is invalid, need to login via username and password")
                        old_session = self.client.get_settings()
                        self.client.set_settings({})
                        self.client.set_uuids(old_session["uuids"])
                        self.client.login(self.username, self.password)
                    return True
                except Exception as e:
                    logger.info("Couldn't login user using session information: %s" % e)
        try:
            logger.info("Attempting to login via username and password. username: %s" % self.username)
            if self.client.login(self.username, self.password):
                return True
        except Exception as e:
            logger.info("Couldn't login user using username and password: %s" % e)
        raise Exception("Couldn't login user with either password or session")