# About
The main goal of this service is to allow people to read only news they want to read, without ads and without mismatching content.

Service parse ATM more than 10 news sources: DTF, Shazoo, Sports.ru, Lenta.ru etc.

Users can create their own news feed based on parsed sources simply by selecting required source and drag'n'dropping it to appropriate place in feed order position.

# Purpose
This project developed by me for the purpose of improvement Django skills.

# Tech stack
To create this project I used: Django, Django Rest Framework, Selenium, Celery, Redis, PostgreSQL, HTML/CSS (Bootstrap), JS (jQuery). 

# Principles of work
Service parse news sources. Users - subscribe to this sources by enable them in their profile source page. After sign in users are able to read parsed articles from their news feed.

Using Celery & Redis service works with a bunch of tasks. For example, scheduled tasks. One schedule tasks runs every 15 minutes to parse fresh articles. Another one runs one per day and clean all articles that are no longer treated as "fresh" for the system.

# Debug
There is a command to start the parser manually.

Command to run parser:
>>python manage.py run

Command to run parser only for specific source:
>>python manage.py run -s SHAZ

# ENV files
Project require env files in the route folder: .evn.dev, .env.prod, .env.prod.db.
Example of .env.dev file:

>DEBUG=1
SECRET_KEY=my_secret
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SQL_DATABASE=my_db
SQL_USER=my_user
SQL_PASSWORD=my_pass
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres

Example of .env.prod:

>DEBUG=0
SECRET_KEY=my_secret
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SQL_DATABASE=my_db
SQL_USER=my_user
SQL_PASSWORD=my_pass
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres

Example of .env.prod.db:

>POSTGRES_USER=my_user
POSTGRES_PASSWORD=my_pass
POSTGRES_DB=my_db