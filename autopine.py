import pymysql,os,sys,shutil,math,datetime
import requests
import subprocess
pdf_num = 100
size = 5
from src.chn_classify_workspace.tag_paper_chn import run_classifier
def query_table(host, port, user, passwd, db, table, begin_time, end_time):
    connect = pymysql.Connect(
        host=host,
        port=port,
        user=user,
        passwd=passwd,
        db=db
    )
    cursor = connect.cursor()
    data = []
    if table != "":
        if begin_time != "":
            sql = 'select docid,filename,filepath,datetemp,duplicate from %s where datetemp >= "%s" and datetemp <= "%s" ' % (table, begin_time, end_time)
        else:
            sql = 'select docid,filename,filepath,datetemp,duplicate from %s' % table
        cursor.execute(sql)
        data += cursor.fetchall()
    else:
        cursor.execute("show tables")
        table_list = [tuple[0] for tuple in cursor.fetchall()]
        for table in table_list:
            sql = 'select docid,filename,filepath,datetemp,duplicate from %s where datetemp >= "%s" and datetemp <= "%s" ' % (table, begin_time, end_time)
            cursor.execute(sql)
            data += cursor.fetchall()
    connect.close()
    return data

def get_paper_num(host, port, user, passwd, db, table, begin_time, end_time):
    return len(query_table(host, port, user, passwd, db, table, begin_time, end_time))

def run_pipeline(host, port, user, passwd, db, table, begin_time, end_time):
    write_done_file(0)
    task_id = int(open(os.path.join(sys.path[0], "config", "task.txt"),"r").readline())
    results = query_table(host, port, user, passwd, db, table, begin_time, end_time)

    insert_into_MirrorFileInfo(results,task_id) #将部分信息直接存入元数据表中
    start = 0
    for id in range(0, len(results), pdf_num):
        print(id)
        list_len = min(id+pdf_num,len(results))
        download_pdf(results[id:list_len], id//(pdf_num//size), task_id) #下载pdf到本地，未全部完成
        run_bat(task_id, start, math.ceil((list_len-id)/(pdf_num//size))) #执行脚本
        start += math.ceil((list_len-id)/(pdf_num//size))

    run_classifier()
    open(os.path.join(sys.path[0], "config", "task.txt"), "w").write("%s" %(task_id + 1))
    write_done_file(1)

def run_bat(task_id, start, num):
    file_list = str(num) + " "
    for id in range(num):
        file_list += os.path.join(sys.path[0], "static", "pdf_file", "task_"+str(task_id), str(id+start)) + " "
    print(file_list)
    subprocess.call(os.path.join(sys.path[0], 'main.bat %s') % file_list)
    print("finished")

def download_pdf(results, id, task_id):
    for i in range(math.ceil(len(results)/(pdf_num//size))):
        pdf_file_path = os.path.join(sys.path[0], "static", "pdf_file", "task_"+str(task_id), str(i+id))
        mkdir(pdf_file_path)
        for j in range(i*pdf_num//size,min(len(results),(i+1)*pdf_num//size)):
            remote_path = 'http://172.16.155.32/allpdf/' + results[j][2]
            file_content = requests.get(remote_path).content
            open(os.path.join(pdf_file_path, str(results[j][0]) + ".pdf"), 'wb').write(file_content)

def insert_into_MirrorFileInfo(results, task_id):
    import mysql_config
    connect = pymysql.Connect(
        host=mysql_config.host,
        port=mysql_config.port,
        user=mysql_config.user,
        passwd=mysql_config.passwd,
        db=mysql_config.dbname,
    )
    cursor = connect.cursor()
    for i in range(len(results)):
        try:
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql_insert = 'INSERT INTO MirrorFileInfo (docid, task_id, task_begin_time, duplicate,bool_check,index_number,citation_number,figure_number,table_number) VALUES (%d, %d, "%s", %d,0,0,0,0,0)' % (results[i][0], task_id, dt, results[i][4])
            cursor.execute(sql_insert)
            connect.commit()
        except Exception as e:
            connect.rollback()

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def write_done_file(val):
    with open(os.path.join(sys.path[0], "config", "done.txt"),"w") as fp:
        fp.write("%s" % val)