# Create your views here.

import datetime as dt
import random

from django.shortcuts import render


def get_date():
    return dt.datetime.now()


def home(request):
    return render(request, "website/home.html")


def hello(request, name):
    now = get_date()
    name = name.title()
    age = random.randint(12, 25)

    fruits = ["pomme", "banane", "poire"]
    return render(
        request,
        "website/hello.html",
        {"fruits": fruits, "now": now, "name": name, "age": age},
    )


def addition(request):
    a = int(request.GET.get("a", 0))
    b = int(request.GET.get("b", 0))
    resultat = a + b
    return render(request, "website/addition.html", {"total": resultat, "a": a, "b": b})
