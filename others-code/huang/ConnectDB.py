# -=-=-=-=-=-=-=-=-=-=-=
# coding=UTF-8
# __author__='Guo Jun'
# Version 1..0.0
# -=-=-=-=-=-=-=-=-=-=-=
import pymysql

#    conn,cur=connDB()
#    connClose(conn, cur)
#     try:
#         conn.cursor().execute(istsql)
#     except Exception as e:
#         print(e)
#     conn.commit();

def connDB():  # 连接数据库函数
    conn = pymysql.connect(host='192.168.1.158', user='test', passwd='cigrg001', db='data', charset='utf8')
    cur = conn.cursor();
    return (conn, cur);


def exeUpdate(cur, sql):  # 更新语句，可执行update,insert语句
    sta = cur.execute(sql);
    return (sta);


def exeDelete(cur, IDs):  # 删除语句，可批量删除
    for eachID in IDs.split(' '):
        sta = cur.execute('delete from relationTriple where tID =%d' % int(eachID));
    return (sta);


def exeQuery(cur, sql):  # 查询语句
    cur.execute(sql);
    return (cur);


def connClose(conn, cur):  # 关闭所有连接
    cur.close();
    conn.commit();
    conn.close();


def get_data(items, table, symbol, startDate, endDate):
    conn, cur = connDB()
    query_sql = 'select ' + items + ' from data.' + table + ' where symbol in ('+ str(symbol).replace('[','').replace(']','') + ') and date between \'' + startDate + '\' and \'' + endDate + '\' order by symbol, date'
    # print(query_sql)
    try:
        cur.execute(query_sql)
        db_data = cur.fetchall()
    except Exception as e:
        print(e)
        print(query_sql)

    connClose(conn, cur)
    return (db_data)


def get_all_data(items, table, condition):
    conn, cur = connDB()
    query_sql = 'select ' + items + ' from data.' + table + ' ' + condition

    try:
        cur.execute(query_sql)
        db_data = cur.fetchall()
    except Exception as e:
        print(e)

    connClose(conn, cur)
    return (db_data)

# items = 'symbol, close'
# startDate = '2018-02-12'
# endDate = '2018-03-12'
# table = 'forward_adj_price_stk'
# symbol_list = ['600030.SH', '601006.SH']
# db_data = get_data(items, table, symbol_list, startDate, endDate)
# print(db_data)