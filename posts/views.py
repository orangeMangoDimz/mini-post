from django.core.cache import cache
from django.db.models import Count, Prefetch
from django.shortcuts import render
from django.views.generic.list import ListView
from likes.models import Likes
from .models import Posts, PostsStat
from asgiref.sync import async_to_sync
from django.contrib.contenttypes.models import ContentType
from channels.layers import get_channel_layer

class PostView(ListView):
    model = Posts
    template_name = "posts/index.html"
    context_object_name = "posts"

    def get_queryset(self):
        qs = Posts.objects.prefetch_related("statistic").all()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        post_content_type = ContentType.objects.get_for_model(Posts)

        like_object_ids = Likes.objects.filter(
            content_type=post_content_type,
            user=user,
            type="posts",
            object_id__in=[post.id for post in context['posts']]
        ).values_list('object_id', flat=True)

        context["liked_post"] = set(like_object_ids)
        context["room_name"] = "test"
        return context