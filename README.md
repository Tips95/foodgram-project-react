# Foodgram - социальная сеть о кулинарии
### Делитесь рецептами и пробуйте новые 
---
### Сервис доступен по адресу:
```
https://foodgram-tips.ddns.net/
```

### Возможности сервиса:
- делитесь своими рецептами
- смотрите рецепты других пользователей
- добавляйте рецепты в избранное
- быстро формируйте список покупок, добавляя рецепт в корзину
- следите за своими друзьями и коллегами

### Технологии:
- Django
- Python
- Docker

### Запуск проекта:
1. Клонируйте проект:
```
git clone https://github.com/tips95/foodgram-project-react.git
```
2. Подготовьте сервер:
```
scp docker-compose.yml <username>@<host>:/home/<username>/
scp nginx.conf <username>@<host>:/home/<username>/
scp .env <username>@<host>:/home/<username>/
```
3. Установите docker и docker-compose:
```
sudo apt install docker.io 
sudo apt install docker-compose
```
4. Соберите контейнер и выполните миграции:
```
sudo docker-compose -f docker-compose.production.yml up -d 
sudo docker-compose -f docker-compose.production.yml exec backend python manage.py migrate
```
5. Создайте суперюзера и соберите статику:
```
sudo docker-compose -f docker-compose.production.yml exec backend python manage.py createsuperuser
sudo docker-compose -f docker-compose.production.yml exec backend python manage.py collectstatic
```
6. Скопируйте статику:
```
sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /app/backend_static/
```
7. Скопируйте предустановленные данные json:
```
sudo docker-compose -f docker-compose.production.yml exec backend python manage.py import_data
```
8. Данные для проверки работы приложения:
Суперпользователь:
```
login - asd@mail.ru
password - admin 
```

![example workflow](https://github.com/tips95/foodgram-project-react/actions/workflows/main.yml/badge.svg)