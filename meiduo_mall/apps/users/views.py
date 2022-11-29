import json
import re

from django.shortcuts import render
from django.views import View
from apps.users.models import User
from django.http import JsonResponse


# Create your views here.
class UsernameCountView(View):
    def get(self, request, username):
        # 1、接受用户名
        # 2、根据用户名，查询数据库
        count = User.objects.filter(username=username).count()
        # 3、返回响应
        return JsonResponse({'code': 200, 'count': count, 'errmsg': 'ok'})


class RegisterView(View):
    def post(self, request):
        # 1、接受请求（POST-----JSON）
        body_bytes = request.body
        body_str = body_bytes.decode()
        body_dict = json.loads(body_str)
        # 2、获取数据
        username = body_dict.get('username')
        password = body_dict.get('password')
        password2 = body_dict.get('password')
        mobile = body_dict.get('mobile')
        allow = body_dict.get('allow')
        # 3、验证数据
        if not all([username, password, password2, mobile, allow]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        if not re.match('[a-zA-Z_-]{5-20}', username):
            return JsonResponse({'code': 400, 'errmsg': '用户名命名不规范'})
        # 还有包含数据验证的基本操作省略
        # 4、数据入库
        user = User.objects.create_user(username=username, password = password, mobile=mobile)
        from django.contrib.auth import login
        login(request,user)
        # 5、返回响应
        return JsonResponse({'code': 200, 'errmsg': 'ok'})


class LoginView(View):
    def post(self, request):
        # 1、接收数据
        data = json.loads(request.body.decode())
        username = data.get('username')
        password = data.get('password')
        remembered = data.get('remembered')
        # 2、验证数据
        if not all([username, password]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        """
        确定通过手机号查询还是根据用户名查询
        USERNAME_FIELD 我们可以根据 修改 User. USERNAME_FIELD 字段
        authenticate 就是根据USERNAME_FIELD 字段来查询
        """
        if re.match('1[3-9]\d{9}', username):
            User.USERNAME_FIELD = 'mobile'
        else:
            User.USERNAME_FIELD = 'username'
        # 3、验证用户名和密码是否正确
        """
        方式一： User.objects.get(username=username)
        """
        # 方式二：系统提供的验证：
        from django.contrib.auth import authenticate
        """
        authenticate 传递用户名和密码
        如果正确，返回user信息
        不正确，返回None
        """
        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({'code': 400, 'errmsg': '账号或密码错误'})
        # 4、session
        from django.contrib.auth import login
        login(request, user)
        # 5、判断是否记住登录
        if remembered:
            # 记住登录 默认为None的话就是两个周
            request.session.set_expiry(None)
        else:
            # 不记住登录，浏览器关闭，session过期
            request.session.set_expiry(0)
        # 6、返回响应
        """
        这里为了减少网络通讯实现登录信息获取，我们把username存到cookie，让前端从cookie中获取username显示用户信息
        """
        response = JsonResponse({'code': 200, 'errmsg': 'ok'})
        response.set_cookie('username', username)
        return response
