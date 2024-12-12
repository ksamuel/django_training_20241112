# HTTP verbs

GET => lecture
POST => creation
PUT => mise à jour totale
PATCH => mise à jour partielle
DELETE => suppression
OPTION / HEAD: ignorer

# HTTP return codes

1xx informational response – the request was received, continuing process
2xx successful – the request was successfully received, understood, and accepted
3xx redirection – further action needs to be taken in order to complete the request
4xx client error – the request contains bad syntax or cannot be fulfilled
5xx server error – the server failed to fulfil an apparently valid request

# Setup project

Install django in windows:

```
py -3.x -m venv .venv
.venv\Scripts\activate
python -m pip install django
```

Install django in Unix:

```
python3.x -m venv .venv
source .venv/Scripts/activate
python -m pip install django
```

Create project:

```
django-admin startproject <project_name>
cd <project_name>
```

Create app:

```
python manage.py startapp <app_name>
```

Insert the <app_name> in ``INSTALLED_APPS`!

# Run django

```
python manage.py runserver
```