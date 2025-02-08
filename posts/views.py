from django.core.cache import cache
from django.db.models import Count, Prefetch
from django.shortcuts import render
from django.views.generic.list import ListView
from likes.models import Likes
from .models import Posts, PostsStat

# Create your views here.

class PostView(ListView):
    model = Posts
    template_name = "posts/index.html"

    def get_queryset(self):
        qs = Posts.objects.prefetch_related("statistic").all()
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["room_name"] = "test"
        return context
    
