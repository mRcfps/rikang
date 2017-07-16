import os
import random

from users.yunpian import ClientV2

COMPANY_NAME = '日康在线'

API_KEY_PATH = '../SMS_API_KEY'


def send_sms_code(phone_number, sms_code):
    """Send sms code to the phone and return response status."""

    if not os.path.exists(API_KEY_PATH):
        raise FileNotFoundError('Please contact mrc to get sms api key.')

    with open(API_KEY_PATH, 'r') as f:
        api_key = f.read()

    client = ClientV2(api_key)
    context = {'company': COMPANY_NAME, 'code': sms_code}
    response = client.send_tpl_sms(phone_number, tpl_id=2, context=context)

    return response.status_code
