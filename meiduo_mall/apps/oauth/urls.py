from django.urls import path
from apps.oauth.views import QQLoginURLView, QuathQQView

urlpatterns = [
    # QQ登录
    path('qq/authorization/', QQLoginURLView.as_view()),
    path('oauth_callback/', QuathQQView.as_view())
]
