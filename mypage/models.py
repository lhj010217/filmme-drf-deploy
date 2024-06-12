from django.db import models
from accounts.models import User, UserManager

def mypage_image_upload_path(instance, filename):
    return f'mypage/{instance.id}/{filename}'

class MovieHistory(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30, null=True, default="")
    content = models.TextField(null=True, blank=True)
    poster = models.ImageField(upload_to=mypage_image_upload_path, null=True)

    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
