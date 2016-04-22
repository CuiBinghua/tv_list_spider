# 1. 简介
tv_list_spider.py是一个简单的爬虫，可以根据关键字抓取感兴趣的中文电视节目表，并定时发送到指定邮箱（默认每周抓取两次数据）。  
tv_list_spider.py is a simple crawler. You can grab Chinese television programs by keywords, and the results will be sent to specified mailbox (twice a week by default).  

# 2. 环境
本人使用的CentOS 6，Python版本为：2.6.6。  
需要安装必要的Python插件：  
$ yum install -y python-setuptools  
$ easy_install requests beautifulsoup4  
另外，为了实现抓取动态网页，还需要安装以下插件：  
$ easy_install selenium  
$ yum install -y firefox xorg-x11-server-Xvfb  

# 3. 配置
注意，tv_list_spider.conf这个配置文件需要以UTF-8编码格式保存。  
在[program]这一段中：  
type表示自定义节目类型；  
tags表示感兴趣的标签，多个标签之间以逗号间隔（如果tags为空，则抓取所有数据）；  
exclude_tags表示不感兴趣的标签（优先级高于tags），多个标签之间以逗号间隔（如果exclude_tags为空，则不会排除任何数据）；  
在[mail]这一段中：  
smtpserver表示所用邮箱的SMTP服务器地址（需要自行设置！！！）  
username表示所用邮箱的用户名（需要自行设置！！！）  
password表示所用邮箱的密码（需要自行设置！！！）  
在[addr]这一段中：  
from表示发送邮箱的地址（必须要有一个有效地址！！！）  
to表示接收邮箱的地址，多个邮箱地址之间以逗号间隔（to或cc加起来至少要有一个有效地址！！！）  
cc表示抄送邮箱的地址，多个邮箱地址之间以逗号间隔（to或cc加起来至少要有一个有效地址！！！）  

# 4. 运行
启动爬虫服务：  
$ sh start.sh  
停止爬虫服务：  
$ sh stop.sh  
查看输出日志：  
$ tailf spider.log  
查看输出文件：  
$ cat tv_list.txt  


# 5. 参考资料
http://plough-man.com/?p=379  
https://github.com/SongJLG/TVPL_Spider/blob/master/spicode/TVPLSpider.py
