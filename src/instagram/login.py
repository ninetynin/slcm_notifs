import logging
from instagrapi import Client
from instagrapi.exceptions import LoginRequired


class InstagramClient:
    def __init__(self, username=None, password=None):
        self.logger = logging.getLogger()
        self.client = Client()
        # self.session = self.client.load_settings("session.json")
        self.session = None
        self.username = username
        self.password = password

    def login_user(self):
        login_via_session = False
        login_via_pw = False

        if self.session:
            try:
                self.session = self.client.load_settings("session.json")
                self.client.set_settings(self.session)
                self.client.login(self.username, self.password)

                try:
                    self.client.get_timeline_feed()
                except LoginRequired:
                    self.logger.info("Session is invalid, need to login via username and password")

                    old_session = self.client.get_settings()

                    # use the same device uuids across logins
                    self.client.set_settings({})
                    self.client.set_uuids(old_session["uuids"])

                    self.client.login(self.username, self.password)
                login_via_session = True
            except Exception as e:
                self.logger.info("Couldn't login user using session information: %s" % e)

        if not login_via_session:
            try:
                self.logger.info("Attempting to login via username and password. username: %s" % self.username)
                if self.client.login(self.username, self.password):
                    login_via_pw = True
            except Exception as e:
                self.logger.info("Couldn't login user using username and password: %s" % e)

        if not login_via_pw and not login_via_session:
            raise Exception("Couldn't login user with either password or session")

        return self.client
