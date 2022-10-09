from django.contrib import admin
from users.models import UserProfile
from django.utils.safestring import mark_safe


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'image_show', 'phone')
    list_display_links = ('user', )
    search_fields = ('phone', )

    def image_show(self, obj):
        if obj.profile_pic:
            return mark_safe(f'<img src="{obj.profile_pic.url}" width="80">')
        else:
            return 'Нет'
    image_show.__name__ = 'Аватарка'
