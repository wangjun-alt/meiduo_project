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
            response = JsonResponse({'code': 400, 'access_token': openid})
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