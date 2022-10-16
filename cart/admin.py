from django.contrib import admin
from cart.models import Orders, Products


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('pk', 'order', 'user', 'phone', 'price_total', 'profit_total', 'added_at')
    list_display_links = ('order', )
    search_fields = ('order', )


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'amount', 'price', 'profit', 'added_at')
    list_display_links = ('order', )
