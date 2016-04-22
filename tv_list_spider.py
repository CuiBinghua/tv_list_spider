#!/usr/bin/env python
# encoding: utf-8

# --------------------------------------------
# Author: CuiBinghua <i_chips@qq.com>
# Date: 2016-04-22 13:30:00
# --------------------------------------------

"""tv_list_spider.py是一个简单的爬虫，可以根据关键字抓取感兴趣的中文电视节目表，并定时发送到指定邮箱（默认每周抓取两次数据）。  
   tv_list_spider.py is a simple crawler. You can grab Chinese television programs by keywords, and the results will be sent to specified mailbox (twice a week by default).
"""

# 把str编码由ascii改为utf8（或gb18030）
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import time
from bs4 import BeautifulSoup
import smtplib
import ConfigParser
import codecs 
from email.message import Message
from threading import Timer
from selenium import webdriver
import requests

requests.adapters.DEFAULT_RETRIES = 10

class tv_list_spider:
    def __init__(self):
        self.conf = ConfigParser.RawConfigParser()
        self.conf.readfp(codecs.open("tv_list_spider.conf", "r", "utf-8"))
        self.program_type = self.conf.get("program", "type")
        self.program_tags = self._str2list(self.conf.get("program", "tags"))
        self.program_exclude_tags = self._str2list(self.conf.get("program", "exclude_tags"))
        self.program_range = u"本周一到本周天"
        self.ch_url = ["CCTV-CCTV5", "CCTV-CCTV5-PLUS",
                       "BTV-BTV1", "SHHAI-DONGFANG1", "TJTV-TJTV1", "CCQTV-CCQTV1",
                       "GDTV-GDTV1", "GUANXI-GUANXI1", "FJTV-FJTV2", "TCTC-TCTC1", "ZJTV-ZJTV1", "JSTV-JSTV1", "JXTV-JXTV1",
                       "SDTV-SDTV1", "SXTV-SXTV1", "SHXITV-SHXITV1", "LNTV-LNTV1", "JILIN-JILIN1", "HLJTV-HLJTV1",
                       "AHTV-AHTV1", "HUNANTV-HUNANTV1", "HUBEI-HUBEI1", "HNTV-HNTV1", "HEBEI-HEBEI1", "SCTV-SCTV1", "YNTV-YNTV1", "GUIZOUTV-GUIZOUTV1",
                       "XJTV-XJTV1", "XIZANGTV-XIZANGTV2", "QHTV-QHTV1", "GSTV-GSTV1", "NXTV-NXTV2", "NMGTV-NMGTV1"] # m.tvmao.com只认大写，不认小写
        self.file_content = ""
        self.file_name = "tv_list.txt"
        self.week_dict = {1 : "星期一", 2 : "星期二", 3 : "星期三", 4 : "星期四", 5 : "星期五", 6 : "星期六", 7 : "星期天"}
        self.timer_interval = 3600 * 24 * 7 / 2 # 每周抓取两次数据
        self.search_len = 60
        self.split_line = "--------------------------------------------------------------------------------------------------------\n"

    def _str2list(self, str):
        """将字符串的所有空格都去掉之后再转成列表（如果不是有效字符串，则直接转换为空列表）"""
        if str is None:
            return []
        str = str.replace(' ', '')
        if str == "":
            return []
        return str.split(',')

    def do_spider_get_header(self):
        return u"\n★ 抓取时间：" + time.strftime("%Y年%m月%d日%H时%M分%S秒", time.localtime()) + u"\n★ 抓取范围：" + self.program_range + "\n★ 抓取类型：" + self.program_type + "\n\n\n"
	
    def do_spider_get_program_item(self, program_item, tv_weekday):
        time_program = program_item.text.strip().replace('\n', '')
        tv_item = tv_weekday + time_program[:5] + "\t" + time_program[5:]
        self.file_content += "★ " + tv_item + "\n"
        print tv_item

    def do_spider_check_tag(self, program_list, tv_weekday):
        if program_list is None:
            return

        for i in program_list:
            bExclude = False
            if self.program_exclude_tags != []:
                for j in self.program_exclude_tags:
                    if i.text.find(j, 0, self.search_len) != -1:
                        bExclude = True
                        break
            if bExclude:
                continue

            if self.program_tags == []: # 如果没有要抓取的标签, 则抓取所有数据
                self.do_spider_get_program_item(i, tv_weekday)
            else:
                for k in self.program_tags:
                    if i.text.find(k, 0, self.search_len) != -1:
                        self.do_spider_get_program_item(i, tv_weekday)
                        break

    def do_request(self, url):
        headers = {"User-Agent" : "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"}
        headers_bak = {"User-Agent" : "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)"}
        source_code = None

        try:
            source_code = requests.get(url, headers = headers)
        except Exception as e:
            print "请求报错："
            print e
            time.sleep(10)
            try:
                source_code = requests.get(url, headers = headers_bak)
            except Exception as e:
                print "再次请求报错："
                print e
            else:
                print "再次请求，成功！"
        finally:
		    return source_code

    def do_soup_baitv(self, url):
        source_code = self.do_request(url)
        if source_code is not None:
            plain_text = source_code.text
            soup = BeautifulSoup(plain_text, "lxml")
            if soup.find('div', {"class" : "schedule-header"}) is not None:
                return soup
        return None

    def do_spider_baitv(self):
        """抓取www.baitv.com的电视节目信息
           优点：① 静态网页，抓取轻便！
           缺点：① 该网站提供的节目表不全！② 抓取网页偶尔失败！
        """
        print "准备开始抓取..."
        self.file_content += self.do_spider_get_header()

        for i in range(1, 8):
            for c in self.ch_url:
                url = "http://www.baitv.com/program/" + c + "-w" + str(i) + ".html"
                print "正在抓取：" + url
                soup = self.do_soup_baitv(url)
                if soup is None:
                    print url + "信息抓取失败！"
                    time.sleep(10)
                    soup = self.do_soup_baitv(url)
                    if (soup is None):
                        print url + "信息抓取再次失败！"
                        continue
           
                program_list = soup.find(attrs = {"class" : "schedule-list"})
                if program_list is None:
                    print url + "暂无节目列表！"
                    continue

                tv = soup.find('div', {"class" : "schedule-header"}).find("h1").text
                tv_weekday = self.week_dict.get(i, "？？？") + "\t" + tv + "\t"         
                program_list = program_list.find_all("li")
                self.do_spider_check_tag(program_list, tv_weekday)
            self.file_content += self.split_line

    def do_soup_tvmao(self, url):
        self.browser.get(url)
        plain_text = self.browser.page_source
        soup = BeautifulSoup(plain_text, "lxml")
        if soup.find('div', {"class" : "pgmain"}) is not None:
            return soup
        return None

    def do_spider_tvmao(self):
        """抓取www.tvmao.com的电视节目信息
           优点：① 该网站提供的节目表相对完整！
           缺点：① 动态网页，抓取复杂！
        """
        print "准备开始抓取..."
        self.file_content += self.do_spider_get_header()
        self.browser = webdriver.Firefox()

        for i in range(1, 8):
            for c in self.ch_url:
                url = "http://www.tvmao.com/program/" + c + "-w" + str(i) + ".html"
                print "正在抓取：" + url
                soup = self.do_soup_tvmao(url)
                if soup is None:
                    print url + "信息抓取失败！"
                    time.sleep(10)
                    soup = self.do_soup_tvmao(url)
                    if (soup is None):
                        print url + "信息抓取再次失败！"
                        continue

                program_info = soup.find(attrs = {"class" : "epg mt10 mb10"})
                if program_info is None:
                    print url + "暂无节目列表！"
                    continue

                tv = soup.find('div', {"class" : "pgmain"}).find("h1").text
                tv_weekday = self.week_dict.get(i, "？？？") + "\t" + tv + "\t"
                program_list = program_info.find_all("li")
                self.do_spider_check_tag(program_list, tv_weekday)
            self.file_content += self.split_line
        self.browser.quit()

    def do_soup_m_tvmao(self, url):
        plain_text = None
        try:
            self.browser.get(url)
            plain_text = self.browser.page_source
        except Exception as e:
            print "请求报错："
            print e
            return None

        soup = BeautifulSoup(plain_text, "lxml")
        if soup.find('div', {"class" : "clear blank mt10 mb10"}) is not None:
            return soup
        return None

    def do_spider_m_tvmao(self):
        """抓取m.tvmao.com的电视节目信息
           优点：① 该网站提供的节目表相对完整！② 手机版冗余信息少很多！
           缺点：① 动态网页，抓取复杂！② 抓取网页有时不完整！
        """
        print "准备开始抓取..."
        self.file_content += self.do_spider_get_header()
        self.browser = webdriver.Firefox()

        for i in range(1, 8):
            for c in self.ch_url:
                url = "http://m.tvmao.com/program/" + c + "-w" + str(i) + ".html"
                print "正在抓取：" + url
                soup = self.do_soup_m_tvmao(url)
                if soup is None:
                    print url + "信息抓取失败！"
                    time.sleep(10)
                    soup = self.do_soup_m_tvmao(url)
                    if (soup is None):
                        print url + "信息抓取再次失败！"
                        continue

                program_info = soup.find(attrs = {"class" : "timeline clear blank"})
                if program_info is None:
                    print url + "暂无节目列表！"
                    continue

                tv = soup.find('div', {"class" : "lt mr5 mt5"}).text
                tv = tv[tv.find("-") + 1:].strip('\n')
                tv_weekday = self.week_dict.get(i, "？？？") + "\t" + tv + "\t"
                program_list = program_info.find_all("tr")
                self.do_spider_check_tag(program_list, tv_weekday)
            self.file_content += self.split_line
        self.browser.quit()

    def do_write(self):
        """将最终结果追加写入文件"""
        print "正在将抓取信息写入到文件%s中..." % self.file_name
        f = open(self.file_name, 'a')
        f.write(self.file_content)
        f.close()
        print "抓取完毕，请到文件%s中查看抓取信息..." % self.file_name

    def do_check_email_conf(self, smtpserver, username, password, from_addr, to_and_cc_addr):
        if smtpserver == "":
            print "发送邮件失败！请在配置文件tv_list_spider.conf中为smtpserver配置正确参数！"
            return False
        if username == "":
            print "发送邮件失败！请在配置文件tv_list_spider.conf中为username配置正确参数！"
            return False
        if password == "":
            print "发送邮件失败！请在配置文件tv_list_spider.conf中为password配置正确参数！"
            return False
        if from_addr == "":
            print "发送邮件失败！请在配置文件tv_list_spider.conf中为from配置正确参数！"
            return False
        if to_and_cc_addr == []:
            print "发送邮件失败！请在配置文件tv_list_spider.conf中为to或者cc配置正确参数！"
            return False
        return True
		
    def do_email(self):
        """将最终结果以邮件形式发送"""
        print "准备发送邮件..."
        from_addr = self.conf.get("addr", "from")
        to_addr = self.conf.get("addr", "to")
        cc_addr = self.conf.get("addr", "cc")
        smtpserver = self.conf.get("mail", "smtpserver")
        username = self.conf.get("mail", "username")
        password = self.conf.get("mail", "password")
        to_and_cc_addr = self._str2list(to_addr) + self._str2list(cc_addr)
        if self.do_check_email_conf(smtpserver, username, password, from_addr, to_and_cc_addr) is not True:
            return
        subject = self.program_range + self.program_type + time.strftime("（发送时间：%Y年%m月%d日）", time.localtime())
        message = Message()
        message["Subject"] = subject
        message["From"] = from_addr
        message["To"] = to_addr
        message["Cc"] = cc_addr
        message.set_payload(self.file_content)
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver)
        smtp.login(username, password)  
        smtp.sendmail(from_addr, to_and_cc_addr, message.as_string())
        smtp.quit()
        print "发送完毕，请到邮箱中查看抓取信息..."

    def clean(self):
        self.file_content = ""

    def start(self):
        """万一哪天tvmao.com和baitv.com都挂了，还可以考虑去抓取tvsou.com等网站的信息"""
        # self.do_spider_baitv()
        # self.do_spider_m_tvmao()
        self.do_spider_tvmao()
        self.do_write()
        self.do_email()
        self.clean()
        t = Timer(self.timer_interval, self.start)  
        t.start()

if __name__ == "__main__":
    mySpider = tv_list_spider()
    mySpider.start()