from django.forms import Form, CharField, PasswordInput, FileField

class UserForm(Form):

    email = CharField(max_length=50)
    password = CharField(max_length=50)
    name = CharField(max_length=50)
    mobile = CharField(max_length=50)
    dob = CharField(max_length=50)
    gender = CharField(max_length=50)
    nationality = CharField(max_length=50)
    address = CharField(max_length=500)
    languages= CharField(max_length=50)
    pic = FileField()

class LoginForm(Form):
    username = CharField(max_length=100)
    password = CharField(widget=PasswordInput())

class UpdateProfileForm(Form):

    password = CharField(max_length=50)
    mobile = CharField(max_length=50)
    address = CharField(max_length=500)
    languages = CharField(max_length=50)

    degreepercentage = CharField(max_length=50)
    degreebranch = CharField(max_length=50)
    intermediatepercentage = CharField(max_length=50)
    intermediatebranch = CharField(max_length=50)
    sscpercentage = CharField(max_length=50)
    skills = CharField(max_length=5000)
    personalstrengths = CharField(max_length=5000)
    professionalstrengths = CharField(max_length=5000)
    projecttitle = CharField(max_length=5000)
    projectdescription = CharField(max_length=5000)
    careerobjective = CharField(max_length=5000)
    yearofExperience = CharField(max_length=50)
    currentworkingcompany = CharField(max_length=500)

class UpdatePICForm(Form):
    pic = FileField()