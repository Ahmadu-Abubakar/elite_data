from django.db import models
from django.contrib.auth.models import AbstractUser 

class User(AbstractUser):

    email = models.EmailField(unique=True)

    phone_number = models.CharField(max_length=15)


    created_at = models.DateTimeField(
        auto_now_add=True
    )



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    profile_picture = models.ImageField(
        upload_to="profile_pics/", blank=True, null=True
    )
