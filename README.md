<strong>С использованием методов класса Account из Account.py реализован API управления аккаунтом Instagram</strong>

API может быть использован для фарминга аккаунтов или автоматизированного управления рутинными операциями для своего аккаунта.

В настоящей реализации содержатся методы, позволяющие осуществлять авторизацию в аккаунте, проверку аккаунта на бан, подписание на аккаунт, 
создание поста, добавление аватара, лайк фото в ленте, лайк всех фото аккаунта, правку профайла, получение информации об аккаунте, получение
cookie браузера (например, для дальнейшей авторизации в аккаунте по cookie), получение user-agent браузера.

Ниже представлен пример использования скрипта для авторизации в аккаунте и подписания на другие аккаунты. Вся информация об аккаунтах содержится в импровизированной 
базе данных sqlite (accounts.db). Аккаунты в базе данных выбираются случайным образом. 

<strong>Конфигурирование и использование</strong>

Скачайте браузер [Chrome](https://www.google.com/intl/en/chrome/), если он еще не установлен
```ruby
$ git clone https://github.com/SofronovRoman/IG_accounts_farmer.git
$ cd IG_accounts_farmer
$ python3 -m pip install -r requirements.txt
$ python3 follow_friend.py
```

Если планируется использовать прокси-сервер, то измените параметры прокси-сервера в файле proxy.py и параметр в follow_friend.py на 
driver = settings(ua, use_proxy=True)

Если версия Chromedriver не совпадает с версией используемого браузера Chrome, задайте требуемую версию Chromedriver в файле requirements.txt

В текущей реализации для примера также содержатся скрипты добавления аватара (add_profile_photo.py) и создания поста(create_post.py).
