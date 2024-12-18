"""
URL configuration for toto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from website.views import (
    ProductListView,
    addition,
    ajax_product_list,
    api_product_list,
    hello,
    home,
    palindrom_with_django_form,
    product_listing,
)

# Python routing
urlpatterns = [
    path(
        "admin/",  # URL
        admin.site.urls,  # View to call
    ),
    path(
        "hello/",
        hello,
        name="hello",  # name of the view for url reversing
    ),
    path("hello/<str:name>/", hello),
    path("addition/", addition, name="addition"),
    # path("palindrom/", palindrom, name="palindrom"),
    path("palindrom/", palindrom_with_django_form, name="palindrom"),
    # path("products/", product_listing_with_automation, name="products"),
    path("products/", ProductListView.as_view(), name="products"),
    path("ajax_products/", product_listing),  # full page
    path("partial/product/list/", ajax_product_list),  # page subset
    path("api/product/list/", api_product_list),
    path(
        "htmx/demo/",
        ProductListView.as_view(
            context_object_name="products",
            template_name="website/product_listing_htmx.html",
        ),
    ),
    path("", home, name="home"),
]
