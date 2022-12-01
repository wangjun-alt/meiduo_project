from django.urls import path
from apps.oauth.views import QQLoginURLView

urlpatterns = [
    # QQ登录
    path('qq/authorization/', QQLoginURLView.as_view())
]
