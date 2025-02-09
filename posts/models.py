from django.db import models
from django.dispatch import receiver
from activities.models import Activities
from config.models import BaseModel
from django.db.models.signals import post_save
from likes.models import Likes
from mini_post.utils import get_fileupload_path

class Posts(BaseModel):
    user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE
    )
    thumbnail = models.ImageField(null=True, blank=True, upload_to=get_fileupload_path)
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return str(self.title)

    @property
    def get_thumbnail_url(self):
        if self.thumbnail and hasattr(self.thumbnail, "url"):
            return self.thumbnail.url

class PostsStat(models.Model):
    post = models.OneToOneField(
        "Posts",
        related_name="statistic",
        on_delete=models.CASCADE,
        primary_key=True
    )
    total_likes = models.PositiveIntegerField()
    total_comments = models.PositiveIntegerField()

@receiver(post_save, sender=Posts)
def _create_post_stat(sender, instance, created, **kwargs):
    if created:
        PostsStat.objects.create(
            post=instance,
            total_likes=0,
            total_comments=0
        )

        # this logic should be available in the API
        Likes.objects.create(
            content_object=instance,
            object_id=instance.pk,
            type='posts',
            user=instance.user
        )

        Activities.objects.create(
            content_object=instance,
            object_id=instance.pk,
            type='posts',
            total_likes=0
        )

