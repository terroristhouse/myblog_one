import requests
from lxml import etree
import pymysql
import logging
import time
from datetime import datetime
# 声明一个logger对象
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
# windows启用
# handler = logging.FileHandler('error.log',encoding='utf-8')
# linux启用
handler = logging.FileHandler('/data/rizhi/wodebokeyuan_error.log',encoding='utf-8')
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


class Bokeyuan:
    def __init__(self):
        self.start_time = time.time()
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', db='blog_lf', charset='utf8mb4')
        self.cursor = self.conn.cursor()
        self.search_result = self.search_result()
        self.list_mail = []

    # 获取列表页-详情页url
    def get_index(self):
        for i in range(1,7):
            lists_url = 'https://www.cnblogs.com/nmsghgnv/default.html?page=%s'%i
            response = requests.get(lists_url)
            result = etree.HTML(response.text)
            detail_urls = result.xpath('//a[@class="postTitle2"]')
            for d in detail_urls:
                detail_url = d.xpath('./@href')[0]
                if detail_url in self.search_result:
                    print('数据已入库')
                    continue
                self.get_detail(detail_url)

    # 获取文章内容
    def get_detail(self,url):
        response = requests.get(url)
        result = etree.HTML(response.text)
        # 标题
        title = result.xpath('//a[@id="cb_post_title_url"]/text()')[0]
        # 内容
        content = ''
        contents = result.xpath('//div[@id="cnblogs_post_body"]//p/text()|//div[@id="cnblogs_post_body"]//a/text()|//div[@id="cnblogs_post_body"]//img/@src')
        for c in contents:
            content += '　　' +  c  + '\n\n'
        # 图片
        standbyID = ''
        standbyIDs = result.xpath('//div[@id="cnblogs_post_body"]//img/@src')
        if standbyIDs:
            standbyID = standbyIDs[0]

        # 创建时间
        publishtime = result.xpath('//span[@id="post-date"]/text()')
        if publishtime:
            publishtime = publishtime[0]
        # 来源
        source = '我的博客园'
        data = [url,title,content,content,source,0,1,1,publishtime,publishtime]
        self.insert_mysql(data)

    # 写入数据库
    def insert_mysql(self,data):
        sql = "INSERT INTO blog_article(url,title,excerpt,body,source,views,category_id,user_id,created_time,modified_time) VALUES (%s,%s, %s,%s,%s,%s, %s,%s, %s,%s);"
        self.cursor.execute(sql, data)
        print('正在写入：',data[0])
        # 提交事务
        self.conn.commit()

    # 查询去重
    def search_result(self):
        search_sql = "select URL from blog_article"
        self.cursor.execute(search_sql)
        search = []
        for url in self.cursor.fetchall():
            search.append(url[0])
        return search

    # 启动函数
    def run(self):
        self.get_index()
        self.write_log()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    # 写入日志
    @robust
    def write_log(self):
        cha = time.time() - self.start_time
        # with open('wangyi.txt', 'a+', encoding='utf-8') as f:
        #     f.write(str(datetime.now()) + ' 下载数量：%s' % len(self.list_mail) + '用时:%s'%cha + '\n')
        # linux启用
        with open('/data/rizhi/wodebokeyuan.txt', 'a+', encoding='utf-8') as f:
            f.write(str(datetime.now()) + ' 下载数量：%s' % len(self.list_mail) + '用时:%s' % cha + '\n')

if __name__ == '__main__':
    B = Bokeyuan()
    B.run()







