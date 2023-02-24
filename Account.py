# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 12:13:36 2022

@author: User
"""


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


class Account:
    def __init__(self, driver):
        self.driver = driver

    def auth(self, login: str, password: str, cookies: tuple) -> bool:
        try:
            if cookies:
                self.driver.get('https://instagram.com')
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
                self.driver.get('https://www.instagram.com/accounts/edit/')
                WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, '_ab6-')))
                print(f'\033[0;92mВход в {login} выполнен через cookie\033[00m')
                return True
        except:
            pass
        try:
            if login and password:
                WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.NAME, 'username'))).send_keys(login)
                WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.NAME, 'password'))).send_keys(password)
                time.sleep(2)
                WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.NAME, 'password'))).send_keys(
                    Keys.ENTER)
                time.sleep(3)
                self.driver.get('https://www.instagram.com/accounts/edit/')
                WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, '_ab6-')))
                print(f'\033[0;92mВход в {login} выполнен через ввод пароля\033[00m')
                return True
        except:
            pass
        print('')
        print(f'\033[1;31mВход в аккаунт {login} не выполнен\033[00m')
        return False

    def follow_friend(self, nickname: str) -> bool:
        try:
            self.driver.get(f'https://instagram.com/{nickname}')
            button = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.CLASS_NAME, '_aacl._aaco._aacw._aad6._aade')))
            if button.text == 'Follow' or button.text == 'Follow Back':
                button.click()
            if button.text == 'Following':
                print(f'Аккаунт уже подписан на {nickname}')
            return True
        except Exception as e:
            print('')
            print(f'\033[1;31mНеудачное подписание на {nickname}\033[00m')
            print(e)
            return False

    def check_ban(self):
        try:
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'x1swlcf7.xh8yej3.xixxii4')))
            print(f'\033[1;31mАккаунт заблокирован\033[00m')
            return True
        except:
            print('')
            print(f'\033[0;92mПризнак блокировки аккаунта не обнаружен\033[00m')
            return False

    def create_post(self, path_to_file: str):
        try:
            time.sleep(2)
            menu = WebDriverWait(self.driver, 10).until(lambda d: d.find_elements(By.CLASS_NAME, "_ab6-"))
            for item in menu:
                if item.get_attribute('aria-label') == "New post":
                    item.click()
            time.sleep(5)
            items = self.driver.find_elements(By.CLASS_NAME, '_ac69')
            for i in range(len(items)):
                if items[i].get_attribute(
                        'accept') == "image/jpeg,image/png,image/heic,image/heif,video/mp4,video/quicktime":
                    items[i].send_keys(path_to_file)
            time.sleep(2)
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, '_ac7b._ac7d'))).click()
            time.sleep(2)
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, '_ac7b._ac7d'))).click()
            time.sleep(2)
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, '_ac7b._ac7d'))).click()
            time.sleep(2)
            start = time.time()
            while (time.time()-start < 20):
                text = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, '_ac7a'))).text
                if text == 'Post shared':
                    break
                else:
                    time.sleep(2)
            print('\033[0;92mМедиафайл загружен\033[00m')
            return True
        except Exception as e:
            print('')
            print(f'\033[1;31mНеудачная загрузка медиафайла\033[00m')
            print(e)
            return False

    def add_profile_photo(self, path_to_file: str) -> bool:
        try:
            self.driver.get('https://www.instagram.com/accounts/edit/')
            time.sleep(2)
            self.driver.find_elements(By.CLASS_NAME, '_ac69')[1].send_keys(path_to_file)
            time.sleep(2)
            start = time.time()
            while (time.time()-start < 20):
                try:
                    text = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, '_abmp'))).text
                    if text == 'Profile photo added.':
                        break
                    else:
                        time.sleep(2)
                except:
                    pass
            print(f'\033[0;92mУспешная загрузка аватара\033[00m')
            return True
        except Exception as e:
            print('')
            print(f'\033[1;31mНеудачная загрузка аватара\033[00m')
            print(e)
            return False

    def like_photos_home_page(self, number_of_photos: int) -> bool:
        try:
            self.driver.get('https://www.instagram.com')
            WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.CLASS_NAME, '_a9--._a9_0'))).click()
            i = 0
            while i < number_of_photos:
                likes = WebDriverWait(self.driver, 10).until(lambda d: d.find_elements(By.CLASS_NAME, "_aamw"))
                for like in likes:
                    if like.find_element(By.CLASS_NAME, '_ab6-').get_attribute('aria-label') == 'Like':
                        like.click()
                        i += 1
                    self.driver.execute_script("window.scrollBy(0,500)", "")
                    time.sleep(2)
            print(f'\033[0;92mУспешный лайк фото\033[00m')
        except Exception as e:
            print('')
            print(f'\033[1;31mНеудачный лайк {i} фото\033[00m')
            print(e)
            return False

    def like_all_photos_of_nickname(self, nickname: str) -> bool:
        try:
            self.driver.get(f'https://instagram.com/{nickname}')
            pictures = WebDriverWait(self.driver, 10).until(lambda d: d.find_elements(By.CLASS_NAME, "_aagu"))
            for picture in pictures:
                picture.click()
                if WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, '_aamw'))).find_element(By.CLASS_NAME, '_ab6-').get_attribute('aria-label') == 'Like':
                    WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, '_aamw'))).click()
                WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'x10l6tqk.x160vmok.x1eu8d0j.x1vjfegm'))).click()
                time.sleep(1)
            print(f'\033[0;92mУдачный лайк фото для {nickname}\033[00m')
            return True
        except Exception as e:
            print('')
            print(f'\033[1;31mНеудачный лайк фото для {nickname}\033[00m')
            print(e)
            return False

    def edit_profile(self, Name=None, Username=None, Bio=None, Email=None, Phone_number=None):
        try:
            self.driver.get('https://www.instagram.com/accounts/edit/')
            if Name:
                WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, 'pepName'))).send_keys(Name)
            if Username:
                WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, 'pepUsername'))).send_keys(Username)
            if Bio:
                WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, 'pepBio'))).send_keys(Bio)
            if Email:
                WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, 'pepEmail'))).send_keys(Email)
            if Phone_number:
                WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, 'pepPhone Number'))).send_keys(Phone_number)
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, '_acan._acap._acas._aj1-'))).click()
            print(f'\033[0;92mУдачное изменение данных\033[00m')
            return True
        except Exception as e:
            print('')
            print(f'\033[1;31mНеудачное изменение данных\033[00m')
            print(e)
            return False

    def get_information_about_nickname(self, nickname: str) -> dict:
        try:
            self.driver.get(f'https://instagram.com/{nickname}')
            dictionary = {}
            items = WebDriverWait(self.driver, 10).until(lambda d: d.find_elements(By.CLASS_NAME, "_ac2a"))
            dictionary['posts'] = items[0].text
            dictionary['followers'] = items[1].text
            dictionary['following'] = items[2].text
            inf = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, '_aa_c')))
            for item in ['span', 'div', 'h1', 'a']:
                try:
                    dictionary[item] = inf.find_element(By.TAG_NAME, item).text.replace('\n', ' ')
                except:
                    pass
            return dictionary
        except Exception as e:
            print('')
            print(f'Получение информации для {nickname} не выполнено')
            print(e)

    def get_cookies(self) -> tuple:
        return tuple(self.driver.get_cookies())

    def get_user_agent(self) -> str:
        return self.driver.execute_script("return navigator.userAgent;")
