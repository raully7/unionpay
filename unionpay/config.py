# -*- coding: utf-8

''' 关于银联支付的若干配置 '''

# 基本信息
version = '1.0.0'
charset = 'UTF-8'

# 请求url
trade_url = 'https://mgate.unionpay.com/gateway/merchant/trade'
query_url = 'https://mgate.unionpay.com/gateway/merchant/query'

# 商户信息

# 商户ID
mer_id = 'XXXXXXXXXXXXXXX'
# 回调地址
mer_backend_url = 'https://www.XXXX.com/callback/up/'

# 签名相关
secret_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

sign_method = 'MD5'

field_signature = 'signature'
field_sign_method = 'signMethod'
