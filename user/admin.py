from django.contrib import admin
from .models import User as UserModel, UserProfile as UserProfileModel, Hobby

admin.site.register(UserModel)
admin.site.register(UserProfileModel)
admin.site.register(Hobby)