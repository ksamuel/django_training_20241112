# Create your views here.

import datetime as dt
import random

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

from website.forms import PalindromForm


def has_cool_username(user):
    return user.username in ["kevin", "nolan"]


def get_date():
    return dt.datetime.now()


def home(request):
    return render(request, "website/home.html")


def hello(
    request,
    name="",  # parameter extracted from url path
):
    now = get_date()

    age = random.randint(12, 25)

    if not name:
        # Get data from cookie (text only)
        name = request.COOKIES.get("name", "Anonyme")

    name = name.title()

    fruits = ["pomme", "banane", "poire"]
    response = render(
        request,
        "website/hello.html",
        {"fruits": fruits, "now": now, "name": name, "age": age},
    )
    if name:
        # Set cookie value and send it to the client
        response.set_cookie("name", name)
    return response


@login_required
@user_passes_test(has_cool_username)
def addition(request):
    try:
        a = int(request.GET["a"])  # get data from querystring
    except (KeyError, ValueError):
        a = 0

    b = int(request.GET.get("b", 0))

    resultat = a + b
    return render(request, "website/addition.html", {"total": resultat, "a": a, "b": b})


def palindrom(request):
    word = None
    is_palindrom = False

    if request.POST:
        word = request.POST.get("word", "")  # get data from form
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
