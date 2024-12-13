from django.contrib import admin

from website.models import Product, Sale


class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "price")  # Afficher tous les champs dans la liste
    list_filter = ("price",)  # Filtrer par le champ `price`
    search_fields = ("title",)  # Rechercher par le champ `title`


class SaleAdmin(admin.ModelAdmin):
    autocomplete_fields = ["product"]


admin.site.register(Product, ProductAdmin)
admin.site.register(Sale, SaleAdmin)
