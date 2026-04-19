from django.http import JsonResponse
from resume.models import UserModel


def api_search(request):
    if request.session.get('role') != 'admin':
        return JsonResponse({'error': 'Admin only'}, status=403)

    keyword = request.GET.get('keyword', '')
    search_skills = [s.strip().lower() for s in keyword.split(',') if s.strip()]

    results = []
    for user in UserModel.objects.all():
        user_skills = [s.strip().lower() for s in (user.skills or '').split(',') if s.strip()]
        score = sum(1 for s in search_skills if s in user_skills)
        results.append({
            'name': user.name,
            'email': user.email,
            'mobile': str(user.mobile or ''),
            'score': score,
            'skills': user.skills or '',
            'yearofExperience': user.yearofExperience or '',
            'currentworkingcompany': user.currentworkingcompany or '',
            'degreebranch': user.degreebranch or '',
        })

    results.sort(key=lambda x: x['score'], reverse=True)
    return JsonResponse(results, safe=False)
