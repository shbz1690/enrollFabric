"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserInformation(models.Model):
    firstName = models.CharField(max_length=128)
    lastName = models.CharField(max_length=128)
    username = models.CharField(max_length=128)
    institution = models.CharField(choices = [("@childrensnational.org","Children's National Medical Center"), ("@gwu.edu","George Washington University")], max_length=128)
    phoneNumber = models.CharField(max_length=128)    
    orchidNumber = models.CharField(max_length=128)
    cstaPI = models.CharField(max_length=128)
    cstaPIUsername = models.CharField(max_length=128)
    ctsaPIInstitution = models.CharField(default="N/A",choices = [("@childrensnational.org","Children's National Medical Center"), ("@gwu.edu","George Washington University")], max_length=128)
    ctsaPIPhoneNumber = models.CharField(max_length=128) 
