import os
import random

import keys

from users.yunpian import ClientV2

COMPANY_NAME = '日康在线'

API_KEY = keys.SMS_API_KEY


def send_sms_code(phone_number, sms_code):
    """Send sms code to the phone and return response status."""

    client = ClientV2(API_KEY)
    context = {'company': COMPANY_NAME, 'code': str(sms_code)}
    response = client.send_tpl_sms(phone_number, tpl_id=2, tpl_context=context)

    return response.status_code
