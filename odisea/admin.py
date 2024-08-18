from django.contrib import admin
from .models import Reader, Author, Article, Comment

class ReaderAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'updated_at')

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'bio', 'updated_at')

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'category', 'updated_at')
    list_filter = ('category',)
    search_fields = ('title', 'content')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'commenter', 'content', 'created_at', 'updated_at')
    list_filter = ('article', 'commenter')
    search_fields = ('content',)

admin.site.register(Reader, ReaderAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
