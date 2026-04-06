from django.db.models import Q
from django.http import FileResponse
from django.shortcuts import render

from resume import constants
from resume.forms import UserForm, LoginForm, UpdatePICForm, UpdateProfileForm
from resume.models import UserModel, NotificationModel

from reportlab.pdfgen import canvas
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from datetime import datetime

def registration(request):

    if request.method == "POST":

        userForm = UserForm(request.POST,request.FILES)

        if userForm.is_valid():

            userModel = UserModel()

            userModel.email = userForm.cleaned_data["email"]
            userModel.password = userForm.cleaned_data["password"]
            userModel.name = userForm.cleaned_data["name"]
            userModel.mobile = userForm.cleaned_data["mobile"]
            userModel.dob = userForm.cleaned_data["dob"]
            userModel.address = userForm.cleaned_data["address"]
            userModel.gender = userForm.cleaned_data["gender"]
            userModel.nationality = userForm.cleaned_data["nationality"]
            userModel.languages = userForm.cleaned_data["languages"]
            userModel.pic=userForm.cleaned_data["pic"]

            user = UserModel.objects.filter(email=userModel.email).first()

            if user is not None:
               return render(request, 'index.html.html', {"message": "User All Ready Exist"})

            else:
                userModel.save()
                return render(request, 'index.html',{"message": "Registered Successfully"})

        return render(request, 'user.html', {"message": "Invalid Form"})

    return render(request, 'user.html', {"message": "Invalid Request"})

def login(request):

    if request.method == "GET":

        loginForm = LoginForm(request.GET)

        if loginForm.is_valid():

            uname = loginForm.cleaned_data["username"]
            upass = loginForm.cleaned_data["password"]

            if uname == "admin" and upass == "admin":

                request.session['username'] = "admin"
                request.session['role'] = "admin"

                return render(request, "users.html",locals())

            else:

                user = UserModel.objects.filter(email=uname, password=upass).first()

                if user is not None:
                    request.session['username'] = uname
                    request.session['role'] = "user"

                    user = UserModel.objects.get(email=request.session['username'])
                    user.pic = str(user.pic).split("/")[1]
                    return render(request, 'viewprofile.html',
                                  {"profile": user})

                else:
                    return render(request, 'index.html', {"message": "Invalid username or Password"})

        return render(request, 'index.html', {"message": "Invalid Form"})

    return render(request, 'index.html', {"message": "Invalid Credentials"})

def logout(request):
    try:
        del request.session['username']
    except:
        pass
    return render(request, 'index.html', {})

def viewprofile(request):
    user=UserModel.objects.get(email=request.session['username'])
    user.pic = str(user.pic).split("/")[1]
    return render(request, 'viewprofile.html',
                  {"profile": user})

def updateprofile(request):

    if request.method == "POST":
        # Get the posted form
        updateProfileForm = UpdateProfileForm(request.POST)

        if updateProfileForm.is_valid():

            password = updateProfileForm.cleaned_data["password"]
            mobile = updateProfileForm.cleaned_data["mobile"]
            address = updateProfileForm.cleaned_data["address"]
            languages = updateProfileForm.cleaned_data["languages"]

            degreepercentage = updateProfileForm.cleaned_data["degreepercentage"]
            degreebranch = updateProfileForm.cleaned_data["degreebranch"]
            intermediatepercentage = updateProfileForm.cleaned_data["intermediatepercentage"]
            intermediatebranch = updateProfileForm.cleaned_data["intermediatebranch"]
            sscpercentage = updateProfileForm.cleaned_data["sscpercentage"]
            skills = updateProfileForm.cleaned_data["skills"]
            personalstrengths = updateProfileForm.cleaned_data["personalstrengths"]
            professionalstrengths = updateProfileForm.cleaned_data["professionalstrengths"]
            projecttitle = updateProfileForm.cleaned_data["projecttitle"]
            projectdescription = updateProfileForm.cleaned_data["projectdescription"]
            careerobjective = updateProfileForm.cleaned_data["careerobjective"]
            yearofExperience = updateProfileForm.cleaned_data["yearofExperience"]
            currentworkingcompany = updateProfileForm.cleaned_data["currentworkingcompany"]

            UserModel.objects.filter(email=request.session['username']).update(password=password,
                                                                            mobile=mobile,
                                                                            address=address,
                                                                            languages=languages,
                                                                            degreepercentage=degreepercentage,
                                                                            degreebranch=degreebranch,
                                                                            intermediatepercentage=intermediatepercentage,
                                                                            intermediatebranch=intermediatebranch,
                                                                            sscpercentage=sscpercentage,skills=skills,
                                                                            personalstrengths=personalstrengths,
                                                                            professionalstrengths=professionalstrengths,
                                                                            projecttitle=projecttitle,
                                                                            projectdescription=projectdescription,
                                                                            careerobjective=careerobjective,
                                                                            yearofExperience=yearofExperience,
                                                                            currentworkingcompany=currentworkingcompany)

    user = UserModel.objects.get(email=request.session['username'])
    user.pic = str(user.pic).split("/")[1]

    return render(request, 'viewprofile.html', {"profile":user})

def updatepic(request):

    if request.method == "POST":

        updatepicfrom = UpdatePICForm(request.POST,request.FILES)

        if updatepicfrom.is_valid():

            user = UserModel.objects.filter(email=request.session['username']).first()
            user.pic = updatepicfrom.cleaned_data["pic"]

            UserModel.objects.filter(email=request.session['username']).delete()
            user.save()

        user = UserModel.objects.get(email=request.session['username'])
        user.pic = str(user.pic).split("/")[1]
        return render(request, 'viewprofile.html', {"profile": user})

#==============================================================================

def searchUsers(request):

    skills=request.GET['keyword']
    skills = skills.split(",")

    results = {}

    for user in UserModel.objects.all():
        count = 0
        for skill in skills:
            if skill.lower() in user.skills.lower().split(","):
                count = count + 1
        results.update({str(user.email): count})

    results_sorted = sorted(results, key=results.get, reverse=True)

    print("Sorted Result:", results_sorted)

    users = []

    for result in results_sorted:
        user = UserModel.objects.filter(email=result).first()
        user.score = results[result]
        users.append(user)

    return render(request,"users.html",{"users":users})

#================================================================================

def download(request):

    user=UserModel.objects.filter(email=request.GET['email']).first()

    certificate="D:\\"+user.email+".pdf"
    c = canvas.Canvas(certificate)

    c.setFillColor(HexColor('#FF3C33'))
    c.setFont("Helvetica", 15)  # choose your font type and font size
    c.drawString(280, 800, "Resume")  # write your text
    c.setFillColor(HexColor('#2A06F2'))
    c.setFont("Helvetica", 13)  # choose your font type and font size
    c.drawString(100, 750, user.name)  # write your text

    c.setFont("Helvetica", 20)  # choose your font type and font size
    c.drawString(100, 735, "----------------------------------------------------------------")  # write your text

    c.setFillColor(HexColor('#0A0505'))  # choose your font colour
    c.setFont("Helvetica", 10)  # choose your font type and font size
    c.drawString(100, 720, "Email:"+str(user.email))  # write your text
    c.drawString(100, 700, "Mobile:"+str(user.mobile))  # write your text
    c.drawString(100, 680, "Address:"+str(user.address))
    c.drawString(100, 660, "Gender:"+str(user.gender))  # write your text
    c.drawString(100, 640, "Date of Birth:"+str(user.dob))  # write your text
    c.drawString(100, 620, "Nationality:"+str(user.nationality))  # write your text
    c.drawString(100, 600, "Languages Known:"+str(user.languages))  # write your text

    c.drawImage(constants.imagepath+str(user.pic), 400, 610, width=120, height=120)

    ##  =========================================================================================================

    c.setFillColor(HexColor('#2A06F2'))
    c.setFont("Helvetica", 10)  # choose your font type and font size
    c.drawString(270, 570, "Academic Summary")  # write your text

    c.setFont("Helvetica", 20)  # choose your font type and font size
    c.drawString(100, 560, "----------------------------------------------------------------")  # write your text

    c.setFillColor(HexColor('#0A0505'))  # choose your font colour
    c.setFont("Helvetica", 10)  # choose your font type and font size
    c.drawString(100, 550, "Degree Percentage :"+str(user.degreepercentage))  # write your text
    c.drawString(100, 530, "Degree Branch :"+str(user.degreebranch))  # write your text
    c.drawString(100, 510, "Intermediate Percentage :"+str(user.intermediatepercentage))
    c.drawString(100, 490, "Intermediate Branch :"+str(user.intermediatebranch))  # write your text
    c.drawString(100, 470, "SSC Percentage :"+str(user.sscpercentage))  # write your text

    ##  =========================================================================================================

    c.setFillColor(HexColor('#2A06F2'))
    c.setFont("Helvetica", 10)  # choose your font type and font size
    c.drawString(270, 450, "Key Strengths")  # write your text

    c.setFont("Helvetica", 20)  # choose your font type and font size
    c.drawString(100, 440, "----------------------------------------------------------------")  # write your text

    c.setFillColor(HexColor('#0A0505'))  # choose your font colour
    c.setFont("Helvetica", 10)  # choose your font type and font size
    c.drawString(100, 430,"Career Objective :"+str(user.careerobjective))  # write your text
    c.drawString(100, 410, "Skills :"+str(user.skills))  # write your text
    c.drawString(100, 390, "Personal Strengths :"+str(user.personalstrengths))
    c.drawString(100, 370, "Professional Strengths :"+str(user.professionalstrengths))  # write your text

    ##  =========================================================================================================

    c.setFillColor(HexColor('#2A06F2'))
    c.setFont("Helvetica", 10)  # choose your font type and font size
    c.drawString(270, 340, "Projects Handled")  # write your text

    c.setFont("Helvetica", 20)  # choose your font type and font size
    c.drawString(100, 330, "----------------------------------------------------------------")  # write your text

    c.setFillColor(HexColor('#0A0505'))  # choose your font colour
    c.setFont("Helvetica", 10)  # choose your font type and font size
    c.drawString(100, 320, "Project Title :"+str(user.projecttitle))  # write your text
    c.drawString(100, 300, "Project Description :"+str(user.projectdescription))  # write your text

    ##  =========================================================================================================

    c.setFillColor(HexColor('#2A06F2'))
    c.setFont("Helvetica", 10)  # choose your font type and font size
    c.drawString(270, 270, "Experience Info")  # write your text

    c.setFont("Helvetica", 20)  # choose your font type and font size
    c.drawString(100, 260, "----------------------------------------------------------------")  # write your text

    c.setFillColor(HexColor('#0A0505'))  # choose your font colour
    c.setFont("Helvetica", 10)  # choose your font type and font size
    c.drawString(100, 250, "Years of Experience :"+str(user.yearofExperience))  # write your text
    c.drawString(100, 230, "Current Working Company :"+str(user.currentworkingcompany))  # write your text

    c.showPage()
    c.save()

    response = FileResponse(open(certificate, 'rb'))
    return response

#============================================================================

def addnotification(request):

    title = request.GET['title']
    description = request.GET['description']
    ndate=datetime.now()
    skills=request.GET['skills']

    NotificationModel(title=title,description=description,date=ndate,skills=skills).save()

    return render(request, 'addnotification.html', {"message": "Notification Posted SuccessFully"})

    return render(request, 'addnotification.html', {"message": "Notification Request Failed"})

def getnotifications(request):
    return render(request, "viewnotifications.html",{"notifications": NotificationModel.objects.all()})

def deletenotification(request):

    notificationid = request.GET['notificationid']
    NotificationModel.objects.get(id=notificationid).delete()

    return render(request, "viewnotifications.html", {"notifications": NotificationModel.objects.all()})