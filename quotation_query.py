# -*- coding:UTF-8 -*-

from mysql_config import *
import pymysql as mdb

def connect_database():
    conn = mdb.connect(host=host, port=port, user=user, passwd=passwd,
                                      db=dbname, charset='utf8')
    cursor = conn.cursor()
    return conn, cursor

def get_reference(title):
    conn, cursor = connect_database()
    reference_sql = "SELECT id,reference_paper, reference_sentence,bool_check FROM Citation WHERE title = '%s'" % title
    cursor.execute(reference_sql)
    reference_list = cursor.fetchall()
    conn.close()
    return reference_list

def get_paper_id1(title):
    print('BEGIN')
    conn, cursor = connect_database()
    id_sql = "SELECT docid FROM Citation WHERE title = '%s'" % title
    cursor.execute(id_sql)
    id_list = cursor.fetchall()
    conn.close()
    if len(id_list) == 0:
        return -1
    return id_list[0][0]

def update_reference(paper_title, reference_title, reference_content,id):
    conn, cursor = connect_database()
    reference_sql = "UPDATE Citation SET reference_paper = '%s', bool_check = '%s',reference_sentence  = '%s' WHERE id = '%s'" % (reference_title, '1', reference_content, id)
    cursor.execute(reference_sql)
    conn.commit()

def check_reference(paper_title, id):
    conn, cursor = connect_database()
    reference_sql = "UPDATE Citation SET bool_check = '%s' WHERE id = '%s'" % (str(1), id)
    cursor.execute(reference_sql)
    conn.commit()

if __name__ == "__main__":
    print(type(get_reference('End-to-end Neural Coreference Resolution')))
    print(get_reference('End-to-end Neural Coreference Resolution'))
    print(get_paper_id1('End-to-end Neural Coreference Resolution'))