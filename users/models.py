from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    phone = PhoneNumberField(db_index=True, verbose_name='Телефон')
    profile_pic = models.ImageField(blank=True, upload_to="profile/%Y/%m/%d/", verbose_name='Аватарка')

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
        ordering = ['user']

    def __str__(self):
        return self.user.username

    '''
    Проверяем загруженное фото, если размер по ширине или высоте более 300 пикселей перезаписываем в 300 на 300 пикселей
    '''
    def save(self, **kwargs):
        if self.profile_pic:
            super().save(**kwargs)
            img = Image.open(self.profile_pic.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.profile_pic.path)
        else:
            super().save(**kwargs)


def create_profile(sender, **kwargs):
    if kwargs['created']:
        UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)
