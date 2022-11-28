from django.test import TestCase

# Create your tests here.
from ronglian_sms_sdk import SmsSDK

accId = '8aaf0708842397dd0184b91dbc943559'
accToken = 'c042a8b512024bc2a3970ce0119988e1'
appId = '8aaf0708842397dd0184b91dbd8b3560'


def send_message():
    sdk = SmsSDK(accId, accToken, appId)
    tid = '1'
    mobile = '18392119861'
    datas = (312413, 5)
    resp = sdk.sendMessage(tid, mobile, datas)
    print(resp)
send_message()