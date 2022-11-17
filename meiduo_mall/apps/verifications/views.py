from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from captcha.captcha import captcha
from django_redis import get_redis_connection

# Create your views here.
class ImageCodeView(View):
    def get(self, request, uuid):
        text, image = captcha.generate_captcha()
        redis_cli = get_redis_connection('image_code')
        redis_cli.setex(uuid, 100, text)
        return HttpResponse(image, content_type='image/png')