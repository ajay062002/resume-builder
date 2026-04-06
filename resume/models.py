from django.db import models

from django.db.models import Model

class UserModel(Model):

    email = models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    name=models.CharField(max_length=50,default="")
    mobile=models.CharField(max_length=50,default="")
    dob=models.CharField(max_length=50,default="")
    gender=models.CharField(max_length=50,default="")
    nationality=models.CharField(max_length=50,default="")
    address = models.CharField(max_length=500, default="")
    languages=models.CharField(max_length=50,default="")
    pic = models.FileField(upload_to="images")

    degreepercentage=models.CharField(max_length=50,default="")
    degreebranch = models.CharField(max_length=50,default="")
    intermediatepercentage = models.CharField(max_length=50,default="")
    intermediatebranch = models.CharField(max_length=50,default="")
    sscpercentage = models.CharField(max_length=50,default="")
    skills= models.CharField(max_length=5000,default="")
    personalstrengths= models.CharField(max_length=5000,default="")
    professionalstrengths = models.CharField(max_length=5000,default="")
    projecttitle = models.CharField(max_length=5000,default="")
    projectdescription = models.CharField(max_length=5000,default="")
    careerobjective = models.CharField(max_length=5000,default="")
    yearofExperience= models.CharField(max_length=50,default="")
    currentworkingcompany= models.CharField(max_length=500,default="")

class NotificationModel(Model):
    title=models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    skills = models.CharField(max_length=50)
    date=models.CharField(max_length=50)