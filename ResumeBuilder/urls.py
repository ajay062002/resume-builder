from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from resume.views import login, registration, logout, searchUsers, updateprofile, viewprofile, updatepic, download,addnotification, getnotifications,deletenotification

urlpatterns = [

    path('admin/', admin.site.urls),

    path('',TemplateView.as_view(template_name = 'index.html'),name='login'),
    path('login/',TemplateView.as_view(template_name = 'index.html'),name='login'),
    path('loginaction/',login,name='loginaction'),

    path('registration/',TemplateView.as_view(template_name = 'registration.html'),name='registration'),
    path('regaction/',registration,name='regaction'),

    path('search/',TemplateView.as_view(template_name="users.html"),name='search'),
    path('searchusers/',searchUsers,name='searchusers'),

    path('viewprofile/',viewprofile,name='view profile'),
    path('updateprofile/',updateprofile,name='update profile'),
    path('updatepic/',updatepic,name='update pic'),

    path('download/',download,name='download'),

    path('logout/',logout,name='logout'),

    path('addnotification/', TemplateView.as_view(template_name='addnotification.html'), name='apply'),
    path('addnotificationaction/', addnotification, name='add'),
    path('getnotifications/', getnotifications, name='view'),
    path('deletenotification/', deletenotification, name='delete'),
]
