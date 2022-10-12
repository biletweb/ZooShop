from django.contrib import admin
from comments.models import Comments


@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'validation', 'comment', 'added_at')
    list_display_links = ('comment', )
    list_editable = ('validation', )
    search_fields = ('comment', )
    list_filter = ('validation', 'added_at')
