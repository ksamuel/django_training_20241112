from django.contrib import admin

from website.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price")  # Afficher tous les champs dans la liste
    list_filter = ("price",)  # Filtrer par le champ `price`
    search_fields = ("name",)  # Rechercher par le champ `name`


admin.site.register(Product, ProductAdmin)
