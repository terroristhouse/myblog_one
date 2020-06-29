import pymysql
import requests
import time,sys,os
from lxml import etree
import json
from datetime import datetime
import html
import logging

# 声明一个logger对象
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
# windows启用
# handler = logging.FileHandler('error.log',encoding='utf-8')
# linux启用
handler = logging.FileHandler('/data/rizhi/wangyi_error.log',encoding='utf-8')

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(lineno)d - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)



def robust(actual_do):
    def add_robust(*args, **keyargs):
        try:
            return actual_do(*args, **keyargs)
        except Exception as e:
            logger.error(actual_do.__name__ + ':' + str(e), exc_info=True)
    return add_robust





class Wyxw:
    @robust
    def __init__(self):
        # 连接数据库
        self.conn = pymysql.connect(host="127.0.0.1", user="root", password="root", database="blog_lf", charset="utf8",port=3306)
        self.start_time = time.time()
        self.cursor = self.conn.cursor()
        self.index_url = 'https://news.163.com/'
        self.today_time = datetime.now().date()
        self.list_mail = []
        self.old_urls = self.search_server()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36",
            # 'cookie': 's_n_f_l_n3 = c276f23cba15490e1586652098498;vinfo_n_f_l_n3 = c276f23cba15490e.1.0.1586652098460.0.1586652102247',
        }

    # 获取到列表页的url
    def get_index(self,url):
        response =  requests.get(url=url,headers=self.headers)
        result = etree.HTML(response.text)
        li_lists = result.xpath('//div[@class="ns_area list"]/ul/li[@class]')
        for li_list in li_lists:
            list_urls = li_list.xpath('./a/@href')[0]
            list_name = li_list.xpath('./a/text()')[0]
            if list_name == '首页' or list_name == '王三三':
                continue
            print(list_urls)
            # 国内
            if list_urls == 'http://news.163.com/domestic/':
                for i in range(3):
                    if i == 0:
                        list_url = 'https://temp.163.com/special/00804KVA/cm_guonei.js?callback=data_callback'
                        res = self.get_list(list_url,sort_id='国内')
                        if res:
                            break
                    else:
                        list_url = 'https://temp.163.com/special/00804KVA/cm_guonei_0{}.js?callback=data_callback'.format(i+1)
                        res = self.get_list(list_url,sort_id='国内')
                        if res:
                            break
            # 国际
            elif list_urls == 'http://news.163.com/world/':
                for i in range(3):
                    if i == 0:
                        list_url = 'https://temp.163.com/special/00804KVA/cm_guoji.js?callback=data_callback'
                        res = self.get_list(list_url,sort_id='国际')
                        if res:
                            break
                    else:
                        list_url = 'https://temp.163.com/special/00804KVA/cm_guoji_0{}.js?callback=data_callback'.format(i+1)
                        res = self.get_list(list_url,sort_id='国际')
                        if res:
                            break
            # 军事
            elif list_urls == 'http://war.163.com/':
                for i in range(3):
                    if i == 0:
                        list_url = 'https://temp.163.com/special/00804KVA/cm_war.js?callback=data_callback'
                        res = self.get_list(list_url,sort_id='军事')
                        if res:
                            break
                    else:
                        list_url = 'https://temp.163.com/special/00804KVA/cm_war_0{}.js?callback=data_callback'.format(i+1)
                        res = self.get_list(list_url,sort_id='军事')
                        if res:
                            break
            # 航空
            elif list_urls == 'http://news.163.com/air/':
                for i in range(3):
                    if i == 0:
                        list_url = 'https://temp.163.com/special/00804KVA/cm_hangkong.js?callback=data_callback&a=2'
                        res = self.get_list(list_url,sort_id='航空')
                        if res:
                            break
                    else:
                        list_url = 'https://temp.163.com/special/00804KVA/cm_hangkong_0{}.js?callback=data_callback&a=2'.format(i+1)
                        res = self.get_list(list_url,sort_id='航空')
                        if res:
                            break
            # 无人机
            elif list_urls == 'http://news.163.com/uav/':
                for i in range(3):
                    if i == 0:
                        list_url = 'https://news.163.com/uav/special/000189N0/uav_index.js?callback=data_callback'
                        res = self.get_list(list_url,sort_id='无人机')
                        if res:
                            break
                    else:
                        list_url = 'https://news.163.com/uav/special/000189N0/uav_index_0{}.js?callback=data_callback'.format(i+1)
                        res = self.get_list(list_url,sort_id='无人机')
                        if res:
                            break

    # 获取到详情页的url
    @robust
    def get_list(self,list_url,sort_id):
        response = requests.get(url=list_url, headers=self.headers)
        result = response.text.lstrip('data_callback(').rstrip(')')
        res = json.loads(result)
        for r in res:
            old_times = r['time'].split(' ')[0].split('/')
            old_time = datetime(int(old_times[2]), int(old_times[0]), int(old_times[1])).date()
            if old_time != self.today_time:
                return True
            if r['docurl'] in self.old_urls:
                print('数据已入库')
                continue
            self.get_detail(detail_url=r['docurl'],sort_id=sort_id)

    # 获取文章详情
    @robust
    def get_detail(self,detail_url,sort_id):
        time.sleep(3)
        response = requests.get(url=detail_url,headers=self.headers)
        result = etree.HTML(response.text)
        publishtime = str(self.today_time)
        title = result.xpath('//div[@class="post_content_main"]/h1/text()')
        if title:
            title = title[0].replace('「', '“').replace('」', '”')
        URL = detail_url
        UniqURL = detail_url
        LASTUPDATE = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        ENCODING = 'big5-hkscs'
        SITE = 5
        CATEGORYCODE = '0'
        PARENTID = -1
        PAGETITLES = result.xpath('//title/text()')
        PAGETITLE = ''
        if PAGETITLES:
            PAGETITLE = PAGETITLES[0]
        CANBEPUBLISHED = 1
        NETRESOURCETYPE = 256
        HTMLCONTENT = ''
        authorID = ''
        sort2_ID = sort_id
        source = '网易新闻'
        content_lists = result.xpath('//div[@class="post_text"]//p/text()')
        content = ''
        for content_list in content_lists:
            # content += '　　' + content_list.xpath('string(.)').replace('「', '“').replace('」','”').strip() + '\n\n'
            content += '　　' + content_list.replace('「', '“').replace('」', '”').strip() + '\n\n'
        content = content.replace('\u3000','')
        lang = 'TC'
        standbyIDS = result.xpath('//div[@class="post_text"]//p/img')
        standbyID = []
        try:
            for standbyID_1 in standbyIDS:
                standbyID_2 = standbyID_1.xpath('./@src | ./@alt')
                if standbyID_2:
                    standbyID.append((standbyID_2[0],standbyID_2[1]))
        except Exception as e:
            pass
        standbyID = str(standbyID)
        zoneID = '大陆>'
        columnID = '新闻>综合'
        data_result = [(URL, title, sort2_ID,standbyID,content, publishtime, LASTUPDATE,HTMLCONTENT, authorID, UniqURL, ENCODING, SITE,CATEGORYCODE,PARENTID,PAGETITLE, CANBEPUBLISHED, NETRESOURCETYPE, source, lang, zoneID,columnID),]
        # print(data_result)
        self.insert_server(data_result)

    # 写入数据库
    @robust
    def insert_server(self,data):
        sql = "INSERT INTO blog_crawler_02(URL, title,sort2_ID,standbyID,content,publishtime,LASTUPDATE,HTMLCONTENT,authorID,UniqURL,ENCODING,SITE,CATEGORYCODE,PARENTID,PAGETITLE,CANBEPUBLISHED,NETRESOURCETYPE,source,lang,zoneID,columnID) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.cursor.executemany(sql, data)
        self.conn.commit()
        self.list_mail.append(data[0][1])
        print('正在入库：', data[0][1],data[0][5])


    # 查询去重
    @robust
    def search_server(self):
        old_url = []
        search_sql = "select URL from blog_crawler_02 where publishtime='%s'" %self.today_time
        self.cursor.execute(search_sql)
        for i in self.cursor.fetchall():
            old_url.append(i[0])
        # print(old_url)
        return old_url

    def run(self):
        self.get_index(self.index_url)
        self.write_log()
    # 析构方法
    def __del__(self):
        self.cursor.close()
        self.conn.close()

    # 写入日志
    @robust
    def write_log(self):
        cha = time.time()-self.start_time
        # with open('wangyi.txt', 'a+', encoding='utf-8') as f:
        #     f.write(str(datetime.now()) + ' 下载数量：%s' % len(self.list_mail) + '用时:%s'%cha + '\n')
        # linux启用
        with open('/data/rizhi/wangyi.txt', 'a+', encoding='utf-8') as f:
            f.write(str(datetime.now()) + ' 下载数量：%s' % len(self.list_mail) + '用时:%s'%cha + '\n')


if __name__ == '__main__':
    W = Wyxw()
    W.run()


# 国内新闻
# https://temp.163.com/special/00804KVA/cm_guonei_02.js?callback=data_callback
# https://temp.163.com/special/00804KVA/cm_guonei_03.js?callback=data_callback

# 国际
# https://temp.163.com/special/00804KVA/cm_guoji.js?callback=data_callback

# 航空
# https://temp.163.com/special/00804KVA/cm_hangkong_02.js?callback=data_callback&a=2

# 军事
# https://temp.163.com/special/00804KVA/cm_war_02.js?callback=data_callback

# 无人机
# https://news.163.com/uav/special/000189N0/uav_index_02.js?callback=data_callback
# https://news.163.com/uav/special/000189N0/uav_index_03.js?callback=data_callback
