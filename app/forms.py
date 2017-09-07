"""
Definition of forms.
"""

from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from app.models import UserInformation
from django.utils.translation import ugettext_lazy as _


class UserInformationForm(ModelForm):
    firstName = forms.CharField(max_length=254, 
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   }))
    lastName = forms.CharField(
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   }))
    username = forms.CharField(
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   }))

    institution = forms.ChoiceField( choices = [("@childrensnational.org","Children's National Medical Center"), ("@gwu.edu","George Washington University")]
                                     ,widget=forms.Select({                                   
                                   'class': 'form-control',
                                   }))   


    phoneNumber = forms.CharField( required=False,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   }))
    orchidNumber = forms.CharField( required=False,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   }))                                

    cstaPI = forms.CharField(
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   }))
    cstaPIUsername = forms.CharField(
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   }))
    ctsaPIInstitution = forms.ChoiceField( choices = [("@childrensnational.org","Children's National Medical Center"), ("@gwu.edu","George Washington University")]
                                     ,widget=forms.Select({                                   
                                   'class': 'form-control',
                                   }))   

    ctsaPIPhoneNumber = forms.CharField(
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   }))



    class Meta:
        model = UserInformation
        exclude = ()
