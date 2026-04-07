from django.contrib import admin

from .models import Application, UserProfile

admin.site.register([Application, UserProfile])
