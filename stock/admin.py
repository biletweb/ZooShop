from django.contrib import admin
from stock.models import Supplier, Category, Stock
from django.utils.safestring import mark_safe

admin.site.site_header = 'ZooShop'
admin.site.index_title = 'Мой первый интернет магазин'


"""
list_display - указываем поля модели которые будут отображаться в админке
list_display_links - указываем поля модели которые будут ссылками для редактирования объекта
search_fields - указываем поля модели по которым будет выполняться поиск в админке
list_filter - в эту переменную указываем поля по которым будет добавлен фильтр
prepopulated_fields - указываем автоматическое заполнение поля slug при вводе значений в поле title
list_editable - указываем поля которые будут доступны для редактирования при просмотре записи не входя в объект
"""


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('title', 'contact_person', 'address', 'telephone')
    search_fields = ('title', 'contact_person')
    prepopulated_fields = {'slug': ('title', )}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_display_links = ('title', )
    prepopulated_fields = {'slug': ('title', )}


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('title', 'availability', 'image_show', 'remainder', 'purchase_price', 'sale_price', 'added_at')
    list_display_links = ('title',)
    search_fields = ('title', )
    list_editable = ('remainder', 'availability', 'purchase_price', 'sale_price')
    list_filter = ('availability', 'category')
    prepopulated_fields = {'slug': ('title', )}

    def image_show(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="80">')
        else:
            return 'Нет'
    image_show.__name__ = 'Изображение'
