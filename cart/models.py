from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Orders(models.Model):
    order = models.CharField(max_length=100, db_index=True, verbose_name='Ордер')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    phone = PhoneNumberField(blank=True, verbose_name='Телефон')
    price_total = models.CharField(max_length=100, verbose_name='Цена грн')
    profit_total = models.CharField(max_length=100, verbose_name='Профит грн')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлен')

    class Meta:
        verbose_name = 'Ордер'
        verbose_name_plural = 'Ордера'
        ordering = ['-added_at']

    def __str__(self):
        return f' Заказ № {self.pk} ордер: {self.order}'


class Products(models.Model):
    product = models.CharField(max_length=100, db_index=True, verbose_name='Наименование')
    order = models.ForeignKey('Orders', blank=True, on_delete=models.CASCADE, null=True, related_name='orders', verbose_name='Ордер')
    amount = models.CharField(max_length=100, verbose_name='Количество')
    price = models.CharField(max_length=100, verbose_name='Цена грн')
    profit = models.CharField(max_length=100, verbose_name='Профит грн')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлен')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['order']

    def __str__(self):
        return self.product
