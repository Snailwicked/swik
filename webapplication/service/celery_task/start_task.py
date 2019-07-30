from webapplication.service.celery_task.task_spider import add #导入我们的任务函数add
import time
result = add.delay(12,12) #异步调用，这一步不会阻塞，程序会立即往下运行

while not result.ready():# 循环检查任务是否执行完毕
    print(time.strftime("%H:%M:%S"))
    time.sleep(1)

print(result.get()) #获取任务的返回结果
print(result.successful()) #判断任务是否成功执行