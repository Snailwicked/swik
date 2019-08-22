import psutil

''''
获取cpu信息
'''

class System():

    def infos(self):

        '''cpu 信息'''
        cpu = {}
        cpu["cpu_count"] = psutil.cpu_count()  # 获取cpu的逻辑个数
        cpu["cpu_percent"] = psutil.cpu_percent()  # 获取cpu利用率

        '''
        内存信息
        '''
        memory = {}
        memory["total"]= psutil.virtual_memory().total
        memory["free"]= psutil.virtual_memory().free
        memory["percent"]= psutil.virtual_memory().percent

        #
        # '''
        # 磁盘信息
        # '''
        disk = {}
        disk_usage = psutil.disk_usage('/')  # 获取整个硬盘的信息
        disk["total"] = disk_usage.total
        disk["free"] = disk_usage.free
        disk["percent"] = disk_usage.percent
        return {"cpu":cpu,"memory":memory,"disk":disk}

if __name__ == '__main__':
    system = System()
    print(system.infos())