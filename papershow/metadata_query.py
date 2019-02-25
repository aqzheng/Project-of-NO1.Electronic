# -*- coding:UTF-8 -*-

from config import *
import pymysql as mdb

def connect_database():
    conn = mdb.connect(host=host, port=port, user=user, passwd=passwd,
                                      db=dbname, charset='utf8')
    cursor = conn.cursor()
    return conn, cursor

def get_metadata(paper_title):
    conn, cursor = connect_database()
    metadata_sql = "SELECT id, clc_code, index_word, type, contributor_list, organization_list FROM mirrorfileinfo WHERE title='%s'" % paper_title
    cursor.execute(metadata_sql)
    metadata_list = cursor.fetchall()
    conn.close()
    return metadata_list

def update_metadata(paper_title, clc_code, index_word, type, contributor, organization):
    conn, cursor = connect_database()
    metadata_sql = "UPDATE mirrorfileinfo SET clc_code = '%s', index_word = '%s', type = '%s', contributor_list = '%s', organization_list = '%s', bool_check = '%s' WHERE title='%s'" % \
                   (clc_code, index_word, type, contributor, organization, '1', paper_title)
    cursor.execute(metadata_sql)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    print(len(get_metadata()))