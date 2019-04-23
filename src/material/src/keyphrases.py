# -*- coding:UTF-8 -*-

from .config import *
from xml.dom.minidom import parse
import xml.dom.minidom
import os, datetime, sys
sys.path.append(r'D:\software\anaconda\lib\site-packages\kleis')
import kleis.resources.dataset as kl
from .process import get_dir_path, get_file_path, get_paper_title, get_paper_abstract
from pymongo import MongoClient
import pymysql as mdb

def extract_phrase(text):
    default_corpus = kl.load_corpus()
    # train or load model
    default_corpus.training(filter_min_count=4)
    # labeling
    keyphrases = default_corpus.label_text(text)
    #print(keyphrases)
    phrases = []
    for phrase in keyphrases:
        phrases.append(phrase[2])
    return phrases

def insert_corpus(conn, cursor, paper_title, paper_abstract):
    type = 1
    finish_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = "INSERT INTO thesaurus_corpus (title, content, type, finish_time) VALUES ('%s','%s','%s','%s')" % (paper_title, paper_abstract, type, finish_time)
    cursor.execute(sql)
    conn.commit()

def insert_candidate_word(conn, cursor, paper_title, phrases):
    sql = "SELECT id FROM thesaurus_corpus WHERE title ='%s'"% paper_title
    cursor.execute(sql)
    corpus_id = cursor.fetchall()[0][0]
    state = 1
    for phrase in phrases:
        sql = "SELECT english_name FROM thesaurus_info WHERE english_name = '%s'" % phrase
        cursor.execute(sql)
        res = cursor.fetchall()
        if len(res) == 0:
            sql = "INSERT INTO thesaurus_candidate_word (name, corpus_id, state) VALUES ('%s','%s','%s')" % (phrase, corpus_id, state)
            try:
                cursor.execute(sql)
            except Exception:
                continue
            conn.commit()

def insert_index_word(source_dir, task_id):
    conn = mdb.connect(host=host, port=port, user=user, passwd=passwd, db=dbname, charset='utf8')
    cursor = conn.cursor()

    for filename, file_path in get_file_path(source_dir):
        xml_file_path = file_path[:-3]+'cermxml'
        paper_title = get_paper_title(xml_file_path)
        paper_abstract = get_paper_abstract(xml_file_path)
        if paper_title!=False and paper_abstract!=False:
            index_words = extract_phrase(paper_abstract)
            index_words_num = len(index_words)
            index_words_str = ';'.join(index_words)
            doc_id = str(filename[:-4])
            finish_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql = "UPDATE mirrorfileinfo SET finish_time='%s', index_word = '%s', index_number='%s' where docid='%s' and task_id='%s'" % (finish_time, index_words_str, index_words_num, doc_id, task_id)
            try:
                cursor.execute(sql)
            except Exception:
                continue
            conn.commit()


def insert_thesaurus_database(source_dir, task_id):
    conn = mdb.connect(host=thesaurus_host, port=thesaurus_port, user=thesaurus_user, passwd=thesaurus_passwd, db=thesaurus_dbname, charset='utf8')
    cursor = conn.cursor()

    for filename, file_path in get_file_path(source_dir):
        xml_file_path = file_path[:-3]+'cermxml'
        paper_title = get_paper_title(xml_file_path)
        paper_abstract = get_paper_abstract(xml_file_path)
        insert_corpus(conn, cursor, paper_title, paper_abstract)
        if paper_title!=False and paper_abstract!=False:
            phrases = extract_phrase(paper_abstract)
            #dic = {"title":paper_title, "keyphrases": phrases}
            #my_set.insert(dic)
            insert_candidate_word(conn, cursor, paper_title, phrases)
