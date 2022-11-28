# 生产者 任务 -> 函数
# 1、这个函数，必须要让celery的实例的 task装饰器 装饰
# 2、需要celery自动检测指定包的任务

from ronglian_sms_sdk import SmsSDK
from celery_tasks.main import app

@app.task
def celery_send_sms_code(tid, mobile, datas, sdk):
    sdk.sendMessage(tid, mobile, datas)