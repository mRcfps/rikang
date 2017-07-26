import time
import uuid
from hashlib import sha256

import requests

from rest_framework import status

APP_ID = ''
APP_KEY = ''
MASTER_SECRET = ''
BASE_URL = 'https://restapi.getui.com/v1/'
AUTH_URL = BASE_URL + APP_ID + '/auth_sign'
PUSH_SINGLE_URL = BASE_URL + APP_ID + '/push_single'

timestamp = str(time.time()).replace('.', '')[:13]
sign_str = APP_KEY + timestamp + MASTER_SECRET
sign = sha256(sign_str.encode()).hexdigest()

auth_data = {
    'sign': sign,
    'timestamp': timestamp,
    'appkey': APP_KEY,
}


def send_push_to_user(message, user_id):
    """
    Send push notifications to a certain user and return
    response from Getui.
    """
    response = requests.post(AUTH_URL, json=auth_data)

    if response.status_code != status.HTTP_200_OK:
        raise ConnectionError("Can't connect to Getui server.")

    auth_token = response.json()['auth_token']

    cid = User.objects.get(id=user_id).clientid.cid
    headers = {'authtoken': auth_token}
    payload = {
        'message': {
            'appkey': APP_KEY,
            'is_offline': True,
            'offline_expire_time': 10000000,
            'msgtype': 'notification',
        },
        'notification': {
            'style': {
                'type': 0,
                'text': message,
                'title': '',
            },
        },
        'cid': cid,
        'requestid': uuid.uuid4().hex(),
    }
    response = requests.post(PUSH_SINGLE_URL,
                             json=payload,
                             headers=headers)

    return response
