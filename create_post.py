# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 12:13:36 2022

@author: User
"""

from selenium import webdriver
import sqlite3
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
import ast
import os
import random
from Account import Account
from proxy import create_proxy_file
import chromedriver_binary


# устанавливаем настройки driver
def settings(ua, use_proxy=False):
    options = Options()
    # options.add_argument("--incognito")  # режим ИНКОГНИТО
    options.add_argument('--disable-blink-features=AutomationControlled')  # скрываем использование webdriver
    options.add_argument(f'user-agent={ua}')  # user-agent
    options.add_argument('--lang=en')  # устанавливаем язык браузера
    # если используем прокси settings(use_proxy=True)
    if use_proxy:
        create_proxy_file()
        options.add_extension('proxy_auth_plugin.zip')  # используем прокси (расширение не работает в режиме ИНКОГНИТО)
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    # driver.set_window_position(-2000, 0)  # запуск окна браузера за пределами экрана
    return driver


def main():
    con = sqlite3.connect('accounts.db')
    sql = 'select id from account'
    with con:
        list_of_id = con.execute(sql).fetchall()
    x = random.randint(0, len(list_of_id)-1)
    i = list_of_id[x][0]
    sql = 'select mail, password, user_agent, cookies, nickname from account where id = ?'
    with con:
        record = con.execute(sql, (i,)).fetchall()
    mail, password, ua, cookies, nickname = record[0][0], record[0][1], record[0][2], record[0][3], record[0][4]
    driver = settings(ua, use_proxy=False)
    cookies = ast.literal_eval(cookies[1:-1])
    account = Account(driver)
    if account.auth(mail, password, cookies):
        path_to_file = 'add absolute path here'
        account.create_post(path_to_file)
        os.remove(path_to_file)
    else:
        account.check_ban()
    driver.quit()


if __name__ == '__main__':
    main()
