from django.shortcuts import render
from resume.models import UserModel


def searchUsers(request):
    keyword = request.GET.get('keyword', '')
    search_skills = [s.strip().lower() for s in keyword.split(',') if s.strip()]

    scored = []
    for user in UserModel.objects.all():
        user_skills = [s.strip().lower() for s in (user.skills or '').split(',')]
        user.score = sum(1 for s in search_skills if s in user_skills)
        scored.append(user)

    scored.sort(key=lambda u: u.score, reverse=True)
    return render(request, 'users.html', {'users': scored})
