import pymysql

def init_db():
    database = "dir001"
    host = "localhost"
    port = 3306
    user = "root"
    password = "mysql"
    charset = 'utf8mb4'
    try:
        conn = pymysql.connect(database=database, host=host, port=port,
                               user=user, password=password, charset=charset)
        return conn
    except Exception as e:
        print(e, "Error:数据库连接错误")
        return None


def select_data(conn, sql):
    try:
        cs = conn.cursor()
        cs.execute(sql)
        cs.close()
        return cs.fetchall()
    except Exception as e:
        print(e, "Error:数据库连接错误")
        return None
    # finally:
    #     conn.close()

def db_close(conn):
    conn.close()


def update_demo():
    pass


def delete_demo():
    pass


def insert_demo():
    pass


def save2mysql(*args, **kwargs):
    """
    传参
    (keyword=content.get("keyword"),c_time=content.get("c_time"),c_name=self.name,core=content.get('core'))
    """

    conn = pymysql.connect(host="localhost", port=3306, database="data_word",
                           user="root", password="mysql", charset='utf8mb4')

    sql = "insert into ciku_china_hotword (%s) values (%s)"
    key_list = []
    value_list = []
    for k, v in kwargs.items():
        key_list.append(k)
        value_list.append('%%(%s)s' % k)
    sql = sql % (','.join(key_list), ','.join(value_list))
    cs = conn.cursor()
    cs.execute(sql, kwargs)
    conn.commit()
    cs.close()
    conn.close()