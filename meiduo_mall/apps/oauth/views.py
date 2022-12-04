import json

from django.contrib.auth import login
from django.shortcuts import render

# Create your views here.
"""
第三方登录的步骤：
1.QQ互联平台申请成为开发者
2.QQ互联创建应用
3.按照文档开发

3.1 准备工作：
    QQ登录参数：
    1.申请的客户端id
    QQ_CLIENT_ID = '102033236' -> APPID
    2.申请的客户端密钥
    QQ_CLIENT_SECRET = 'GYdU7bswnQu990g7' -> APP Key
    3.申请时添加的回调路径
    QQ_REDIRECT_URL = 'http：xx'
    
3.2 放置QQ登录的图标（前端做）
3.3 根据oauth2.0获取 code 和 token
    对于应用：需要进行两部：
    1、获取Authorization Code： 表面是一个链接，实际是需要用户同意，然后获取code
    2、通过Authorization Code 获取 Access Token
3.4 通过token 换取 openid

将openid和用户信息进行一一绑定
前端： 当用户点击QQ登录图标，前端发送一个ajax请求

后端： 
    接受请求
    调用QQLoginTool， 生成跳转链接
    响应： 返回跳转链接
详细步骤：
1.生成QQLoginTool实例对象
2.调用对象的方法生成跳转链接
3.返回响应
"""
from QQLoginTool.QQtool import OAuthQQ
from django.views import View
from meiduo_mall import settings
from django.http import JsonResponse
from apps.oauth.models import OAuthQQUser
from apps.users.models import User


class QQLoginURLView(View):
    def post(self, request):
        # 生成QQLoginTool实例对象
        qq = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                     client_secret=settings.QQ_CLIENT_SECRET,
                     redirect_uri=settings.QQ_REDIRECT_URL,
                     state=None)
        # 调用对象的方法生成跳转链接
        qq_login_url = qq.get_qq_url()
        # 返回响应
        return JsonResponse({'code': 200, 'errmsg': 'ok', 'login_url': qq_login_url})


class QuathQQView(View):
    def get(self, request):
        # 1、获取code
        code = request.GET.get('code')
        if code is None:
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        # 2、通过code换取token
        qq = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                     client_secret=settings.QQ_CLIENT_SECRET,
                     redirect_uri=settings.QQ_REDIRECT_URL,
                     state=None)
        token = qq.get_access_token(code)
        # 3、通过token换取openid
        openid = qq.get_open_id(token)
        # 4、通过openid进行判断
        try:
            qquser  = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            # 不存在，则需要绑定
            from utils.jwt_auth import generate_token
            access_token = generate_token(openid)
            response = JsonResponse({'code': 400, 'access_token': access_token})
            return response
        else:
            # 存在
            # 绑定过直接登录
            # 设置session
            login(request, qquser.user)
            # 设置cookie
            response = JsonResponse({'code': 200, 'errmsg': 'ok'})
            response.set_cookie('username', qquser.user.username)
            return response

    # 绑定账号
    def post(self, request):
        # 1、接受请求
        data_dict = json.loads(request.body.decode())
        # 2、获取请求参数， openid
        mobile = data_dict.get('mobile')
        password = data_dict.get('password')
        sms_code = data_dict.get('sms_code')
        access_token = data_dict.get('access_token')
        # 对数据进行验证：
        """
        1、判断参数是否齐全
        2、判断手机号、密码是否合法
        3、判断短信验证码是否一致
        创建redis链接对象
        判断sms_code_server链接对象有无，无的话直接返回错误
        有的话就行判断是否正确  
        """
        # 3、根据手机号进行用户信息的查询
        from utils.jwt_auth import validate_token
        openid = validate_token(access_token)
        if openid is False:
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})

        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            # 手机号不存在
            user = User.objects.create_user(username=mobile, mobile=mobile, password=password)
        else:
            # 手机号存在
            if not user.check_password(password):
                return JsonResponse({'code': 400, 'errmsg': '账号或密码错误'})

        OAuthQQUser.objects.create(user=user, openid=openid)

        # 完成状态保持
        login(request, user)
        # 返回响应：
        response = JsonResponse({'code': 200, 'errmsg': 'ok'})
        response.set_cookie('username', user.username)
        return response

"""
itsdangerous 的基本使用
itsdangerous -> 数据加密的第三方库
1、导入 itsdangerous的类
2、创建类的实例对象
3、加密数据
"""