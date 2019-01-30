from django.contrib import admin
from newsletters.models import NewsLetterUsers

# Register your models here.

class NewsLetterUsersAdmin(admin.ModelAdmin):
    """NewsLetter Users admin panel customization"""
    list_display = ['id', 'email', 'date_added']
    list_display_links = ['email']
    list_filter = ['date_added', 'email']
    search_fields = ['id', 'email']


admin.site.register(NewsLetterUsers, NewsLetterUsersAdmin)
