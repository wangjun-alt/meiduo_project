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
