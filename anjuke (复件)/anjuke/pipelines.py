# -*- coding: utf-8 -*-
from twisted.enterprise import adbapi

class AnjukePipeline():
    def open_spider(self, spider):
        database = "data"
        host = "localhost"
        port = 3306
        user = "root"
        password = "mysql"
        charset = 'utf8mb4'
        self.dbpool = adbapi.ConnectionPool('pymysql', database=database, host=host, port=port, user=user,
                                            password=password, charset=charset)
        # 创建连接池对象，每个连接对象在独立的线程中工作，内部使用第一个参数-》pymysql访问数据库
    def close_spider(self, spider):
        self.dbpool.close()

    def process_item(self, item, spider):
        self.dbpool.runInteraction(self.insert_db, item)
        # 以异步方式调用insert_db函数
        return item

    def insert_db(self, tx, item):  # 第一个参数是Transaction对象，
        values = (
            str(item.get('brokerPhone')),
            str(item.get('personal_name')),
            # str(item.get('house_title')),
            str(item['right_info']),
        )
        sql = "insert into anjuke_duo (brokerPhone, personal_name, right_info) values (%s,%s,%s)"
        tx.execute(sql, values)
        print('save ok')