import os,sys,pymysql

filecount = 77

def insert_into_paper_index(sourceDir):
    print(sourceDir)
    try:
        sql_insert = 'INSERT INTO paper_index (id,path) VALUES (%s,"%s")' % (filecount,pymysql.escape_string(sourceDir))
        cursor.execute(sql_insert)
        connect.commit()
    except Exception as e:
        print("insert wrong" + str(e))
        connect.rollback()

def gci(sourceDir):
    global filecount
    for file in os.listdir(sourceDir):
        sourceFile = os.path.join(sourceDir, file)
        if os.path.isdir(sourceFile):
            gci(sourceFile)
        elif os.path.splitext(sourceFile)[1]=='.pdf':
            insert_into_paper_index(sourceFile)
            filecount = filecount + 1

if __name__ == "__main__":
    if len(sys.argv)!=2:
        print("input error")
        sys.exit()
    sourceDir = os.path.abspath(sys.argv[1])
    if not os.path.exists(sourceDir):
        print("sourceDir is not exist")
        sys.exit()
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
    gci(sourceDir)
    connect.close()