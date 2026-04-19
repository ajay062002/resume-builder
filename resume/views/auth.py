from django.shortcuts import render
from resume.forms import UserForm, LoginForm
from resume.models import UserModel


def registration(request):
    if request.method != 'POST':
        return render(request, 'user.html', {'message': 'Invalid Request'})

    form = UserForm(request.POST, request.FILES)
    if not form.is_valid():
        return render(request, 'user.html', {'message': 'Invalid Form'})

    email = form.cleaned_data['email']
    if UserModel.objects.filter(email=email).exists():
        return render(request, 'index.html', {'message': 'User Already Exists'})

    user = UserModel()
    for field in ['email', 'password', 'name', 'mobile', 'dob',
                  'address', 'gender', 'nationality', 'languages', 'pic']:
        setattr(user, field, form.cleaned_data[field])
    user.save()
    return render(request, 'index.html', {'message': 'Registered Successfully'})


def login(request):
    if request.method != 'GET':
        return render(request, 'index.html', {'message': 'Invalid Credentials'})

    form = LoginForm(request.GET)
    if not form.is_valid():
        return render(request, 'index.html', {'message': 'Invalid Form'})

    uname = form.cleaned_data['username']
    upass = form.cleaned_data['password']

    if uname == 'admin' and upass == 'admin':
        request.session['username'] = 'admin'
        request.session['role'] = 'admin'
        return render(request, 'users.html', locals())

    user = UserModel.objects.filter(email=uname, password=upass).first()
    if not user:
        return render(request, 'index.html', {'message': 'Invalid username or Password'})

    request.session['username'] = uname
    request.session['role'] = 'user'
    user.pic = str(user.pic).split('/')[-1]
    return render(request, 'viewprofile.html', {'profile': user})


def logout(request):
    request.session.flush()
    return render(request, 'index.html', {})
