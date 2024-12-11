# Create your views here.

import datetime as dt
import random

from django.shortcuts import render

from website.forms import PalindromForm


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
    try:
        a = int(request.GET["a"])
    except (KeyError, ValueError):
        a = 0

    b = int(request.GET.get("b", 0))

    resultat = a + b
    return render(request, "website/addition.html", {"total": resultat, "a": a, "b": b})


def palindrom(request):
    word = None
    is_palindrom = False

    if request.POST:
        word = request.POST.get("word", "")
        is_palindrom = word == word[::-1]

    return render(
        request, "website/palindrom.html", {"is_palindrom": is_palindrom, "word": word}
    )


def palindrom_with_django_form(request):
    form = PalindromForm(request.POST or None)
    is_palindrom = False

    if form.is_valid():
        word = form.cleaned_data["word"]
        is_palindrom = word == word[::-1]

    return render(
        request,
        "website/palindrom_with_django_form.html",
        {"is_palindrom": is_palindrom, "form": form},
    )
