from django.urls import path
from apps.verifications.views import ImageCodeView, SmsCodeView

urlpatterns = [
    # 判断用户名是否重复
    path('image_codes/<uuid>/', ImageCodeView.as_view()),
    # 短信验证码
    path('sms_codes/<mobile>/', SmsCodeView.as_view()),
]