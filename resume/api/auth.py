import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from resume.models import UserModel


@ensure_csrf_cookie
def api_csrf(request):
    return JsonResponse({'ok': True})


@csrf_exempt
def api_login(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    data = json.loads(request.body)
    username = data.get('username', '')
    password = data.get('password', '')

    if username == 'admin' and password == 'admin':
        request.session['username'] = 'admin'
        request.session['role'] = 'admin'
        return JsonResponse({'success': True, 'role': 'admin', 'name': 'Recruiter', 'email': 'admin'})

    user = UserModel.objects.filter(email=username, password=password).first()
    if not user:
        return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=401)

    request.session['username'] = username
    request.session['role'] = 'user'
    return JsonResponse({'success': True, 'role': 'student', 'name': user.name, 'email': user.email})


@csrf_exempt
def api_logout(request):
    request.session.flush()
    return JsonResponse({'success': True})


@csrf_exempt
def api_register(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    email = request.POST.get('email', '')
    if UserModel.objects.filter(email=email).exists():
        return JsonResponse({'success': False, 'error': 'Email already registered'}, status=400)

    user = UserModel(
        name=request.POST.get('name', ''),
        email=email,
        password=request.POST.get('password', ''),
        mobile=request.POST.get('mobile', ''),
        dob=request.POST.get('dob', ''),
        address=request.POST.get('address', ''),
        gender=request.POST.get('gender', ''),
        nationality=request.POST.get('nationality', ''),
        languages=request.POST.get('languages', ''),
    )
    if 'pic' in request.FILES:
        user.pic = request.FILES['pic']
    user.save()

    request.session['username'] = email
    request.session['role'] = 'user'
    return JsonResponse({'success': True, 'name': user.name, 'email': user.email})
