from unicodedata import category
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    is_organisor = models.BooleanField(default=True)
    is_band = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class MusicianManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class Musician(models.Model):
    first_name =  models.CharField(max_length=20)
    last_name  = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    gigs_played = models.IntegerField(default=0)
    instruments_played = models.TextField(max_length=100)
    genres = models.TextField(max_length=100)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    band = models.ForeignKey("Band", null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey("Category", related_name="musicians", null=True, blank=True, on_delete=models.SET_NULL)
    date_added = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    converted_date = models.DateTimeField(null=True, blank=True)

    objects = MusicianManager()

    def __str__(self):
       return f"{self.first_name} {self.last_name}"

# def handle_upload_follow_ups(instance, filename):
#     return f"musician_followups/musician_{instance.musician.pk}/{filename}"

# class FollowUp(models.Model):
#     musician = models.ForeignKey(Musician, related_name="followups", on_delete=models.CASCADE)
#     date_added = models.DateTimeField(auto_now_add=True)
#     notes = models.TextField(blank=True, null=True)
#     file = models.FileField(null=True, blank=True, upload_to=handle_upload_follow_ups)

#     def __str__(self):
#         return f"{self.musician.first_name} {self.musician.last_name}"

   
class Band(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
       return self.user.email


class Category(models.Model):
    name = models.CharField(max_length=30)  # New, Contacted, Converted, Unconverted
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        

post_save.connect(post_user_created_signal, sender=User)