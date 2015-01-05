unionpay
========

银联移动支付的python服务器端

### 功能

因为官方没有提供python版本SDK，也没找到开源项目，参照官方PHP代码实现了项目需要的最小功能集：

- trade: 发送订单推送请求，获得交易流水号
- parse_response: 处理银联后台回调，获得交易信息字典
- query: 发起交易信息查询，获得交易信息字典

### 依赖

- 银联支付接口版本: 1.0.11，2014-4-16发布
- requests: 用于同服务器交互

### 使用

- 集成代码
- 修改config.py中相应信息
  - mer_id: 商户ID
  - mer_backend_url: 服务器回调地址
  - secret_key: 商户秘钥
- 以函数方式，使用各接口

### 示例

- 发起支付交易，并进行查询

``` python

    order_id = datetime.datetime.strftime(datetime.datetime.now(), "%H%M%S%f")
    order_time = datetime.datetime.now()

    print '----- begin trade -----'

    print trade(order_id, 1000, order_time)

    print '----- begin query -----'

    print query(order_id, order_time=order_time)

```

- 处理银联回调（django中）

``` python

@csrf_exempt
def callback_up(request):

    ret = parse_response(request.body)
    if ret is None or ret.get('respCode', '') != '00':
        return HttpResponse('bad request', status=400)

```
