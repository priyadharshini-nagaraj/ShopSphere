from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ProfilePic(models.Model):
    host = models.ForeignKey(User,on_delete=models.CASCADE)
    pimage = models.ImageField(upload_to= 'uploads/',default = 'default_profile.webp')