from django.db import models
from django.contrib.auth.models import User
from stock.models import Stock


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    title = models.ForeignKey(Stock, on_delete=models.CASCADE, verbose_name='Наименование')
    comment = models.TextField(max_length=1000, blank=True, verbose_name='Комментарий')
    answer = models.ForeignKey('Comments', blank=True, on_delete=models.CASCADE, null=True, related_name='replies',
                               verbose_name='Ответ')
    validation = models.BooleanField(default=True, verbose_name='Прошел проверку')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлен')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-added_at']

    def __str__(self):
        return str(self.comment)
