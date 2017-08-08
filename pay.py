import pingpp
import keys

from services.types import SERVICE_NAME, SERVICE_DESCRIPTION

# app_id 获取方式：登录 [Dashboard](https://dashboard.pingxx.com)->点击你创建的应用->应用首页->应用 ID(App ID)
APP_ID = 'app_mjv1K0SWTGWTvn54'

# 设置 API Key
pingpp.api_key = keys.PAY_API_KEY

# 设置请求签名私钥
pingpp.private_key_path = 'rsa_private_key.pem'


def create_charge(service_type, cost, order_no, channel, client_ip):
    """
    Create charge object and return response from ping++
    and whether it is created successfully.
    """
    try:
        response = pingpp.Charge.create(
            subject=SERVICE_NAME[service_type],
            body=SERVICE_DESCRIPTION[service_type],
            amount=float(cost)*100,
            order_no=order_no,
            currency='cny',
            channel=channel,
            client_ip=client_ip,
            app=dict(id=APP_ID)
        )
        return response, True
    except Exception as e:
        return {'error': e.args[0]}, False


def refund(charge_id):
    """Full refund for a charge and return response from ping++
    and whether refund is made.
    """
    try:
        charge = pingpp.Charge.retrieve(charge_id)
        ref = charge.refunds.create(description="超时未接受预约")
        return ref, True
    except Exception as e:
        return {'error': e.args[0]}, False
