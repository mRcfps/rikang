import requests

APP_ID = ''
APP_KEY = ''
MASTER_KEY = ''
PUSH_URL = 'https://api.leancloud.cn/1.1/push'

headers = {
    'X-LC-Id': APP_ID,
    'X-LC-Key': APP_KEY,
    'Content-Type': 'application/json'
}


def send_push_to_all_users(message):
    """
    Send push notifications to all users and return
    response from LeanCloud.
    """
    payload = {'data': message}
    response = requests.post(PUSH_URL,
                             json=payload,
                             headers=headers)

    return response


def send_push_to_user(message, user_id):
    """
    Send push notifications to a certain user and return
    response from LeanCloud.
    """
    payload = {'data': message, 'where': {'objectId': user_id}}
    response = requests.post(PUSH_URL,
                             json=payload,
                             headers=headers)

    return response
