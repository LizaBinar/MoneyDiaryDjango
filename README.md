<p align="center">
    <img src="https://i.ibb.co/BsSYhcT/QI4r-e-Tyd4-I.jpg">
</p>

<p align="center">
    <img src="https://img.shields.io/badge/Python-3.10.6-yellowgreen">
    <img src="https://img.shields.io/badge/Django-4.1-green">
    <img src="https://img.shields.io/badge/Version-0.0-yellow">
</p>

### About

Сайт для ведения домашней бухгалтерии.
На данный момент хостится тут: http://lizabinar.beget.tech/transactions/

### Start

Для запуска проекта, установите все библиотеки из requirements.txt.
- pip install -r requirements.txt

Создайте файл .env в корне проекта и заполните его по примеру с изображения, тут будут храниться пароли для файла settings.py.
(По умолчанию в проекте используется Postgres. Однако при желании можете изменить в файле app/settings.py настройки БД под свою любимую СУБД.) 
<img src="https://i.ibb.co/vZT58Qs/image.png"> 

<p align="center">
<p>
Подставьте свой настройки в app/settings.py (Пароль и адрес своей почты. Данные для подключения БД.)

Инициализируем стартовые миграции:
- python manage.py makemigrations accounts
- python manage.py makemigrations profiles
- python manage.py makemigrations transactions
- python manage.py makemigrations users

Применяем миграции:

- python manage.py migrate

Создаем базовые данные в БД
- python manage.py loaddata start_icons.json

Запускаем сервер и радуемся!
- python manage.py runserver


### Developers

- [LIZA_BINAR](https://github.com/LizaBinar)
- [novobransev](https://github.com/novobransev?tab=repositories)
