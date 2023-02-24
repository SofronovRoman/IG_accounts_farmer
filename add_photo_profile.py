from selenium import webdriver
import sqlite3
from selenium.webdriver.chrome.options import Options
import time
import ast
import os
from Account import Account
from proxy import create_proxy_file
import chromedriver_binary


# устанавливаем настройки driver
def settings(ua, use_proxy=False):
    options = Options()
    options.add_argument('--disable-blink-features=AutomationControlled')  # скрываем использование webdriver
    options.add_argument(f'user-agent={ua}')  # user-agent
    options.add_argument('--lang=en')  # устанавливаем язык браузера
    # если используем прокси settings(use_proxy=True)
    if use_proxy:
        create_proxy_file()
        options.add_extension('proxy_auth_plugin.zip')  # используем прокси (расширение не работает в режиме ИНКОГНИТО)
    options.add_argument("--disable-application-cache")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    # driver.set_window_position(-2000, 0)   # запуск окна браузера за пределами экрана
    return driver


def main():
    con = sqlite3.connect('accounts.db')
    sql = """select mail, password, user_agent, cookies from account where avatar = 0"""
    with con:
        records = con.execute(sql).fetchall()
    for record in records:
        mail, password, ua, cookies = record[0], record[1], record[2], record[3]
        driver = settings(ua, use_proxy=False)
        cookies = ast.literal_eval(cookies[1:-1])
        account = Account(driver)
        if account.auth(mail, password, cookies):
            path_to_file = 'add absolute path here'
            account.add_profile_photo(path_to_file)
            os.remove(path_to_file)
            last_enter_date = time.strftime("%d-%m-%Y")
            sql = f'Update account set last_enter_date = "{last_enter_date}", avatar = 1 where mail = "{mail}"'
            with con:
                con.execute(sql)
        else:
            account.check_ban()
        driver.quit()


if '__name__' == '__main__':
    main()