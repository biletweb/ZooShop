from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from PIL import Image


class Supplier(models.Model):
    title = models.CharField(max_length=100, db_index=True, verbose_name='Поставщик')
    slug = models.SlugField(max_length=100, unique=True)
    contact_person = models.CharField(max_length=100, db_index=True, blank=True, verbose_name='Контактное лицо')
    address = models.CharField(max_length=250, blank=True, verbose_name='Адрес')
    telephone = PhoneNumberField(blank=True, verbose_name='Телефон')

    class Meta:
        verbose_name = 'Поставщика'
        verbose_name_plural = 'Поставщики'
        ordering = ['title']

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Категория')
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'
        ordering = ['title']

    def __str__(self):
        return self.title


class Stock(models.Model):
    title = models.CharField(max_length=100, db_index=True, verbose_name='Наименование')
    slug = models.SlugField(max_length=100, unique=True)
    availability = models.BooleanField(default=True, verbose_name='Наличие')
    remainder = models.FloatField(blank=True, default=0, verbose_name='Остаток кг/шт')
    purchase_price = models.FloatField(verbose_name='Закупка грн')
    sale_price = models.FloatField(verbose_name='Продажа грн')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name='Поставщик')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    image = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True, verbose_name='Изображение')
    notes = models.TextField(max_length=1000, blank=True, verbose_name='Заметка')
    barcode = models.IntegerField(blank=True, default=0, db_index=True, verbose_name='Штрихкод')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлен')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменён')
# start like, dislike ##################################################################################################
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='dislikes', blank=True)
# end like, dislike ####################################################################################################

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-added_at']

    def get_absolute_url(self):
        return reverse_lazy('stock_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    def save(self):
        """
        We check the uploaded photo, if the size in width or height is more than 300 pixels,
        we rewrite it in 300 by 300 pixels
        """
        if self.image:
            super().save()
            img = Image.open(self.image.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)
        else:
            super().save()
