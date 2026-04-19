import json
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from resume.models import UserModel
from resume.pdf import build_resume_pdf

UPDATABLE_FIELDS = [
    'mobile', 'address', 'languages',
    'degreepercentage', 'degreebranch',
    'intermediatepercentage', 'intermediatebranch', 'sscpercentage',
    'skills', 'personalstrengths', 'professionalstrengths',
    'careerobjective', 'projecttitle', 'projectdescription',
    'yearofExperience', 'currentworkingcompany',
]


def api_profile(request):
    if not request.session.get('username') or request.session.get('role') != 'user':
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    try:
        user = UserModel.objects.get(email=request.session['username'])
    except UserModel.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

    pic_name = str(user.pic).split('/')[-1] if user.pic else ''
    data = {f: getattr(user, f, '') or '' for f in UPDATABLE_FIELDS}
    data.update({'name': user.name, 'email': user.email, 'pic': pic_name,
                 'dob': str(user.dob or ''), 'gender': user.gender or '',
                 'nationality': user.nationality or ''})
    return JsonResponse(data)


@csrf_exempt
def api_update_profile(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    if not request.session.get('username'):
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    data = json.loads(request.body)
    updates = {f: data.get(f, '') for f in UPDATABLE_FIELDS}
    if data.get('password'):
        updates['password'] = data['password']

    UserModel.objects.filter(email=request.session['username']).update(**updates)
    return JsonResponse({'success': True})


@csrf_exempt
def api_upload_pic(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    if not request.session.get('username'):
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    if 'pic' not in request.FILES:
        return JsonResponse({'error': 'No file uploaded'}, status=400)

    user = UserModel.objects.filter(email=request.session['username']).first()
    if not user:
        return JsonResponse({'error': 'User not found'}, status=404)

    user.pic = request.FILES['pic']
    user.save()
    return JsonResponse({'success': True, 'pic': str(user.pic).split('/')[-1]})


def api_download_pdf(request):
    if not request.session.get('username') or request.session.get('role') != 'user':
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    user = UserModel.objects.filter(email=request.session['username']).first()
    if not user:
        return JsonResponse({'error': 'User not found'}, status=404)

    pdf_path = build_resume_pdf(user)
    filename = f'{user.name or user.email}_resume.pdf'
    response = FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
