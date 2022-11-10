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
        return JsonResponse({'code': 200, 'count': count, 'ermsg': 'ok'})
