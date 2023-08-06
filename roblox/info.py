from . import constants
from models import RobloxAccount

import undetected_chromedriver as uc


class RobloxInfo:
    def __init__(self, driver: uc.Chrome, account: RobloxAccount):
        self.driver = driver
        self.account = account

    def get_robux(self) -> RobloxAccount:
        result = self.driver.execute_script(f"""
        {constants.SCRIPT}
        return await info.getRobux()
        """)

        self.account.robux = int(result)

        return self.account

    def get_messages(self) -> str:
        result = self.driver.execute_script(f"""
        {constants.SCRIPT}
        return await info.getMessages()
        """)

        return result
    
    def agreeRoblox(self) -> str:
        result = self.driver.execute_script(f"""
        {constants.SCRIPT}
        return await info.agreeRoblox()
        """)

        return result

    def changePassword(self, oldPassword: str, newPassword: str) -> str:
        result = self.driver.execute_script(f"""
        {constants.SCRIPT}
        return await info.changePassword('{oldPassword}', '{newPassword}')
        """)

        return result