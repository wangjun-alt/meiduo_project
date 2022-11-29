# import os
# import sys
#
# from django.test import TestCase
# from apps.users.models import User
# # Create your tests here.
# from pathlib import Path
# BASE_DIR1 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# BASE_DIR = Path(__file__).resolve().parent.parent
# print(BASE_DIR)
# print(BASE_DIR1)
# print(os.path.dirname(BASE_DIR))
# print(os.path.join(os.path.dirname(BASE_DIR)))
#
# count = User.objects.all()
# print(count)
import re
username = input()
if re.match('1[3-9]\d{9}', username):
    print('true')
else:
    print('false')