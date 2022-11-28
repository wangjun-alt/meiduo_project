from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from captcha.captcha import captcha
from django_redis import get_redis_connection
from ronglian_sms_sdk import SmsSDK

# 图片验证码模块
class ImageCodeView(View):

    def get(self, request, uuid):
        text, image = captcha.generate_captcha()
        redis_cli = get_redis_connection('image_code')
        redis_cli.setex(uuid, 100, text)
        return HttpResponse(image, content_type='image/png')


# 注册验证（验证码校验）
class SmsCodeView(View):

    def get(self, request, mobile):
        # 1、获取请求参数
        image_code = request.GET.get('image_code')
        uuid = request.GET.get("image_code_id")
        # 2、校验参数
        if not all([image_code, uuid]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        # 3、验证图片验证码
        redis_cli = get_redis_connection('code')
        redis_image_code = redis_cli.get(uuid)
        if redis_image_code is None:
            return JsonResponse({'code': 400, 'errmsg': '图片验证码已过期'})
        if redis_image_code.decode().lower() != image_code.lower():
            return JsonResponse({'code': 400, 'errmsg': '图片验证码错误'})
        # 4、生成短信验证码：
        from random import randint
        sms_code = "%06d" % randint(0, 999999)
        # 5、保存短信验证码：
        redis_cli.setex(mobile, 300, sms_code)
        # 6、发送短信验证码：
        accId = '8aaf0708842397dd0184b91dbc943559'
        accToken = 'c042a8b512024bc2a3970ce0119988e1'
        appId = '8aaf0708842397dd0184b91dbd8b3560'
        sdk = SmsSDK(accId, accToken, appId)
        tid = '1'
        mobile = '18392119861'
        datas = (sms_code, 5)
        sdk.sendMessage(tid, mobile, datas)
        return JsonResponse({'code': '200', 'errmsg': 'ok'})
