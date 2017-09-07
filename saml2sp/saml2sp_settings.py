from django.conf import settings

try:
    SAML2SP_ACS_URL = settings.SAML2SP_ACS_URL
except:
    SAML2SP_ACS_URL = 'http://www.samltestcnmc.com/sp/acs/'

try:
    SAML2SP_ENTITY_ID = settings.SAML2SP_ENTITY_ID
except:
    # A value of None will default to the metadata URL, in the views.
    SAML2SP_ENTITY_ID = 'http://www.samltestcnmc.com/sp/metadata'

try:
    SAML2SP_IDP_SLO_URL = settings.SAML2SP_IDP_SLO_URL
except:
    SAML2SP_IDP_SLO_URL = 'https://singlesignon.gwu.edu/idp/profile/SAML2/POST/SLO'

try:
    SAML2SP_IDP_AUTO_LOGOUT = settings.SAML2SP_IDP_AUTO_LOGOUT
except:
    SAML2SP_IDP_AUTO_LOGOUT = False

try:
    SAML2SP_IDP_REQUEST_URL = settings.SAML2SP_IDP_REQUEST_URL
except:
    SAML2SP_IDP_REQUEST_URL = 'https://singlesignon.gwu.edu/idp/profile/SAML2/POST/SSO'

try:
    SAML2SP_SAML_USER_PASSWORD = settings.SAML2SP_SAML_USER_PASSWORD
except:
    SAML2SP_SAML_USER_PASSWORD = settings.SECRET_KEY[::-1]
    
try:
    SAML2SP_SIGNING = settings.SAML2SP_SIGNING
except:
    SAML2SP_SIGNING = False

# If using relative paths, be careful!
try:
    SAML2SP_CERTIFICATE_FILE = settings.SAML2SP_CERTIFICATE_FILE
except:
    SAML2SP_CERTIFICATE_FILE = 'keys/sample/certificate.pem'

# If using relative paths, be careful!
try:
    SAML2SP_PRIVATE_KEY_FILE = settings.SAML2SP_PRIVATE_KEY_FILE
except:
    SAML2SP_PRIVATE_KEY_FILE = 'keys/sample/private-key.pem'
