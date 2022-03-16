
![Yamdb Workflow Status](https://github.com/vakafm/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?branch=master&event=push)
# API_YAMDB 

Ссылка: http://vansitniko.hopto.org/redoc/
## Описание 
 
Проект YaMDb собирает отзывы пользователей на различные произведения.
Произведения делятся на категории: «Книги», «Фильмы», «Музыка». 
### Как запустить проект: 
Клонируем репозиторий и переходим в него: 
```bash 
git clone git@github.com:vakafm/yamdb_final.git
cd yamdb_final 
cd api_yamdb 
``` 
 
Создаем и активируем виртуальное окружение: 
```bash 
python3 -m venv venv 
source /venv/bin/activate (source /venv/Scripts/activate - для Windows) 
python -m pip install --upgrade pip 
``` 
 
Устанавливаем зависимости: 
```bash 
pip install -r requirements.txt 
``` 

 
Поднимаем контейнеры: 
```bash 
docker-compose up -d --build 
``` 

Выполняем миграции: 
```bash 
docker-compose exec web python manage.py makemigrations reviews 
``` 
```bash 
docker-compose exec web python manage.py migrate --run-syncdb
``` 

Создать суперпользователя: 
```bash 
docker-compose exec web python manage.py createsuperuser 
``` 

Собрать статику: 
```bash 
docker-compose exec web python manage.py collectstatic --no-input 
``` 

Создаём дамп базы данных: 
```bash 
docker-compose exec web python manage.py dumpdata > dumpSQL.json 
``` 


#### Шаблон наполнения .env (не включен в текущий репозиторий) расположенный по пути infra/.env 
``` 
DB_ENGINE=django.db.backends.postgresql 
DB_NAME=postgres 
POSTGRES_USER=postgres 
POSTGRES_PASSWORD=postgres 
DB_HOST=db 
DB_PORT=5432 
``` 
