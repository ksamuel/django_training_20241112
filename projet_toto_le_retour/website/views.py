# Create your views here.

import datetime as dt
import random

from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from django.views.generic import CreateView, ListView
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from website.forms import PalindromForm, ProductForm, ProductModelForm
from website.models import Product


def has_cool_username(user):  # must return True/False
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
        name = request.COOKIES.get("name", _("Anonymous"))

    name = name.title()

    fruits = [_("apple"), _("banane"), _("pear")]
    response = render(
        request,
        "website/hello.html",
        {"fruits": fruits, "now": now, "name": name, "age": age},
    )
    if name:
        # Set cookie value and send it to the client
        response.set_cookie("name", name)
    return response


@login_required  # decorator to check if user is logged in or redirect to login
@user_passes_test(has_cool_username)  # check if user matches a condition
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


PAGINATION = 10


def product_listing(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        p = Product.objects.create(
            name=form.cleaned_data["name"], price=form.cleaned_data["price"]
        )
        return redirect("products")

    products = Product.objects.all()

    product_filter = request.GET.get("filter", "")
    if product_filter:
        products = products.filter(name__icontains=product_filter)

    try:
        current_page = int(request.GET.get("page", 1))
    except (ValueError, TypeError):
        current_page = 1

    all_pages = range(1, int(products.count() / PAGINATION) + 1)
    product_start = (current_page - 1) * PAGINATION
    product_stop = product_start + PAGINATION
    products = products[product_start:product_stop]

    return render(
        request,
        "website/product_listing.html",
        {
            "all_pages": all_pages,
            "current_page": current_page,
            "product_filter": product_filter,
            "products": products,
            "form": form,
        },
    )


def ajax_product_list(request):
    products = Product.objects.all()

    product_filter = request.GET.get("filter", "")
    if product_filter:
        products = products.filter(name__icontains=product_filter)

    try:
        current_page = int(request.GET.get("page", 1))
    except (ValueError, TypeError):
        current_page = 1

    product_start = (current_page - 1) * PAGINATION
    product_stop = product_start + PAGINATION
    products = products[product_start:product_stop]

    return render(
        request,
        "website/_product_list.html",
        {
            "products": products,
        },
    )


def product_listing_with_automation(request):
    form = ProductModelForm(request.POST or None)
    if form.is_valid():
        p = form.save()
        return redirect("products")

    products = Product.objects.all()

    product_filter = request.GET.get("filter", "")
    if product_filter:
        products = products.filter(name__icontains=product_filter)

    try:
        current_page = int(request.GET.get("page", 1))
    except (ValueError, TypeError):
        current_page = 1

    paginator = Paginator(products, PAGINATION)
    products = paginator.get_page(current_page)

    return render(
        request,
        "website/product_listing.html",
        {
            "all_pages": paginator.page_range,
            "current_page": current_page,
            "product_filter": product_filter,
            "products": products,
            "form": form,
        },
    )


def filter_queryset(request, queryset):
    product_filter = request.GET.get("filter", "")
    if product_filter:
        return queryset.filter(name__icontains=product_filter), product_filter
    return queryset, product_filter


def paginate_queryset(request, queryset, pagination=PAGINATION):
    try:
        current_page = int(request.GET.get("page", 1))
    except (ValueError, TypeError):
        current_page = 1

    paginator = Paginator(queryset, PAGINATION)
    return paginator, current_page, paginator.get_page(current_page)


def handle_form(request, form_class):
    form = form_class(request.POST or None)
    if form.is_valid():
        form.save()
        raise HttpResponseRedirect("/products/")
    return form


def product_listing_with_automation_decoupled(request):
    form = handle_form(request, ProductModelForm)
    products, product_filter = filter_queryset(request, Product.objects.all())
    paginator, current_page, products = paginate_queryset(request, products)

    return render(
        request,
        "website/product_listing.html",
        {
            "all_pages": paginator.page_range,
            "current_page": current_page,
            "product_filter": product_filter,
            "products": products,
            "form": form,
        },
    )


class FilteredListViewMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        self.product_filter = self.request.GET.get("filter", "")
        return qs.filter(name__icontains=self.product_filter)


class PaginatedListViewMixin:
    paginate_by = 10

    def get_context_data(self):
        context = super().get_context_data()
        try:
            context["current_page"] = int(self.request.GET.get("page", 1))
        except (ValueError, TypeError):
            context["current_page"] = 1

        return context


class ProductListView(
    PaginatedListViewMixin, FilteredListViewMixin, ListView, CreateView
):
    model = Product
    form_class = ProductModelForm
    template_name = "website/product_listing_cbv.html"
    success_url = "."
    object = None

    def get_queryset(self):
        qs = super().get_queryset()
        self.product_filter = self.request.GET.get("filter", "")
        return qs.filter(name__icontains=self.product_filter)

    def get_context_data(self):
        context = super().get_context_data()
        context["filter"] = self.product_filter
        return context


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.FloatField()


@api_view(["GET"])
def api_product_list(request):
    products, _ = filter_queryset(request, Product.objects.all())
    _, _, page = paginate_queryset(request, products)
    serializer = ProductSerializer(list(page.object_list), many=True)
    return Response(serializer.data)
