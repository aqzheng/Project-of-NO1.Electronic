# -*- coding:UTF-8 -*-

import os
import pymysql as mdb
from .config import *
from whoosh.fields import Schema, TEXT
from whoosh.index import create_in, open_dir
from whoosh.query import *
from whoosh.qparser import QueryParser, FuzzyTermPlugin


def create_index(index_path, paper_title, material_title):
    if not os.path.exists(index_path):
        schema = Schema(title=TEXT(stored=True), content=TEXT(stored=True))
        os.mkdir(index_path)
        ix = create_in(index_path, schema)
    else:
        ix = open_dir(index_path)
    writer = ix.writer()
    writer.add_document(title = paper_title, content = material_title)
    writer.commit()

def searcher(index_path, query):
    ix = open_dir(index_path)
    searcher = ix.searcher()
    parser = QueryParser("content", ix.schema)
    parser.add_plugin(FuzzyTermPlugin())
    my_query = parser.parse(query)
    results = searcher.search(my_query, limit=None)
    for result in results:
        print(result['content'])

def connect_database():
    conn = mdb.connect(host=host, port=port, user=user, passwd=passwd, \
                                      db=dbname, charset='utf8')
    cursor = conn.cursor()
    return conn, cursor

def test_create_on_table():
    conn, cursor = connect_database()
    table_sql = 'SELECT title, table_title FROM ttable'
    cursor.execute(table_sql)
    results = cursor.fetchall()
    for paper_title, table_title in results:
        create_index(table_index_path, paper_title, table_title)
    searcher(table_index_path, 'results')

def test_create_on_figure():
    conn, cursor = connect_database()
    figure_sql = 'SELECT title, figure_title FROM image'
    cursor.execute(figure_sql)
    results = cursor.fetchall()
    for paper_title, figure_title in results:
        create_index(figure_index_path, paper_title, figure_title)
    searcher(figure_index_path, 'results')

def test_search_on_figure():
    searcher(figure_index_path, 'figure')

def test_search_on_table():
    searcher(table_index_path, 'Results')




