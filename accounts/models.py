from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile' ,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="images",default="default_profile.jpg", null=True)

    def __str__(self):
        return self.user.username

