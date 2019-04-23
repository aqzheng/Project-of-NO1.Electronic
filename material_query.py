# -*- coding:UTF-8 -*-

from mysql_config import *
import pymysql as mdb
from whoosh.qparser import QueryParser, FuzzyTermPlugin
from whoosh.index import open_dir

def connect_database():
    conn = mdb.connect(host=host, port=port, user=user, passwd=passwd,
                                      db=dbname, charset='utf8')
    cursor = conn.cursor()
    return conn, cursor

def get_figure(title):
    conn, cursor = connect_database()
    figure_sql = "SELECT pdf_name, fig_num, figure_title, figure_file, figure_page_file, bool_check FROM image WHERE title = '%s'" % title
    cursor.execute(figure_sql)
    figure_list = cursor.fetchall()
    conn.close()
    return figure_list

def get_table(title):
    conn, cursor = connect_database()
    table_sql = "SELECT pdf_name, table_num, table_title, table_file, bool_check, task_id FROM ttable WHERE title = '%s'" % title
    cursor.execute(table_sql)
    table_list = cursor.fetchall()
    conn.close()
    new_table_list = []
    for e in table_list:
        table_file = e[3]
        task_id = e[5]
        new_table_file = 'task_'+str(task_id)+ r'/xml/' + table_file
        new_table_list.append([e[0], e[1], e[2], new_table_file, e[4]])
    return new_table_list

def get_paper_id2(title):
    conn, cursor = connect_database()
    id_sql = "SELECT doc_id FROM image WHERE title = '%s'" % title
    cursor.execute(id_sql)
    id_list = cursor.fetchall()
    conn.close()
    if len(id_list) == 0:
        return -1
    return id_list[0][0]

def get_figure_all():
    conn, cursor = connect_database()
    figure_sql_all = "SELECT title, fig_num, figure_title, figure_file FROM image"
    cursor.execute(figure_sql_all)
    figure_list_all = cursor.fetchall()
    conn.close()
    return figure_list_all

def get_table_all():
    conn, cursor = connect_database()
    table_sql_all = "SELECT title, table_num, table_title, table_file, task_id FROM ttable"
    cursor.execute(table_sql_all)
    table_list_all = cursor.fetchall()
    conn.close()
    new_table_list_all = []
    for e in table_list_all:
        table_file = e[3]
        task_id = e[4]
        new_table_file = 'task_'+str(task_id)+ r'/xml/' + table_file
        new_table_list_all.append([e[0], e[1], e[2], new_table_file])
    return new_table_list_all

def search_table(query_word):
    print(query_word)
    conn, cursor = connect_database()
    ix = open_dir(table_index_path)
    searcher = ix.searcher()
    parser = QueryParser("content", ix.schema)
    my_query = parser.parse(query_word)
    results = searcher.search(my_query, limit=100)
    print(results)
    ret = []
    for result in results:
        paper_title = result['title']
        table_title = result['content']
        sql = "SELECT pdf_path FROM ttable WHERE title='%s'" % paper_title
        print(paper_title)
        cursor.execute(sql)
        pdf_path = cursor.fetchall()[0][0]
        pdf_name = '/'.join(pdf_path.split('\\')[-3:])
        # process for figure_title:
        """
        new_query_word = query_word.lower()
        new_figure_title = figure_title.lower()
        pos = new_figure_title.index(new_query_word)
        fig_title_left = figure_title[:pos]
        fig_title_right = figure_title[pos + len(query_word):]
        highlight_word = figure_title[pos: pos+len(query_word)]"""
        ret.append((paper_title, table_title, pdf_name))
        print(paper_title, table_title, pdf_name)
    return ret

def search_figure(query_word):
    print(query_word)
    conn, cursor = connect_database()
    ix = open_dir(figure_index_path)
    searcher = ix.searcher()
    parser = QueryParser("content", ix.schema)
    my_query = parser.parse(query_word)
    results = searcher.search(my_query, limit=100)
    print(results)
    ret = []
    for result in results:
        paper_title = result['title']
        figure_title = result['content']
        sql = "SELECT pdf_path FROM image WHERE title='%s'" % paper_title
        cursor.execute(sql)
        pdf_path = cursor.fetchall()[0][0]
        pdf_name = '/'.join(pdf_path.split('\\')[-3:])
        # process for figure_title:
        """
        new_query_word = query_word.lower()
        new_figure_title = figure_title.lower()
        pos = new_figure_title.index(new_query_word)
        fig_title_left = figure_title[:pos]
        fig_title_right = figure_title[pos + len(query_word):]
        highlight_word = figure_title[pos: pos+len(query_word)]"""
        ret.append((paper_title, figure_title, pdf_name))
        print(paper_title, figure_title, pdf_name)
    return ret

def update_figure(paper_title, figure_id, figure_title):
    conn, cursor = connect_database()
    figure_sql = "UPDATE image SET figure_title = '%s', bool_check = '%s' WHERE fig_num = '%s' AND title = '%s'" % (figure_title, '1', figure_id, paper_title)
    cursor.execute(figure_sql)
    conn.commit()

def update_table(paper_title, table_id, table_title):
    conn, cursor = connect_database()
    table_sql = "UPDATE ttable SET table_title = '%s', bool_check = '%s' WHERE table_num = '%s' AND title = '%s'" % (table_title, '1', table_id, paper_title)
    cursor.execute(table_sql)
    conn.commit()

def check_figure(paper_title, figure_id):
    conn, cursor = connect_database()
    figure_sql = "UPDATE image SET bool_check = '%s' WHERE fig_num = '%s' AND title = '%s'" % (str(1), figure_id, paper_title)
    cursor.execute(figure_sql)
    conn.commit()

def check_table(paper_title, table_id):
    conn, cursor = connect_database()
    table_sql = "UPDATE ttable SET bool_check = '%s' WHERE table_num = '%s' AND title = '%s'" % (str(1), table_id, paper_title)
    cursor.execute(table_sql)
    conn.commit()


if __name__ == "__main__":
    print(type(get_figure('Modeling Relation Paths for Representation Learning of Knowledge Bases')))
    print(get_table('End-to-end Neural Coreference Resolution'))
    print(get_paper_id2('End-to-end Neural Coreference Resolution'))
    print(len(get_figure_all()))