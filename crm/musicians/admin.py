from django.contrib import admin

# Register your models here.
from .models import User, Musician, Band, UserProfile, Category


admin.site.register(Category)
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Musician)
admin.site.register(Band)