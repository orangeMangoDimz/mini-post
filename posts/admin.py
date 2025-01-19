from django.contrib import admin

from posts.models import Posts

# Register your models here.

class PostsAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'created_at', 'updated_at']
    search_fields = ['title', 'description']
    list_filter = ['created_at', 'updated_at']

admin.site.register(Posts, PostsAdmin)
