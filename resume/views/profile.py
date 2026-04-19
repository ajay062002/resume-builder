from django.shortcuts import render
from resume.forms import UpdatePICForm, UpdateProfileForm
from resume.models import UserModel

PROFILE_FIELDS = [
    'password', 'mobile', 'address', 'languages',
    'degreepercentage', 'degreebranch',
    'intermediatepercentage', 'intermediatebranch', 'sscpercentage',
    'skills', 'personalstrengths', 'professionalstrengths',
    'projecttitle', 'projectdescription', 'careerobjective',
    'yearofExperience', 'currentworkingcompany',
]


def _get_user(session):
    return UserModel.objects.get(email=session['username'])


def _with_pic(user):
    user.pic = str(user.pic).split('/')[-1]
    return user


def viewprofile(request):
    user = _with_pic(_get_user(request.session))
    return render(request, 'viewprofile.html', {'profile': user})


def updateprofile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST)
        if form.is_valid():
            updates = {f: form.cleaned_data[f] for f in PROFILE_FIELDS}
            UserModel.objects.filter(email=request.session['username']).update(**updates)

    user = _with_pic(_get_user(request.session))
    return render(request, 'viewprofile.html', {'profile': user})


def updatepic(request):
    if request.method == 'POST':
        form = UpdatePICForm(request.POST, request.FILES)
        if form.is_valid():
            # Delete old record and re-save with new pic to update FileField
            user = UserModel.objects.filter(email=request.session['username']).first()
            user.pic = form.cleaned_data['pic']
            UserModel.objects.filter(email=request.session['username']).delete()
            user.save()

    user = _with_pic(_get_user(request.session))
    return render(request, 'viewprofile.html', {'profile': user})
