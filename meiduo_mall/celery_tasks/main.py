"""
1、生产者
2、消费者
3、队列（中间人、经纪人）
Celery --- 将这三者实现
"""
# 0、为celery的运行创建django环境
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meiduo_mall.settings')
# 1、创建celery实例
from celery import Celery
app = Celery('celery_tasks')

# 2、设置broker
"""
这里我们通过加载配置文件来设置broker
"""
app.config_from_object('celery_tasks.config')

# 3、需要celery 自动检测指定包的任务
"""
autodiscover_tasks 参数是列表
列表中的元素是 tasks的路径
"""
app.autodiscover_tasks(['celery_tasks.sms'])

