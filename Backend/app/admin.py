from django.contrib import admin
from .models import Post , Comment, Profile,Notifications

admin.site.register[(Post,Comment,Profile,Notifications)]