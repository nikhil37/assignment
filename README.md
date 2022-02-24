# Assignment
## Introduction
I have made the REST API Using the Django framework without using [Django REST Framework](https://www.django-rest-framework.org/). I have met all the specification mentioned in the PDF provided. All the functions have the documentation on what they are used for. I have created automated tests for all the functionalities. The database used in this is the SQL. 
The database is enumerated with the JSON file provided in the PDF. There is a `db_base.sqlite3` which is only enumerated with the users in the JSON file.
The tests are extensive and are believed to cover all the scenarios.
The API is divided into 2 functions, which is divided on the basis of the URL. Inside each function, different if-else blocks perform different functions based on the method type from the request.
## Setup
#### Install Python
- [Windows](https://www.python.org/downloads/)
- Linux `apt install python3 python3-pip python-is-python3`
##### Install Django
```bash
pip install django
```
##### Database setup(already done)
```bash
python manage.py makemigrations
python manage.py migrate
```

## Running service
```bash
python manage.py runserver
```
## Testing service
```bash
python manage.py test
```
