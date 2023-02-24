# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 12:13:36 2022

@author: User
"""

from selenium import webdriver
import sqlite3
from selenium.webdriver.chrome.options import Options
import time
import ast
import random
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
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    # driver.set_window_position(-2000, 0)  # запуск окна браузера за пределами экрана
    return driver


def main():
    # подключаемся к базе данных и получаем случайный id записей
    con = sqlite3.connect('accounts.db')
    sql = 'select id from account'
    with con:
        list_of_id = con.execute(sql).fetchall()
    x = random.randint(0, len(list_of_id) - 1)
    i = list_of_id[x][0]
    sql = 'select mail, password, user_agent, cookies from account where id = ?'
    with con:
        record = con.execute(sql, (i,)).fetchall()
    # получаем данные случайно выбранного аккаунта Instagram для входа (mail, password, user-agent, cookies)
    mail, password, ua, cookies = record[0][0], record[0][1], record[0][2], record[0][3]
    # создаем экземпляр класса Webdriver
    driver = settings(ua, use_proxy=False)
    cookies = ast.literal_eval(cookies[1:-1])
    # создаем экземпляр класса Account
    account = Account(driver)
    # если авторизация успешна
    if account.auth(mail, password, cookies):
        count = 0
        # определяем количество аккаунтов, на которое планируем подписаться
        while count < 2:
            # проверяем, что взятый в базе данных nickname не является нашим nickname
            x = random.randint(0, len(list_of_id) - 1)
            j = list_of_id[x][0]
            if i != j:
                sql = 'select nickname from account where id = ?'
                with con:
                    nickname = con.execute(sql, (j,)).fetchall()[0][0]
                # подписываемся на nickname
                if account.follow_friend(nickname):
                    # увеличиваем счетчик
                    count += 1
                else:
                    # в случае неудачного подписания проверяем не заблокирован ли наш аккаунт в процессе работы скрипта
                    if account.check_ban():
                        driver.quit()
            time.sleep(1)
    # проверяем не заблокирован ли наш аккаунт в случае неудачной авторизации
    else:
        account.check_ban()

    print('Процесс подписания завершен')
    driver.quit()


if __name__ == '__main__':
    main()