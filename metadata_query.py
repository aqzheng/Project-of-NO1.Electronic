# -*- coding:UTF-8 -*-

from mysql_config import *
import pymysql as mdb
import os

def connect_database():
    conn = mdb.connect(host=host, port=port, user=user, passwd=passwd,
                                      db=dbname, charset='utf8')
    cursor = conn.cursor()
    return conn, cursor

def get_metadata(paper_title):
    conn, cursor = connect_database()
    metadata_sql = "SELECT id, clc_code, index_word, type, contributor, organization FROM mirrorfileinfo WHERE title='%s'" % paper_title
    cursor.execute(metadata_sql)
    metadata_list = cursor.fetchall()
    conn.close()
    return metadata_list

def update_metadata(paper_title, clc_code, index_word, type, contributor, organization):
    conn, cursor = connect_database()
    metadata_sql = "UPDATE mirrorfileinfo SET clc_code = '%s', index_word = '%s', type = '%s', contributor = '%s', organization = '%s', bool_check = '%s' WHERE title='%s'" % \
                   (clc_code, index_word, type, contributor, organization, '1', paper_title)
    cursor.execute(metadata_sql)
    conn.commit()
    conn.close()

def get_metadata_all(task_id, start, end):
    # 用于flash刷新
    conn, cursor = connect_database()
    sql = "SELECT docid, title, clc_code, task_id, task_begin_time, index_number, citation_number, figure_number, table_number, duplicate, bool_check FROM mirrorfileinfo where finish_time is not NULL and task_id = '%s'" % task_id
    cursor.execute(sql)
    metadata_list_all = cursor.fetchall()
    conn.close()
    return metadata_list_all[start:end]

def get_metadata_now():
    # 用于获取当前任务总数
    file = open(task_id_path, 'r')
    task_id = int(file.read().strip())
    if int(open(task_done_path, 'r').read().strip()) == 1:
        task_id -= 1
    conn, cursor = connect_database()
    sql = "SELECT min(task_begin_time),count(*),sum(citation_number),sum(figure_number),sum(table_number) from mirrorfileinfo WHERE task_id='%d' and finish_time is not null;" % task_id
    cursor.execute(sql)
    task_list_all = cursor.fetchall()
    data = []
    data.append((task_id, task_list_all[0][0], task_list_all[0][1],int(task_list_all[0][2]),int(task_list_all[0][3]),int(task_list_all[0][4])))
    return data

def get_taskall_query():
    # 用于全部任务信息查询
    conn, cursor = connect_database()
    sql = "SELECT DISTINCT task_id from mirrorfileinfo;"
    cursor.execute(sql)
    task_list_all = cursor.fetchall()
    data = []
    for task_id in task_list_all:
        sql = "SELECT min(task_begin_time),count(*) from mirrorfileinfo WHERE task_id = '%d';" % task_id
        cursor.execute(sql)
        list_all = cursor.fetchall()
        data.append((task_id, list_all[0][0], list_all[0][1]))
    return data

def check_metadata(doc_id, task_id):
    conn, cursor = connect_database()
    metadata_sql = "UPDATE mirrorfileinfo SET bool_check = '%s' WHERE docid='%s' and task_id='%s'" % \
                   ('1', doc_id, task_id)
    cursor.execute(metadata_sql)
    conn.commit()
    conn.close()

def get_paper_number(task_id):
    conn, cursor = connect_database()
    sql = "SELECT count(*) from mirrorfileinfo where task_id='%d';" % task_id
    cursor.execute(sql)
    num = cursor.fetchall()
    return num[0]

if __name__ == "__main__":
    print(len(get_metadata()))