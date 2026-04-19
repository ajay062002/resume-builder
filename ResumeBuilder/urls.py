from django.contrib import admin
from django.urls import path
from resume import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from resume import api as api_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # React UI (main entry point)
    path('', RedirectView.as_view(url='/static/resume-ranking.html')),

    # Django template pages (kept as fallback)
    path('login', views.login, name='login'),
    path('loginaction/', views.login, name='loginaction'),
    path('registration', views.registration, name='registration'),
    path('regaction/', views.registration, name='regaction'),
    path('logout', views.logout, name='logout'),
    path('viewprofile', views.viewprofile, name='viewprofile'),
    path('updateprofile/', views.updateprofile, name='updateprofile'),
    path('updatepic/', views.updatepic, name='updatepic'),
    path('search', views.searchUsers, name='search'),
    path('searchusers/', views.searchUsers, name='searchusers'),
    path('addnotification', views.addnotification, name='addnotification'),
    path('addnotificationaction', views.addnotification, name='addnotificationaction'),
    path('getnotifications', views.getnotifications, name='getnotifications'),
    path('deletenotification', views.deletenotification, name='deletenotification'),
    path('download', views.download, name='download'),
    path('download/', views.download),

    # JSON API endpoints (for React UI)
    path('api/csrf/', api_views.api_csrf),
    path('api/login/', api_views.api_login),
    path('api/logout/', api_views.api_logout),
    path('api/register/', api_views.api_register),
    path('api/profile/', api_views.api_profile),
    path('api/profile/update/', api_views.api_update_profile),
    path('api/search/', api_views.api_search),
    path('api/notifications/', api_views.api_notifications),
    path('api/notifications/add/', api_views.api_add_notification),
    path('api/notifications/<int:notif_id>/delete/', api_views.api_delete_notification),
    path('api/profile/pic/', api_views.api_upload_pic),
    path('api/download/', api_views.api_download_pdf),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
