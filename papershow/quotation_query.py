# -*- coding:UTF-8 -*-

from config import *
import pymysql as mdb

def connect_database():
    conn = mdb.connect(host=host, port=port, user=user, passwd=passwd,
                                      db=dbname, charset='utf8')
    cursor = conn.cursor()
    return conn, cursor

def get_reference(title):
    conn, cursor = connect_database()
    reference_sql = "SELECT reference_title, reference_id, reference_sentence FROM citation_database WHERE paper_title = '%s'" % title
    cursor.execute(reference_sql)
    reference_list = cursor.fetchall()
    conn.close()
    return reference_list

def get_paper_id1(title):
    print('BEGIN')
    print(title == 'End-to-end Neural Coreference Resolution')
    conn, cursor = connect_database()
    id_sql = "SELECT id FROM citation_database WHERE paper_title = '%s'" % title
    cursor.execute(id_sql)
    id_list = cursor.fetchall()
    conn.close()
    if len(id_list) == 0:
        return -1
    return id_list[0][0]


if __name__ == "__main__":
    print(type(get_reference('End-to-end Neural Coreference Resolution')))
    print(get_reference('End-to-end Neural Coreference Resolution'))
    print(get_paper_id1('End-to-end Neural Coreference Resolution'))