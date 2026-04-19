import json
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from resume.models import NotificationModel


def api_notifications(request):
    notifs = list(NotificationModel.objects.values('id', 'title', 'description', 'skills', 'date'))
    for n in notifs:
        n['date'] = str(n['date'])
    return JsonResponse(notifs, safe=False)


@csrf_exempt
def api_add_notification(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    if request.session.get('role') != 'admin':
        return JsonResponse({'error': 'Admin only'}, status=403)

    data = json.loads(request.body)
    NotificationModel(
        title=data.get('title', ''),
        description=data.get('description', ''),
        skills=data.get('skills', ''),
        date=datetime.now(),
    ).save()
    return JsonResponse({'success': True})


@csrf_exempt
def api_delete_notification(request, notif_id):
    if request.session.get('role') != 'admin':
        return JsonResponse({'error': 'Admin only'}, status=403)
    NotificationModel.objects.filter(id=notif_id).delete()
    return JsonResponse({'success': True})
