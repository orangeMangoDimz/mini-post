from django.db import models

from config.models import BaseModel

# Create your models here.

class Comments(BaseModel):
    user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE
    )
    content = models.CharField(max_length=255)
