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

### Start

Для запуска проекта, установите все библиотеки из requirements.txt.
Создайте файл .env в корне проекта и заполните его по примеру с изображения. 
<p align="center">
<img src="https://i.ibb.co/vZT58Qs/image.png"> 
<p>
Подставьте свой настройки в app/settings.py (Пароль и адрес своей почты. Данные для подключения БД.)

- python manage.py makemigrations
- python manage.py migrate
- python manage.py loaddata start_icons.json
- python manage.py runserver

И переходите на домашнюю страницу.
<b>http://127.0.0.1:8000/transactions/transactions/<b>

### Developers

- [LIZA_BINAR](https://github.com/LizaBinar)
