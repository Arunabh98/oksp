from django.contrib import admin

# Register your models here.
from .models import News, Comment


class NewsAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_display_links = ['title']
    search_fields = ['title']
    context_object_name = 'News'
    
    class Meta:
        model = News


class CommentsAdmin(admin.ModelAdmin):
    list_display = ['text']
    list_display_links = ['text']
    search_fields = ['text']

    class Meta:
        model = Comment


admin.site.register(News, NewsAdmin)
admin.site.register(Comment, CommentsAdmin)
