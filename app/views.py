"""
Definition of views.
"""

from django.http import HttpRequest
from datetime import datetime


from app.forms import *
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from subprocess import call
import os


@csrf_protect
def register(request):
    if request.method == 'POST':
        form = UserInformationForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['first_Name'] 		= form.cleaned_data['firstName']
            request.session['last_Name'] 		= form.cleaned_data['lastName']
            request.session['email'] 			= form.cleaned_data['username'] + form.cleaned_data['institution']
            request.session['phone_Number'] 	= form.cleaned_data['phoneNumber']
            request.session['orchid_Number'] 	= form.cleaned_data['orchidNumber']
            request.session['pi_name'] 			= form.cleaned_data['cstaPI']
            request.session['pi_email'] 		= form.cleaned_data['cstaPIUsername']
            request.session['pi_Institution'] 	= form.cleaned_data['ctsaPIInstitution']
            request.session['pi_PhoneNumber'] 	= form.cleaned_data['ctsaPIPhoneNumber']
            #return HttpResponseRedirect('/register/success/')
            return HttpResponseRedirect('/sp/idpselect/')
    else:
        form = UserInformationForm()
    
    variables =  { 'form': form }
 
    return render(request, 'registration/register.html',variables)
 
def register_success(request):
    return render_to_response(
    'registration/success.html',
    )


def aboutus(request):
    return render_to_response(
    'AboutUs.html',
    )

def contact(request):
    return render_to_response(
    'Contact.html',
    )

def indexpage(request):
    return render_to_response(
    'registration/indexpage.html',
    )


