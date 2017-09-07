"""
Definition of urls for fabricapp.
"""

from django.conf.urls import  include, url
import django.contrib.auth.views
from app.views import *


# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    url(r'^sp/', include('saml2sp.urls')),
    url(r'^$', indexpage),
    url(r'^register/$', register),
    url(r'^register/success/$', register_success),
    url(r'^AboutUs/$', aboutus),
    url(r'^Contact/$', contact),

]