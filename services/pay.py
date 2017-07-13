import pingpp

# api_key 获取方式：登录 [Dashboard](https://dashboard.pingxx.com)->点击管理平台右上角公司名称->开发信息-> Secret Key
API_KEY = 'sk_test_WvLCG0abD088TWrD84arP0CO'

# app_id 获取方式：登录 [Dashboard](https://dashboard.pingxx.com)->点击你创建的应用->应用首页->应用 ID(App ID)
APP_ID = 'app_mjv1K0SWTGWTvn54'

# 设置 API Key
pingpp.api_key = API_KEY

'''
  设置请求签名密钥，密钥对需要你自己用 openssl 工具生成，如何生成可以参考帮助中心：https://help.pingxx.com/article/123161；
  生成密钥后，需要在代码中设置请求签名的私钥(rsa_private_key.pem)；
  然后登录 [Dashboard](https://dashboard.pingxx.com)->点击右上角公司名称->开发信息->商户公钥（用于商户身份验证）
  将你的公钥复制粘贴进去并且保存->先启用 Test 模式进行测试->测试通过后启用 Live 模式
'''
# # 设置私钥内容方式1：通过路径读取签名私钥
# pingpp.private_key_path = os.path.join(
#     os.path.dirname(__file__), 'your_rsa_private_key.pem')

# # 设置私钥内容方式2：直接设置请求签名私钥内容
# # pingpp.private_key = '''-----BEGIN RSA PRIVATE KEY-----
# # 私钥内容字符串
# # -----END RSA PRIVATE KEY-----'''


def create_charge(amount, order_no, channel, client_ip):
    """
    Create charge object and return response from ping++
    and whether it is created successfully.
    """
    try:
        response = pingpp.Charge.create(
            subject="在线咨询",
            body="医生向患者提供在线咨询、答疑和诊断服务",
            amount=amount,  # 订单总金额, 人民币单位：分（如订单总金额为 1 元，此处请填 100）
            order_no=order_no,
            currency='cny',
            channel=channel,  # 支付使用的第三方支付渠道取值，请参考：https://www.pingxx.com/api#api-c-new
            client_ip=client_ip,  # 发起支付请求客户端的 IP 地址，格式为 IPV4，如: 127.0.0.1
            app=dict(id=APP_ID)
        )
        return response, True
    except Exception as e:
        return {'error': e}, False
