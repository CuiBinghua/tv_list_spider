# 1. ���
tv_list_spider.py��һ���򵥵����棬���Ը��ݹؼ���ץȡ����Ȥ�����ĵ��ӽ�Ŀ������ʱ���͵�ָ�����䣨Ĭ��ÿ��ץȡ�������ݣ���  
tv_list_spider.py is a simple crawler. You can grab Chinese television programs by keywords, and the results will be sent to specified mailbox (twice a week by default).  

# 2. ����
����ʹ�õ�CentOS 6��Python�汾Ϊ��2.6.6��  
��Ҫ��װ��Ҫ��Python�����  
$ yum install -y python-setuptools  
$ easy_install requests beautifulsoup4  
���⣬Ϊ��ʵ��ץȡ��̬��ҳ������Ҫ��װ���²����  
$ easy_install selenium  
$ yum install -y firefox xorg-x11-server-Xvfb  

# 3. ����
ע�⣬tv_list_spider.conf��������ļ���Ҫ��UTF-8�����ʽ���档  
��[program]��һ���У�  
type��ʾ�Զ����Ŀ���ͣ�  
tags��ʾ����Ȥ�ı�ǩ�������ǩ֮���Զ��ż�������tagsΪ�գ���ץȡ�������ݣ���  
exclude_tags��ʾ������Ȥ�ı�ǩ�����ȼ�����tags���������ǩ֮���Զ��ż�������exclude_tagsΪ�գ��򲻻��ų��κ����ݣ���  
��[mail]��һ���У�  
smtpserver��ʾ���������SMTP��������ַ����Ҫ�������ã�������  
username��ʾ����������û�������Ҫ�������ã�������  
password��ʾ������������루��Ҫ�������ã�������  
��[addr]��һ���У�  
from��ʾ��������ĵ�ַ������Ҫ��һ����Ч��ַ��������  
to��ʾ��������ĵ�ַ����������ַ֮���Զ��ż����to��cc����������Ҫ��һ����Ч��ַ��������  
cc��ʾ��������ĵ�ַ����������ַ֮���Զ��ż����to��cc����������Ҫ��һ����Ч��ַ��������  

# 4. ����
�����������  
$ sh start.sh  
ֹͣ�������  
$ sh stop.sh  
�鿴�����־��  
$ tailf spider.log  
�鿴����ļ���  
$ cat tv_list.txt  


# 5. �ο�����
http://plough-man.com/?p=379  
https://github.com/SongJLG/TVPL_Spider/blob/master/spicode/TVPLSpider.py
