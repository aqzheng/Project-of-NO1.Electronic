# -*- coding:UTF-8 -*-

import sys
from src.config import *
import pymysql as mdb
from xml.dom.minidom import parse
import xml.dom.minidom
import os, datetime
from src.figure import extract_figure, extract_figure_caption, get_figure_caption
from src.table import extract_table, get_table_caption
from src.process import get_dir_path, get_file_path, get_paper_title
from src.keyphrases import insert_thesaurus_database, insert_index_word
from src.index import create_index

def connect_database():
    conn = mdb.connect(host=host, port=port, user=user, passwd=passwd, \
                                      db=dbname, charset='utf8')
    cursor = conn.cursor()
    return conn, cursor

def get_duplicate(doc_id, cursor, connect):
    duplicate = 0
    try:
        sql_query = "SELECT duplicate from %s WHERE docid=%d ORDER BY task_id DESC LIMIT 1" % \
                    ('mirrorfileinfo', doc_id)
        cursor.execute(sql_query)
        connect.commit()
        duplicate = cursor.fetchone()[0]
    except Exception as e:
        connect.rollback()
    return duplicate

def create_figure_table(source_dir, task_id):
    conn, cursor = connect_database()
    # 如果不存在figure表，新建figure表
    image_sql = 'CREATE TABLE IF NOT EXISTS image (id INT(20) auto_increment key, doc_id BIGINT(16), ' \
                'pdf_name text, pdf_path text,' \
                'title text, fig_num INT (10),' \
                'figure_title text, figure_file text, figure_file_path text,' \
                'figure_page_file text, figure_page_file_path text, bool_check INT(10), ' \
                'task_id INT(20), duplicate INT(10), finish_time DATETIME)'
    cursor.execute(image_sql)
    for filename, file_path in get_file_path(source_dir):
        xml_file_path = file_path[:-3]+'cermxml'
        paper_title = get_paper_title(xml_file_path)
        print(paper_title)
        extract_figure_caption(filename, file_path)
        extract_figure(filename, file_path)
        all_figure_result = get_figure_caption(filename)
        if all_figure_result == False:
            continue
        doc_id = int(filename[:-4])
        for res in all_figure_result:
            fig_num, caption, fig_file_name, fig_page_file_name = res[0], res[1], res[2], res[3]
            pdf_name = filename
            pdf_path = mdb.escape_string(file_path)
            title = paper_title
            fig_num = fig_num
            figure_title = caption
            figure_file = fig_file_name
            figure_file_path = mdb.escape_string(os.path.join(figure_out_dir, filename, fig_file_name))
            figure_page_file = fig_page_file_name
            figure_page_file_path = mdb.escape_string(os.path.join(figure_out_dir, filename, fig_page_file_name))
            check = 0
            finish_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # get duplicated
            duplicate = get_duplicate(doc_id, cursor, conn)
            sql = "INSERT INTO image (doc_id, pdf_name, pdf_path, title, fig_num, figure_title, figure_file, figure_file_path, figure_page_file, figure_page_file_path, bool_check, task_id, duplicate, finish_time) " \
                  "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                  (doc_id, pdf_name, pdf_path, title, fig_num, figure_title, figure_file, figure_file_path, figure_page_file, figure_page_file_path, check, task_id, duplicate, finish_time)
            try:
                cursor.execute(sql)
            except Exception:
                continue
            conn.commit()
            try:
                create_index(figure_index_path, paper_title, figure_title)
            except Exception:
                continue
        figure_number = len(all_figure_result)
        finish_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = "UPDATE mirrorfileinfo SET finish_time='%s',figure_number = '%s' where task_id = '%s' and docid='%s'" % (finish_time,figure_number, task_id, doc_id)
        cursor.execute(sql)
        conn.commit()

def create_table_table(source_dir, task_id):
    conn, cursor = connect_database()
    table_sql = 'CREATE TABLE IF NOT EXISTS ttable (id INT(20) auto_increment key, doc_id BIGINT(16), ' \
                'pdf_name text, pdf_path text,' \
                'title text, table_num INT (10),' \
                'table_title text, table_file text, table_file_path text, ' \
                'bool_check INT(10), task_id INT(20), duplicate INT(10), finish_time DATETIME)'
    cursor.execute(table_sql)
    # for dirname, dir_path in get_dir_path(source_dir):
    #     extract_table(dirname, dir_path)
    extract_table(str(task_id), source_dir)
    for filename, file_path in get_file_path(source_dir):
        xml_file_path = file_path[:-3] + 'cermxml'
        paper_title = get_paper_title(xml_file_path)
        all_table_result = get_table_caption(str(task_id), filename, file_path)
        if all_table_result == False:
            continue
        doc_id = filename[:-4]
        for res in all_table_result:
            table_num, caption, table_file_name, table_file_path = res[0], res[1], res[2], res[3]
            pdf_name = filename
            pdf_path = mdb.escape_string(file_path)
            title = paper_title
            table_num = table_num
            table_title = caption
            table_file = table_file_name
            table_file_path = table_file_path
            check = 0
            finish_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            duplicate = get_duplicate(doc_id, cursor, conn)
            sql = "INSERT INTO ttable (doc_id, pdf_name, pdf_path, title, table_num, table_title, table_file, table_file_path, bool_check, task_id, duplicate, finish_time) " \
                  "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                  (doc_id, pdf_name, pdf_path, title, table_num, table_title, table_file, table_file_path, check, task_id, duplicate, finish_time)
            try:
                cursor.execute(sql)
            except Exception:
                continue
            conn.commit()
            try:
                create_index(table_index_path, paper_title, table_title)
            except Exception:
                continue
        table_number = len(all_table_result)
        finish_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = "UPDATE mirrorfileinfo SET finish_time='%s',table_number = '%s' where task_id = '%s' and docid='%s'" % (finish_time,table_number, task_id, doc_id)
        try:
            cursor.execute(sql)
        except Exception:
            continue
        conn.commit()

def preprocess_pdf(source_dir, task_id):
    create_figure_table(source_dir, task_id)
    create_table_table(source_dir, task_id)
    # insert_thesaurus_database(source_dir, task_id)
    insert_index_word(source_dir, task_id)

if __name__ == "__main__":
    print(sys.argv[1])
    # 获取task_id
    task_id_file = open(task_id_path, 'r')
    task_id = int(task_id_file.read().strip())
    # 获取源文件路径参数
    source_dir = sys.argv[1]
    preprocess_pdf(source_dir, task_id)