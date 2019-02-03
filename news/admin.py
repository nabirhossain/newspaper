from django.contrib import admin
from .models import author, Category, Post, Comment
from import_export.admin import ImportExportModelAdmin
# Register your models here.
@admin.register(author)
class AuthorAdmin(ImportExportModelAdmin):
    list_display = ["__str__", 'id',]
    search_fields = ["auth_name"]
    pass

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ['id',"__str__",]
    search_fields = ["__str__"]
    list_per_page = 10
    pass


@admin.register(Post)
class PostAdmin(ImportExportModelAdmin):
    list_display = ["__str__",'views','category','status','posted']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['posted','author']
    search_fields = ["__str__"]
    list_per_page = 10
    pass

@admin.register(Comment)
class CommentAdmin(ImportExportModelAdmin):
    list_display = ('name', 'email', 'post', 'timestamp', 'active')
    list_filter = ('active', 'timestamp', 'updated')
    search_fields = ('name', 'email', 'body')
    pass
