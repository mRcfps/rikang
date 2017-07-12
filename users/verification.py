import os
import random

from users.yunpian import ClientV2

COMPANY_NAME = '日康在线'

API_KEY_PATH = '../SMS_API_KEY'

# SMS Verification Code (1001~9999)
sms_code = random.randrange(1001, 9999)


def send_sms_code(phone):
    """Send sms code to the phone and return response status."""

    if not os.path.exists(API_KEY_PATH):
        raise FileNotFoundError('Please contact mrc to get sms api key.')

    with open(API_KEY_PATH, 'r') as f:
        api_key = f.read()

    client = ClientV2(api_key)
    sms_code = random.randrange(1001, 9999)
    context = {'company': COMPANY_NAME, 'code': sms_code}
    response = client.send_tpl_sms(phone, tpl_id=2, context=context)

    return response.status_code


def verify_sms_code(code):
    """Check if user's code is correct."""
    return code == sms_code
