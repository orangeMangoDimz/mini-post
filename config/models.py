from django.db import models

ACTIVITY_TYPE_CHOICES = [
    ('Posts', 'posts'),
    ('Comments', 'Comments'),
]

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
