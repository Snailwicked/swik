import psutil

''''
获取cpu信息
'''
a = psutil.cpu_times()  # 使用cpu_times方法获取cpu完成信息，需要显示所有的cpu信息
b = psutil.cpu_times().user  # 获取单项cpu的数据信息，如用户user的cpu时间比
c = psutil.cpu_count()  # 获取cpu的逻辑个数

print(a)
print(b)
print(c)

'''
内存信息
'''
mem = psutil.virtual_memory()  # 使用pstuil.virtual_memory方法获取内存的完整信息
mem_total = psutil.virtual_memory().total  # 获取内存总数
mem_free = psutil.virtual_memory().free  # 获取内存剩余
print(mem)
print(mem_total)
print(mem_free)

'''
磁盘信息
'''
disk_partitions = psutil.disk_partitions()  # 获取磁盘完整信息
disk_usage = psutil.disk_usage('/')  # 获取整个硬盘的信息
disk_usage_c = psutil.disk_usage('C://')  # 获取分区c的硬盘信息
disk_io = psutil.disk_io_counters()  # 获取硬盘的总io个数、读写信息
disk_io_perdisk = psutil.disk_io_counters(perdisk=True)  # ‘perdisk=True'参数获取单个分区IO个数、读写信息
print(disk_partitions)
print(disk_usage)
print(disk_usage_c)
print('硬盘总io=' + str(disk_io))
print('单个分区信息=' + str(disk_io_perdisk))

'''
网络信息
'''
net_io = psutil.net_io_counters()  # 获取网络总IO信息、默认pernic=False
net_io_pernic = psutil.net_io_counters(pernic=True)  # 获取每个网卡的io信息
net_connections = psutil.net_connections()  # 获取所有的连接信息
print(net_io)
print(net_io_pernic)
print(net_connections)

'''
其他系统信息
'''
users = psutil.users()  # 当前登录系统的用户信息
import datetime

boot_time = psutil.boot_time()  # 获取开机时间,为linux格式
boot_time_nu = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d%H:%M:%S')  # 转换为自然格式
print(users)
print(boot_time)
print(boot_time_nu)