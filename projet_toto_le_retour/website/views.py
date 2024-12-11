# Create your views here.

import datetime as dt

from django.shortcuts import render


def hello(request):
    now = dt.datetime.now()
    context = {"maintenant": now}
    return render(request, "website/hello.html", context)
