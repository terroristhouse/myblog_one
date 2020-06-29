import pymysql

conn = pymysql.connect(host='localhost',user='root',password='root',database='blog_lf',charset='utf8mb4')
cursor = conn.cursor()
data_list = []
search_sql = 'select URL,title,publishtime,publishtime,source,content,CATEGORYCODE,content,sort2_ID from blog_crawler_02'

cursor.execute(search_sql)
data = cursor.fetchall()

insert_sql = 'insert into blog_article(url,title,created_time,modified_time,source,body,views,excerpt,sort2_ID) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'

cursor.executemany(insert_sql,data)
conn.commit()
# 清空表
truncate_sql = 'truncate table blog_crawler_02'
cursor.execute(truncate_sql)
conn.commit()

conn.close()


