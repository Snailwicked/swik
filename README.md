# spider: 爬虫管理系统

    
## 项目介绍

        爬虫管理系统是一套对服务器资源进行合理分配的分布式数据采集WEB系统,其中包含网页管理、爬虫管理、数据监控等模块，各模块
    
    间相互关联，组建一个多服务器相互协作的系统，让你仅通过简单的配置信息就能够搭建一个属于自己的数据采集系统。
        
       
## celery

        在运行项目之前，需启动任务队列，启动代码如下：
        celery -A tasks.workers.app worker -l info -P eventlet
        
## 项目展示
### 网址列表
        在网址列表中你可以添加一个需要采集的的目标网站，系统会为你自动生成一系列的默认配置信息，在新闻数据采集中，内部包含一
    套算法采集，让你不需要配置任何信息便可获取目标新闻数据，但采集精度有限，如果需要精确数据可在采集字段中设置xpath路径，css
    路径或正则表达式。
    
        在配置信息你可以设置此网站要采集的深度（默认深度为1，默认采集当前网址数据），也可以根据网址的正则进行过滤网址，获取目
    标网址。
    
        在设置了配置信息之后，你可以点击监测按钮，查看配置信息是否生效，系统会默认先读取输入的选择器信息进行精准定位获取数据，
     在未获取到数据或没有选择器的时候系统启动算法采集模式，
![Image text](https://raw.githubusercontent.com/Snailwicked/spider_manage/master/images/weblist.png)

![Image text](https://raw.githubusercontent.com/Snailwicked/spider_manage/master/images/config.png)

### 爬虫列表
        在爬虫列表中你可以新建一个数据采集引擎，新建的采集引擎为空，只需要导入网址列表中配置好的网站便可启动采集引擎，启动的采集
    引擎将目标网址存入任务队列，后台从任务队列中获取任务进而解析数据保存到数据库中，你也可以通过配置信息指定数据采集任务由哪台服
    务器执行，系统默认本机运行解析代码。
    
        引擎启动之后，引擎状态随之改变，结束之后恢复状态，你也可以手动终止任务，重启任务，或定时采集该爬虫引擎，引擎中含有采集
    任务无法删除引擎，如需销毁引擎，提前移除引擎内采集任务即可。

![Image text](https://raw.githubusercontent.com/Snailwicked/spider_manage/master/images/spider_engine.png)
![Image text](https://raw.githubusercontent.com/Snailwicked/spider_manage/master/images/import.png)

### 系统监控
![Image text](https://raw.githubusercontent.com/Snailwicked/spider_manage/master/images/monitor.png)

###数据列表
![Image text](https://raw.githubusercontent.com/Snailwicked/spider_manage/master/images/newslist.png)
![Image text](https://raw.githubusercontent.com/Snailwicked/spider_manage/master/images/detailed.png)
## 相关技术

- flask
- mysql
- redis
- celey
