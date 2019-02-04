from django.contrib import admin
from .models import Blog, Blogger, Comment

class BlogInline(admin.TabularInline):
    model = Blog

@admin.register(Blogger)
class BloggerAdmin(admin.ModelAdmin):
    fields = ['user', 'bio']
    inlines = [BlogInline]

class CommentInline(admin.TabularInline):
    fields = ['author', 'date', 'description']
    model = Comment

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'date')
    fields = ['name', 'author', 'date', 'description']
    inlines = [CommentInline]

@admin.register(Comment)
class Comment(admin.ModelAdmin):
    list_display = ('blog', 'author', 'date')
    fields = ['blog', 'author', 'date', 'description']