from django.contrib import admin

from resume.models import UserModel,NotificationModel

admin.site.register(UserModel)
admin.site.register(NotificationModel)