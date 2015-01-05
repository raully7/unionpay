# -*- coding: utf-8

''' 封装银联的相关交互 '''

import datetime
import requests
import hashlib

import urlparse

import config as config


def trade(order_id, amount, order_time):
    ''' 交易接口

    参数

        order_id - 交易ID
        amount - 交易实际金额
        order_time - 交易时间，datetime类型

    返回

        成功 - 返回结果字典
        失败 - 返回None

    '''

    order_timeout = datetime.datetime.now() + datetime.timedelta(minutes=5)

    req = {
        'version': config.version,
        'charset': config.charset,
        'transType': '01',
        'merId': config.mer_id,
        'backEndUrl': config.mer_backend_url,
        'orderTime': datetime.datetime.strftime(order_time, "%Y%m%d%H%M%S"),
        'orderTimeout': datetime.datetime.strftime(order_timeout, "%Y%m%d%H%M%S"),
        'orderNumber': str(order_id),
        # 要求金额字段为 包含角和分、没有小数点的字符串
        'orderAmount': str(amount * 100),
    }

    r = requests.post(config.trade_url, build_req(req))

    if r.status_code == 200:
        return parse_response(r.text)
    else:
        return None


def query(order_id, order_time):
    ''' 查询接口

    参数

        order_id - 交易ID
        order_time - 交易时间，datetime类型

    返回

        成功 - 返回结果字典
        失败 - 返回None

    '''

    req = {
        'version': config.version,
        'charset': config.charset,
        'transType': '01',
        'merId': config.mer_id,
        'backEndUrl': config.mer_backend_url,
        'orderTime': datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M%S"),
        'orderNumber': str(order_id),
    }

    r = requests.post(config.query_url, build_req(req))
    if r.status_code == 200:
        return parse_response(r.text)
    else:
        return None


def parse_response(text):
    ''' 处理后台回调返回

    参数

        text - http POST请求包体

    返回

        成功 - 返回结果字典
        失败 - 返回None

    '''

    urlparse.parse_qs(text.encode('ASCII'))

    d = build_dict(text)

    if verify_response(text):
        return d

    return None


def build_sign_str(d):
    ''' 生成升序排列的字符串

    0 - 普通模式
    1 - 签名模式

    '''

    req = []
    for key in sorted(d.keys()):
        if key not in [config.field_signature, config.field_sign_method] and d[key] != '':
            req.append("%s=%s" % (key, d[key]))

    return '&'.join(req)


def build_dict(text):
    d = urlparse.parse_qs(text.encode('ASCII'))

    ret = {}
    for key in d.keys():
        if isinstance(d[key], list) and len(d[key]) == 1:
            ret[key] = d[key][0]
        else:
            ret[key] = d[key]

    return ret


def build_req(d):
    ''' 对输入参数字典，进行签名处理，并生成字符串'''

    req_str = build_sign_str(d)
    d[config.field_sign_method] = config.sign_method
    d[config.field_signature] = build_signature(req_str)

    return d


def build_signature(text):
    ''' 进行签名 '''

    sign_str = text + "&" + hashlib.md5(config.secret_key).hexdigest().lower()
    return hashlib.md5(sign_str).hexdigest().lower()


def verify_response(text):
    ''' 验证返回 '''

    d = build_dict(text)

    rep_str = build_sign_str(d)
    signature = build_signature(rep_str)

    return signature == d.get('signature', '')

if __name__ == '__main__':
    order_id = datetime.datetime.strftime(datetime.datetime.now(), "%H%M%S%f")
    order_time = datetime.datetime.now()

    print '----- begin trade -----'

    print trade(order_id, 1000, order_time)

    print '----- begin query -----'

    print query(order_id, order_time=order_time)
