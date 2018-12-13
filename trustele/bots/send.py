# coding=utf-8
import os
import sys
import logging

import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from trustele.lib.localstorage import LocalStorage

SESSION_KEYS = ['user_auth', 'dc',
                'dc1_auth_key', 'dc1_server_salt',
                'dc4_auth_key', 'dc4_server_salt',
                'dc5_auth_key', 'dc5_server_salt']

logging.basicConfig(level=logging.INFO, filename='./trustele.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger('trustele.sender')

if getattr(sys, 'frozen', False):
    sep = ';' if sys.platform.startswith('win') else ':'
    os.environ['PATH'] += sep + sys._MEIPASS


class Sender(object):
    def __init__(self, my_id):
        self.browser = webdriver.Chrome()
        self.login_url = "https://web.telegram.org/#/login"
        self.req_url = "https://web.telegram.org/#/im"
        self.session_path = my_id + '.ss'

        self.browser.implicitly_wait(5)  # seconds
        log.info('sender initialized...')

    def open_browser(self):
        self.browser.get(self.login_url)

    def wait_for_login(self):
        wait = WebDriverWait(self.browser, timeout=120, poll_frequency=2)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'icon-hamburger-wrap')))

    def try_load_login_session(self):
        if os.path.exists(self.session_path):
            LocalStorage(self.browser).load(self.session_path)

    def record_login_session(self):
        LocalStorage(self.browser).save(self.session_path)

    def send_it(self, msg):
        text_area = self.browser.find_element_by_class_name('composer_rich_textarea')
        text_area.send_keys(msg)
        text_area.send_keys(Keys.ENTER)

    def launch(self, user_names, msg):
        try:
            log.info('openning browser...')
            self.open_browser()
            log.info('opened browser...')
            self.try_load_login_session()
            self.wait_for_login()
            log.info('login passed...')
            self.record_login_session()

            # trim and delete duplicated
            user_names = list(set([u.strip() for u in user_names]))

            counter = 0
            for p in user_names:
                self.browser.get(self.req_url + '?p=' + p)
                self.send_it(msg)
                counter += 1
                percent = 100 * counter / len(user_names)
                yield percent
        except Exception as e:
            log.error(str(e))


if __name__ == '__main__':
   sender = Sender('TrustChain')
   sender.launch('@blockchainaire', 'hello world')
