
# SAMPLE


project consist of two main apps:
 - user
 - otp

user app handle register, login, logout
otp app handle send otp, (verify otp)

# install and using app

clone project from github

make virtualenv and activate it :
```
source venv/bin/activate
```

install requierments from req.text :
```
pip install -r requierment.text
```

run celery and celery beat and redis (use as a broker )

```
linux >> celery -A proj worker -l info
```
```
windows >> celery -A proj worker -l info --pool=solo
```


run django on 8000:

```
python manage.py runserver
```
## migrations django and celery beat

for better using of app should migrate to settle models in db


## database 

default backend dbms is sqlite3 but can use any of rdbms
like ; postgres, mysql, mariadb


## Broker

In this proj ,using **redis** as broker but can use other famuse 
brokers , rabbitmq ,...

## .env file 

have to touch a .env file in root of proj and set these data :

 - CELERY_BROKER_URL
optional :
CELERY_RESULT_BACKEND
CELERY_ACCEPT_CONTENT
CELERY_TASK_SERIALIZER
CELERY_RESULT_SERIALIZER
CELERY_TIMEZONE 

## issues or pull requests

if you're going to make it better , you can do this .



