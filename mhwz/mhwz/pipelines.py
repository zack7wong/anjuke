# -*- coding: utf-8 -*-
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
# 提高程序访问数据库效率
# 每次插入后commit程序执行很慢
class MhwzPipeline():
    def open_spider(self,spider):
        database = "mhwz"
        host = "localhost"
        port = 3306
        user = "root"
        password = "mysql"
        charset = 'utf8mb4'
        self.dbpool = adbapi.ConnectionPool('pymysql',database=database,host=host,port=port,user=user,password=password,charset=charset)
        # 创建连接池对象，每个连接对象在独立的线程中工作，内部使用第一个参数-》pymysql访问数据库

    def close_spider(self,spider):
        self.dbpool.close()

    def process_item(self,item,spider):
        self.dbpool.runInteraction(self.insert_db,item)
        #以异步方式调用insert_db函数
        return item

    def insert_db(self,tx,item): # 第一个参数是Transaction对象，
        values = (
                    item['site_url'],
                    item['site_name'],
        )
        sql = " insert into mhwz (site_url,site_name) values (%s,%s) "
        tx.execute(sql, values)
        print('ok1')



# class MhwzPipeline():
#     def open_spider(self, spider):
#
#         self.db_conn = pymysql.connect(database="mhwz", host="localhost", port=3306, user="root",
#                                             password="mysql",
#                                             charset='utf8mb4')
#         self.db_cur = self.db_conn.cursor()
#
#     def close_spider(self, spider):
#         self.db_conn.commit()
#         self.db_conn.close()
#
#     def process_item(self, item, spider):
#         self.insert_db(item)#
#         return item
#
#     def insert_db(self,item):
#         values = (
#             item['site_url'],
#             item['site_name'],
#         )
#
#         sql = "insert into mhwz (site_url,site_name) values (%s,%s)"
#         self.db_cur.execute(sql, values)
#         print('ok')


# ---------------------------------------------------------------
# class MhwzPipeline():
#
#     def __init__(self):
#         self.conn = pymysql.connect(host="localhost", port=3306, database="mhwz", user="root", password="mysql",
#                                     charset='utf8mb4')
#         self.cs = self.conn.cursor()
#
#     def process_item(self, item, spider):
#         values = (
#             item['site_url'],
#             item['site_name'],
#         )
#         sql = "insert into mhwz (site_url,site_name) values (%s,%s)"
#         self.cs.execute(sql, values)
#         self.conn.commit()
#         print('save ok')
#         # return item

    