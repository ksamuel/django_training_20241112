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

# ORM

```
In [1]: p = Product.objects.create(name="Montre", price=60)
In [3]: p =  Product(name="Stylo", price=3)
In [4]: p.save()
In [5]: Product.objects.get(id=5)
Out[5]: <Product: Croissant>
In [6]: Product.objects.filter(price__gte=1)[a:4]
In [7]: Product.objects.filter(price__gte=1)[1:4]
Out[7]: <QuerySet [<Product: Brique de lait (1l)>, <Product: iPhone>, <Product: Steam Deck>]>
In [28]: prods.order_by("-name")
Out[28]: <QuerySet [<Product: iPhone>, <Product: Stylo>, <Product: Steam Deck>, <Product: Montre>, <Product: Brique de lait (1l)>, <Product: Baguette>]>
In [29]: prods.order_by("-name", "price")
Out[29]: <QuerySet [<Product: iPhone>, <Product: Stylo>, <Product: Steam Deck>, <Product: Montre>, <Product: Brique de lait (1l)>, <Product: Baguette>]>
In [31]: from django.db.models import Count, Case, When
In [34]: Product.objects.aggregate(cheap=Count(Case(When(price__lt=10, then=1))), expensive=Count(Case(When(price__gte=10, then=1))))
Out[34]: {'cheap': 4, 'expensive': 3}
In [39]: from django.db.models import F
In [40]: from django.db.models.functions import Length
In [43]: p = Product.objects.annotate(gros_prix=F('price') + Length('name'))
In [44]: p[0].gros_prix
Out[44]: 9.3
```

# Translation:

Install gettex for windows: https://mlocati.github.io/articles/gettext-iconv-windows.html

Create a directory for each translation in your app:

```
locale/<lang_code>/LC_MESSAGES
```

Ex:

```
locale/fr/LC_MESSAGES for french.
```

Then run:

```
python manage.py makemessages -l fr
python manage.py compilemessages
```