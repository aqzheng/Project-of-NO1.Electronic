# -- coding: utf-8 --
import os,sys,shutil
import pymysql

def copyFiles(paper_id,paper_path):
    #paper_path = paper_path.decode("utf-8")
    file_name = ("%d" % paper_id)+'.pdf'
    targetFile = os.path.join(targetDir,file_name)
    shutil.copyfile(paper_path, targetFile)

def gci(sourceDir):
    global id
    for path in sourceDir:
        copyFiles(path[0],path[1])
        id = id + 1


def get_id():
    cwd = os.getcwd()
    filenum_path = os.path.join(cwd, 'reference\\filenum.txt')
    with open(filenum_path, 'r') as f:
        filenum = int(f.read())
        f.close()
    return filenum

def write_id():
    cwd = os.getcwd()
    filenum_path = os.path.join(cwd, 'reference\\filenum.txt')
    with open(filenum_path, 'w') as f:
        f.write(str(id))
        f.close()

def get_sourceDir(start,end):
    import mysql_config
    connect = pymysql.Connect(
        host=mysql_config.host,
        port=mysql_config.port,
        user=mysql_config.user,
        passwd=mysql_config.passwd,
        db=mysql_config.db,
        charset=mysql_config.charset
    )
    cursor = connect.cursor()
    path = []
    try:
        sql = 'select * from paper_index where id > %s and id <= %s ' %(start,end)
        cursor.execute(sql)
        path = cursor.fetchall()
    except Exception as e:
        print("query wrong" + str(e))
    connect.close()
    return path

if __name__ == "__main__":
    if len(sys.argv)!=3:
        print("input error")
        sys.exit()

    targetDir = sys.argv[1]
    solved_file_num = int(sys.argv[2])
    if solved_file_num == 0 :
        solved_file_num = 500

    if not os.path.exists(targetDir):
        os.mkdir(targetDir)


    id = get_id()

    sourceDir = get_sourceDir(id,id+solved_file_num)

    gci(sourceDir)
    write_id()