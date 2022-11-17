from django.urls import path
from apps.verifications.views import ImageCodeView

urlpatterns = [
    # 判断用户名是否重复
    path('image_codes/<uuid>/', ImageCodeView.as_view()),
]