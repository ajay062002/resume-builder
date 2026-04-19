import os
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
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm, inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Image as RLImage
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT

    user = UserModel.objects.filter(email=request.GET['email']).first()

    generated_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "generated")
    os.makedirs(generated_dir, exist_ok=True)
    certificate = os.path.join(generated_dir, user.email + ".pdf")

    PAGE_W, PAGE_H = A4
    LM = RM = 20*mm
    TM = BM = 15*mm
    W = PAGE_W - LM - RM

    BLACK  = HexColor('#000000')
    DARK   = HexColor('#1a1a1a')
    GREY   = HexColor('#444444')
    LTGREY = HexColor('#666666')
    BLUE   = HexColor('#1a56db')

    def S(name, **kw):
        kw.setdefault('fontName', 'Helvetica')
        kw.setdefault('textColor', DARK)
        kw.setdefault('fontSize', 10)
        kw.setdefault('leading', 14)
        return ParagraphStyle(name, **kw)

    sName    = S('nm', fontName='Helvetica-Bold', fontSize=22, leading=26, textColor=BLACK)
    sContact = S('ct', fontSize=9, textColor=GREY, leading=13, spaceAfter=4)
    sSecHdr  = S('sh', fontName='Helvetica-Bold', fontSize=11, textColor=BLACK,
                  leading=14, spaceBefore=10, spaceAfter=2,
                  underlineWidth=0.5, underlineColor=BLACK)
    sBody    = S('bd', fontSize=9.5, textColor=DARK, leading=14)
    sBullet  = S('bl', fontSize=9.5, textColor=DARK, leading=14, leftIndent=12, firstLineIndent=-12, spaceAfter=2)
    sLabel   = S('lb', fontName='Helvetica-Bold', fontSize=9.5, textColor=DARK, leading=14)
    sEnv     = S('ev', fontSize=9, textColor=GREY, leading=13, spaceBefore=4)

    def val_ok(v):
        return v and str(v).strip() not in ('', 'None', 'none')

    def section_hdr(title):
        return [
            Paragraph(f'<u><b>{title}</b></u>', sSecHdr),
            HRFlowable(width=W, thickness=0.6, color=BLACK, spaceAfter=5),
        ]

    def bullet(text):
        return Paragraph(f'• &nbsp;{text}', sBullet)

    def two_col_row(left, right):
        return Table(
            [[Paragraph(f'<b>{left}</b>', sLabel), Paragraph(str(right), sBody)]],
            colWidths=[48*mm, W - 48*mm],
            style=TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('TOPPADDING', (0,0), (-1,-1), 2),
                ('BOTTOMPADDING', (0,0), (-1,-1), 2),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ])
        )

    story = []

    # ── HEADER ───────────────────────────────────────────────────────────────
    pic_path = None
    if user.pic:
        from django.conf import settings
        p = os.path.join(settings.MEDIA_ROOT, str(user.pic))
        if os.path.exists(p): pic_path = p

    name_block = [
        Paragraph(str(user.name or ''), sName),
    ]
    contacts = []
    if val_ok(user.email):   contacts.append(str(user.email))
    if val_ok(user.mobile):  contacts.append(str(user.mobile))
    if val_ok(user.address): contacts.append(str(user.address))
    if contacts:
        name_block.append(Paragraph('   |   '.join(contacts), sContact))

    if pic_path:
        img = RLImage(pic_path, width=28*mm, height=28*mm)
        hdr = Table(
            [[name_block, img]],
            colWidths=[W - 32*mm, 32*mm],
            style=TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('ALIGN',  (1,0), (1,0),   'RIGHT'),
                ('LEFTPADDING',  (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('TOPPADDING',   (0,0), (-1,-1), 0),
                ('BOTTOMPADDING',(0,0), (-1,-1), 0),
            ])
        )
        story.append(hdr)
    else:
        for item in name_block:
            story.append(item)

    story.append(HRFlowable(width=W, thickness=1.2, color=BLACK, spaceAfter=6))

    # ── CAREER OBJECTIVE / PROFESSIONAL SUMMARY ───────────────────────────────
    if val_ok(user.careerobjective):
        story += section_hdr('Professional Summary')
        for line in str(user.careerobjective).split('\n'):
            if line.strip():
                story.append(bullet(line.strip()))
        story.append(Spacer(1, 4))

    # ── EDUCATION ─────────────────────────────────────────────────────────────
    has_edu = any(val_ok(v) for v in [user.degreebranch, user.degreepercentage,
                  user.intermediatebranch, user.intermediatepercentage, user.sscpercentage])
    if has_edu:
        story += section_hdr('Education')
        edu_data = []
        if val_ok(user.degreebranch) or val_ok(user.degreepercentage):
            d = str(user.degreebranch or '')
            p = (' — ' + str(user.degreepercentage) + '%') if val_ok(user.degreepercentage) else ''
            edu_data.append(('Degree', d + p))
        if val_ok(user.intermediatebranch) or val_ok(user.intermediatepercentage):
            d = str(user.intermediatebranch or '')
            p = (' — ' + str(user.intermediatepercentage) + '%') if val_ok(user.intermediatepercentage) else ''
            edu_data.append(('Intermediate (12th)', d + p))
        if val_ok(user.sscpercentage):
            edu_data.append(('SSC (10th)', str(user.sscpercentage) + '%'))
        for lbl, val in edu_data:
            story.append(two_col_row(lbl, val))
        story.append(Spacer(1, 4))

    # ── TECHNICAL SKILLS ──────────────────────────────────────────────────────
    if val_ok(user.skills):
        story += section_hdr('Technical Skills')
        skills_list = [s.strip() for s in str(user.skills).replace('\n', ',').split(',') if s.strip()]
        if skills_list:
            # Make a 3-column grid of skills
            cols = 3
            rows_data = []
            row_cells = []
            skill_style = S('sk', fontSize=9.5, textColor=DARK, leading=14)
            for i, sk in enumerate(skills_list):
                row_cells.append(Paragraph(f'• {sk}', skill_style))
                if len(row_cells) == cols:
                    rows_data.append(row_cells)
                    row_cells = []
            if row_cells:
                while len(row_cells) < cols:
                    row_cells.append(Paragraph('', skill_style))
                rows_data.append(row_cells)
            col_w = W / cols
            skill_table = Table(rows_data, colWidths=[col_w]*cols,
                style=TableStyle([
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('TOPPADDING', (0,0), (-1,-1), 2),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 2),
                    ('LEFTPADDING', (0,0), (-1,-1), 0),
                    ('RIGHTPADDING', (0,0), (-1,-1), 4),
                ]))
            story.append(skill_table)
        story.append(Spacer(1, 4))

    # ── KEY STRENGTHS ────────────────────────────────────────────────────────
    has_strengths = val_ok(user.personalstrengths) or val_ok(user.professionalstrengths)
    if has_strengths:
        story += section_hdr('Key Strengths')
        if val_ok(user.personalstrengths):
            story.append(two_col_row('Personal', str(user.personalstrengths)))
        if val_ok(user.professionalstrengths):
            story.append(two_col_row('Professional', str(user.professionalstrengths)))
        story.append(Spacer(1, 4))

    # ── PROJECTS ─────────────────────────────────────────────────────────────
    if val_ok(user.projecttitle) or val_ok(user.projectdescription):
        story += section_hdr('Projects')
        if val_ok(user.projecttitle):
            story.append(Paragraph(f'<b>{user.projecttitle}</b>', sBody))
        if val_ok(user.projectdescription):
            for line in str(user.projectdescription).split('\n'):
                if line.strip():
                    story.append(bullet(line.strip()))
        story.append(Spacer(1, 4))

    # ── EXPERIENCE ────────────────────────────────────────────────────────────
    if val_ok(user.currentworkingcompany) or val_ok(user.yearofExperience):
        story += section_hdr('Professional Experience')
        if val_ok(user.currentworkingcompany):
            story.append(Paragraph(f'<b>Current Company:</b> {user.currentworkingcompany}', sBody))
        if val_ok(user.yearofExperience):
            story.append(Paragraph(f'<b>Years of Experience:</b> {user.yearofExperience}', sBody))

    # ── PERSONAL INFO ────────────────────────────────────────────────────────
    personal = [(f, getattr(user, a, '')) for f, a in [
        ('Date of Birth', 'dob'), ('Gender', 'gender'),
        ('Nationality', 'nationality'), ('Languages Known', 'languages')
    ]]
    if any(val_ok(v) for _, v in personal):
        story += section_hdr('Personal Information')
        for lbl, val in personal:
            if val_ok(val):
                story.append(two_col_row(lbl, str(val)))

    doc = SimpleDocTemplate(certificate, pagesize=A4,
        leftMargin=LM, rightMargin=RM, topMargin=TM, bottomMargin=BM)
    doc.build(story)

    response = FileResponse(open(certificate, 'rb'), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{user.name or user.email}_resume.pdf"'
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

