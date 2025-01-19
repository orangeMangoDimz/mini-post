from rest_framework import fields, serializers
from posts.models import Posts, PostsStat

class PostsStatsSerializers(serializers.ModelSerializer):
    class Meta:
        model = PostsStat
        fields = [
            "post",
            "total_likes",
            "total_comments",
        ]
