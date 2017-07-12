import random

from yunpian import ClientV2

COMPANY_NAME = '日康在线'

API_KEY = 'Please contact mRcfps.'

# SMS Verification Code (1001~9999)
sms_code = random.randrange(1001, 9999)


def send_sms_code(phone):
    """Send sms code to the phone and return response status."""
    client = ClientV2(API_KEY)
    sms_code = random.randrange(1001, 9999)
    context = {'company': COMPANY_NAME, 'code': sms_code}
    response = client.send_tpl_sms(phone, tpl_id=2, context)

    return response.status_code


def verify_sms_code(code):
    """Check if user's code is correct."""
    return code == sms_code
