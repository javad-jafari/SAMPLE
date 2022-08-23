
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

**if you would like to migrate models , notice that knox package**
**maybe has a problem, dont worry just comment digest field in**
**LoginToken model in user app then migrate after complete it**
**uncomment digest and migrate it again.**

run celery and redis (use as a broker )

**make sure your Redis Container is up.**


```
linux >> celery -A config worker -l info
```
```
windows >> celery -A config worker -l info --pool=solo
```


run django on 8000:

```
python manage.py runserver
```
## migrations django

for better using of app should migrate to settle models in db


## database 

default backend dbms is sqlite3 but can use any of rdbms
like ; postgres, mysql, mariadb


## Broker

In this proj ,using **redis** as broker but can use other famuse 
brokers , rabbitmq ,...


## issues or pull requests

if you're going to make it better , you can do this .



