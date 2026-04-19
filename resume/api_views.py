import json, os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from resume.models import UserModel, NotificationModel
from datetime import datetime

@ensure_csrf_cookie
def api_csrf(request):
    return JsonResponse({'ok': True})

@csrf_exempt
def api_login(request):
    if request.method \!= 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    data = json.loads(request.body)
    username = data.get('username', '')
    password = data.get('password', '')
    if username == 'admin' and password == 'admin':
        request.session['username'] = 'admin'
        request.session['role'] = 'admin'
        return JsonResponse({'success': True, 'role': 'admin', 'name': 'Recruiter', 'email': 'admin'})
    user = UserModel.objects.filter(email=username, password=password).first()
    if user:
        request.session['username'] = username
        request.session['role'] = 'user'
        return JsonResponse({'success': True, 'role': 'student', 'name': user.name, 'email': user.email})
    return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=401)

@csrf_exempt
def api_logout(request):
    request.session.flush()
    return JsonResponse({'success': True})

@csrf_exempt
def api_register(request):
    if request.method \!= 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    data = request.POST
    files = request.FILES
    email = data.get('email', '')
    if UserModel.objects.filter(email=email).exists():
        return JsonResponse({'success': False, 'error': 'Email already registered'}, status=400)
    user = UserModel(
        name=data.get('name', ''),
        email=email,
        password=data.get('password', ''),
        mobile=data.get('mobile', ''),
        dob=data.get('dob', ''),
        address=data.get('address', ''),
        gender=data.get('gender', ''),
        nationality=data.get('nationality', ''),
        languages=data.get('languages', ''),
    )
    if 'pic' in files:
        user.pic = files['pic']
    user.save()
    request.session['username'] = email
    request.session['role'] = 'user'
    return JsonResponse({'success': True, 'name': user.name, 'email': user.email})

def api_profile(request):
    if not request.session.get('username') or request.session.get('role') \!= 'user':
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    try:
        user = UserModel.objects.get(email=request.session['username'])
        pic_name = str(user.pic).split('/')[-1] if user.pic else ''
        return JsonResponse({
            'name': user.name, 'email': user.email, 'mobile': str(user.mobile or ''),
            'dob': str(user.dob or ''), 'address': user.address or '',
            'gender': user.gender or '', 'nationality': user.nationality or '',
            'languages': user.languages or '', 'pic': pic_name,
            'degreepercentage': user.degreepercentage or '',
            'degreebranch': user.degreebranch or '',
            'intermediatepercentage': user.intermediatepercentage or '',
            'intermediatebranch': user.intermediatebranch or '',
            'sscpercentage': user.sscpercentage or '',
            'skills': user.skills or '',
            'personalstrengths': user.personalstrengths or '',
            'professionalstrengths': user.professionalstrengths or '',
            'careerobjective': user.careerobjective or '',
            'projecttitle': user.projecttitle or '',
            'projectdescription': user.projectdescription or '',
            'yearofExperience': user.yearofExperience or '',
            'currentworkingcompany': user.currentworkingcompany or '',
        })
    except UserModel.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

@csrf_exempt
def api_update_profile(request):
    if request.method \!= 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    if not request.session.get('username'):
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    data = json.loads(request.body)
    UserModel.objects.filter(email=request.session['username']).update(
        mobile=data.get('mobile', ''),
        address=data.get('address', ''),
        languages=data.get('languages', ''),
        degreepercentage=data.get('degreepercentage', ''),
        degreebranch=data.get('degreebranch', ''),
        intermediatepercentage=data.get('intermediatepercentage', ''),
        intermediatebranch=data.get('intermediatebranch', ''),
        sscpercentage=data.get('sscpercentage', ''),
        skills=data.get('skills', ''),
        personalstrengths=data.get('personalstrengths', ''),
        professionalstrengths=data.get('professionalstrengths', ''),
        careerobjective=data.get('careerobjective', ''),
        projecttitle=data.get('projecttitle', ''),
        projectdescription=data.get('projectdescription', ''),
        yearofExperience=data.get('yearofExperience', ''),
        currentworkingcompany=data.get('currentworkingcompany', ''),
        **(({'password': data['password']}) if data.get('password') else {}),
    )
    return JsonResponse({'success': True})

def api_search(request):
    if request.session.get('role') \!= 'admin':
        return JsonResponse({'error': 'Admin only'}, status=403)
    keyword = request.GET.get('keyword', '')
    skills = [s.strip().lower() for s in keyword.split(',') if s.strip()]
    results = []
    for user in UserModel.objects.all():
        user_skills = [s.strip().lower() for s in (user.skills or '').split(',') if s.strip()]
        score = sum(1 for s in skills if s in user_skills)
        results.append({
            'name': user.name, 'email': user.email,
            'mobile': str(user.mobile or ''), 'score': score,
            'skills': user.skills or '',
            'yearofExperience': user.yearofExperience or '',
            'currentworkingcompany': user.currentworkingcompany or '',
            'degreebranch': user.degreebranch or '',
        })
    results.sort(key=lambda x: x['score'], reverse=True)
    return JsonResponse(results, safe=False)

def api_notifications(request):
    notifs = list(NotificationModel.objects.values('id', 'title', 'description', 'skills', 'date'))
    for n in notifs:
        n['date'] = str(n['date'])
    return JsonResponse(notifs, safe=False)

@csrf_exempt
def api_add_notification(request):
    if request.method \!= 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    if request.session.get('role') \!= 'admin':
        return JsonResponse({'error': 'Admin only'}, status=403)
    data = json.loads(request.body)
    NotificationModel(
        title=data.get('title', ''),
        description=data.get('description', ''),
        skills=data.get('skills', ''),
        date=datetime.now()
    ).save()
    return JsonResponse({'success': True})

@csrf_exempt
def api_delete_notification(request, notif_id):
    if request.session.get('role') \!= 'admin':
        return JsonResponse({'error': 'Admin only'}, status=403)
    NotificationModel.objects.filter(id=notif_id).delete()
    return JsonResponse({'success': True})
