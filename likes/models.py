from django.db import models
from config.models import ACTIVITY_TYPE_CHOICES, BaseModel
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.

class Likes(BaseModel):
    # custom foreign key for 'posts' or 'comments' model
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    type = models.CharField(
        choices=ACTIVITY_TYPE_CHOICES
    )

    user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE
    )
