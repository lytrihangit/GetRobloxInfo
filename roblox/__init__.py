from typing import Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .exceptions import InvalidAccount, AnUnknownError, BannedAccount, CookieNotFound, CaptchaTimeout
from models import RobloxAccount

import undetected_chromedriver as uc
import time
import random as rand


class Roblox:
    TIMEOUT = 120

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.states = {
            'Incorrect username or password': InvalidAccount,
            'An unknown error occurred': AnUnknownError,
            'Banned': BannedAccount
        }
        self.solve_time = 60

        self._options = uc.ChromeOptions()
        self._driver: Optional[uc.Chrome] = None

    @property
    def options(self) -> uc.ChromeOptions:
        return self._options

    @property
    def driver(self) -> uc.Chrome:
        if self._driver:
            return self._driver

        self._driver = uc.Chrome(user_multi_procs=True, options=self.options)

        return self._driver

    def close(self) -> None:
        self.driver.quit()
        self._driver = None

    def throw_if_cancellation_requested(self) -> None:
        for state in self.states.keys():
            if state in self.driver.page_source:
                raise self.states[state]

            time.sleep(.5)

    def login(self) -> RobloxAccount:
        self.driver.get('https://www.roblox.com/Login')
        # time.sleep(1)

        # WebDriverWait(self.driver, self.TIMEOUT).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, 'a[id="main-login-button"]'))
        # ).click()
        # time.sleep(rand.uniform(1, 2.5))

        username_input = WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[id="login-username"]'))
        )
        username_input.send_keys(self.username)
        time.sleep(rand.uniform(.5, 1))

        password_input = self.driver.find_element(By.CSS_SELECTOR, 'input[id="login-password"]')
        password_input.send_keys(self.password)
        time.sleep(rand.uniform(.5, 1))

        login_button = WebDriverWait(self.driver, rand.randint(3, 5)).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[id="login-button"]'))
        )
        login_button.click()

        while 'home' not in self.driver.current_url:
            self.throw_if_cancellation_requested()

            captcha_frame = self.driver.find_elements(By.CSS_SELECTOR, 'iframe[id="arkose-iframe"]')
            if not captcha_frame:
                time.sleep(.5)
                continue

            end_time = time.time() + self.solve_time
            while 'home' not in self.driver.current_url:
                self.throw_if_cancellation_requested()
                if time.time() > end_time:
                    raise CaptchaTimeout
                time.sleep(.5)

        security_cookie = None
        cookie_search_time = time.time() + 30
        while not security_cookie:
            security_cookie = self.driver.get_cookie('.ROBLOSECURITY')
            if time.time() > cookie_search_time:
                break
            time.sleep(.5)

        if not security_cookie:
            raise CookieNotFound

        security_cookie = security_cookie['value']
        account = RobloxAccount(self.username, self.password, security_cookie, 0)

        return account
