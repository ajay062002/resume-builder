from datetime import datetime
from django.shortcuts import render
from resume.models import NotificationModel


def addnotification(request):
    NotificationModel(
        title=request.GET.get('title', ''),
        description=request.GET.get('description', ''),
        skills=request.GET.get('skills', ''),
        date=datetime.now(),
    ).save()
    return render(request, 'addnotification.html', {'message': 'Notification Posted Successfully'})


def getnotifications(request):
    return render(request, 'viewnotifications.html',
                  {'notifications': NotificationModel.objects.all()})


def deletenotification(request):
    NotificationModel.objects.filter(id=request.GET.get('notificationid')).delete()
    return render(request, 'viewnotifications.html',
                  {'notifications': NotificationModel.objects.all()})
