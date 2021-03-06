"""
Views for the saml2sp app.

COMMENTARY:
- in this, we use random IDs. Instead, we probably should use IDs that are saved
    somewhere, so that we can refer to SAML messages after they are generated.
- the settings are not pretty and should migrate towards metadata, like in the
    saml2idp project.
- this project probably needs to employ the idea of "Processor" classes, like in
    the saml2idp project.
"""
# Python imports
import base64
from xml.dom.minidom import parseString
# Django imports
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
# Other imports
from BeautifulSoup import BeautifulStoneSoup
# Local imports
import codex
import common
import saml2sp_settings
import xml_render
import xml_signing

def xml_response(request, template, tv):
    return render(request, template, tv, content_type="application/xml")


#TODO: Pull IDP choices from a model. For now, just use the one from the settings.
IDP_CHOICES = (
    (saml2sp_settings.SAML2SP_IDP_REQUEST_URL,
     saml2sp_settings.SAML2SP_IDP_REQUEST_URL),
)
class IdpSelectionForm(forms.Form):
    idp = forms.ChoiceField(choices=IDP_CHOICES)

def _get_entity_id(request):
    entity_id = saml2sp_settings.SAML2SP_ENTITY_ID
    if entity_id is None:
        entity_id = request.build_absolute_uri(reverse('spssodescriptor'))
    return entity_id

def _get_email_from_assertion(assertion):
    """
    Returns the email out of the assertion.

    At present, Assertion must pass the email address as the Subject, eg.:

    <saml:Subject>
            <saml:NameID Format="urn:oasis:names:tc:SAML:2.0:nameid-format:email"
                         SPNameQualifier=""
                         >email@example.com</saml:NameID>
    """
    soup = BeautifulStoneSoup(assertion)
    subject = soup.findAll('saml2:subject')[0]
    name_id = subject.findAll('saml2:nameid')[0]
    email = name_id.string
    return email

def _email_to_username(email):
    """
    Returns a Django-safe username based on the email address.
    This is because Django doesn't support email addresses as usernames yet.

    """
    return email.replace('@', 'AT')

def _get_attributes_from_assertion(assertion):
    """
    Returns the SAML Attributes (if any) that are present in the assertion.

    NOTE: Technically, attribute values could be any XML structure.
          But for now, just assume a single string value.
    """
    attributes = {}
    soup = BeautifulStoneSoup(assertion)
    attrs = soup.findAll('saml2:attribute')
    for attr in attrs:
        name = attr['name']
        values = attr.findAll('saml2:attributevalue')
        if len(values) == 0:
            # Ignore empty-valued attributes. (I think these are not allowed.)
            continue
        elif len(values) == 1:
            #See NOTE:
            attributes[name] = values[0].string
        else:
            # It has multiple values.
            for value in values:
                #See NOTE:
                attributes.setdefault(name, []).append(value.string)
    return attributes

def _get_user_from_assertion(assertion):
    """
    Gets info out of the assertion and locally logs in this user.
    May create a local user account first.
    Returns the user object that was created.
    """
    email = _get_email_from_assertion(assertion)
    try:
        user = User.objects.get(email=email)
    except:
        user = User.objects.create_user(
            _email_to_username(email),
            email,
            saml2sp_settings.SAML2SP_SAML_USER_PASSWORD
        )

    #NOTE: Login will fail if the user has changed his password via the local
    # account. This actually is a good thing, I think.
    user = authenticate(username=user.username,
                        password=saml2sp_settings.SAML2SP_SAML_USER_PASSWORD)
    if user is None:
        raise Exception('Unable to login user "%s" with SAML2SP_SAML_USER_PASSWORD' % email)
    return user,email

def sso_login(request, selected_idp_url):
    """
    Replies with an XHTML SSO Request.
    """
    sso_destination = request.GET.get('next', None)
    request.session['sso_destination'] = sso_destination
    parameters = {
        'ACS_URL': saml2sp_settings.SAML2SP_ACS_URL,
        'DESTINATION': selected_idp_url,
        'AUTHN_REQUEST_ID': common.get_random_id(),
        'ISSUE_INSTANT': common.get_time_string(),
        'ISSUER': _get_entity_id(request),
    }
    authn_req = xml_render.get_authnrequest_xml(parameters, 
                    signed=saml2sp_settings.SAML2SP_SIGNING)
    saml_request = base64.b64encode(authn_req)
    token = sso_destination
    tv = {
        'request_url': selected_idp_url,
        'saml_request': saml_request,
        'token': token,
    }
    return render(request, 'sso_post_request.html', tv)

def sso_idp_select(request):
    """
    Allows the user to select an IDP.
    """
    request.session['first_Name']                =  request.session['first_Name']      
    request.session['last_Name']              =  request.session['last_Name']    
    request.session['email']                  =  request.session['email']        
    request.session['phone_Number']         =  request.session['phone_Number']
    request.session['orchid_Number']         =  request.session['orchid_Number']
    request.session['pi_name']                  =  request.session['pi_name']        
    request.session['pi_email']              =  request.session['pi_email']    
    request.session['pi_Institution']         =  request.session['pi_Institution']
    request.session['pi_PhoneNumber']         =  request.session['pi_PhoneNumber']
    if request.method == 'POST':
        form = IdpSelectionForm(request.POST)
        if form.is_valid():
            idp_request_url = form.cleaned_data['idp']
            return sso_login(request, idp_request_url)
    else:
        form = IdpSelectionForm()
    tv = {
        'form': form,
    }
    return render(request, 'sso_idp_selection.html', tv,
        context_instance=RequestContext(request))


@csrf_exempt
def sso_response(request):
    """
    Handles a POSTed SSO Assertion and logs the user in.
    """
    #TODO: Only allow this view to accept POSTs from trusted sites.
    #sso_session = request.session.get('sso_destination', None),
    
    first_Name                =  request.session['first_Name']      
    last_Name             =  request.session['last_Name']    
    emailUser                  =  request.session['email']        
    phone_Number         =  request.session['phone_Number']
    orchid_Number         =  request.session['orchid_Number']
    pi_Name                  =  request.session['pi_name']        
    pi_Email              =  request.session['pi_email']    
    pi_Institution         =  request.session['pi_Institution']
    pi_PhoneNumber        =  request.session['pi_PhoneNumber']
       
    sso_session = request.POST.get('RelayState', None)
    data = request.POST.get('SAMLResponse', None)
    assertion = base64.b64decode(data)
    user,email = _get_user_from_assertion(assertion)
    attributes = _get_attributes_from_assertion(assertion)
    
    if emailUser == email:
		verification_status = 1;
		verification_status_message = 'Submitted information matched with institutional record'
    else:
		verification_status = 0;
		verification_status = 'Submitted information did not match with institutional record'

    login(request, user)
    tv = {
        'user': user,
        #'assertion': assertion,
        'attributes': attributes,
        #'sso_destination': sso_session,
        'sso_destination_email': email,
        'first_Name': first_Name,
        'last_Name': last_Name,
        'email': emailUser,
        'phone_Number': phone_Number,
        'verification_status': verification_status,
        'verification_status_message': verification_status_message,
    }
    return render(request, 'sso_complete.html', tv)

@login_required
def sso_test(request):
    """
    Exposes a simple resource that requires authentication,
    so that we can kick-off the SAML conversation.
    """
    tv = {
        'session': request.session,
    }
    return render(request, 'sso_test.html', tv)

#@login_required # doesn't make sense otherwise, does it? YAGNI?
def sso_single_logout(request):
    """
    Replies with an XHTML SSO Request.
    """
    #TODO: Fill these in properly (somewhere else?).
    subject = request.user.email #FTM
    parameters = {
        'DESTINATION': saml2sp_settings.SAML2SP_IDP_SLO_URL,
        'LOGOUT_REQUEST_ID': common.get_random_id(),
        'ISSUE_INSTANT': common.get_time_string(),
        'ISSUER': _get_entity_id(request),
        'SUBJECT_FORMAT': 'urn:oasis:names:tc:SAML:2.0:nameid-format:email',
        'SP_NAME_QUALIFIER': saml2sp_settings.SAML2SP_IDP_SLO_URL, #???
        'SUBJECT': subject,
    }
    #STARTHERE: Some thoughts:
    #1. simpleSAMLphp LogoutRequest isn't signed (going from SP to IDP).
    #2. this logout_req gets b64encoded as saml_request, but SAMLTracer chokes on it. Why?
    #3. The template needs to supply a RelayState ID value (which is used later?).
    #4. simpleSAMLphp (IdP) returns a SAMLResponse. What is it checking?
    #5. the browser POSTs the return message to the SP at another view, which...
    #   ...does what? Check the RelayState ID from step #3, perhaps?
    logout_req = xml_render.get_logoutrequest_xml(parameters,                                  
                    signed=False) #saml2sp_settings.SAML2SP_SIGNING)
    saml_request = base64.b64encode(logout_req)    
    #logout(request) #TURN OFF WHILE DEBUGGING!
    tv = {
        'logout_req': logout_req,
        'saml_request': saml_request,
        'idp_logout_url': saml2sp_settings.SAML2SP_IDP_SLO_URL,
        'autosubmit': saml2sp_settings.SAML2SP_IDP_AUTO_LOGOUT,
    }
    return render(request, 'sso_single_logout.html', tv)

def descriptor(request):
    """
    Replies with the XML Metadata SPSSODescriptor.
    """
    acs_url = saml2sp_settings.SAML2SP_ACS_URL
    entity_id = _get_entity_id(request)
    pubkey = xml_signing.load_cert_data(saml2sp_settings.SAML2SP_CERTIFICATE_FILE)
    tv = {
        'acs_url': acs_url,
        'entity_id': entity_id,
        'cert_public_key': pubkey,
    }
    return xml_response(request, 'spssodescriptor.xml', tv)
    




