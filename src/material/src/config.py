import os

cur_path = r'D:\papershow_April\src\material'
# task_id config file
task_id_path = r'D:\papershow_April\config\task.txt'

# root dirs
target_dir = r'D:\papershow_April\static\material_results'
figure_out_dir = r'D:\papershow_April\static\material_results\figure_out'
table_out_dir = r'D:\papershow_April\static\material_results\table_out'

# jar dirs
jar_path = os.path.join(cur_path, 'jars')

figure_jar_dir = os.path.join(jar_path, 'ske-parent', 'lapdftext')
figure_jar = 'lapdftext-1.8.0-SNAPSHOT-jar-with-dependencies.jar'

table_jar_dir = os.path.join(jar_path, r'table_extractor\out\artifacts\table_extractor_jar')
table_jar = 'table_extractor.jar'

# paper database info
host = "127.0.0.1"
port = 3306
user = "root"
passwd = "bit"
dbname = "paper_repo"

# thesaurus database info
thesaurus_host = "127.0.0.1"
thesaurus_port = 3306
thesaurus_user = "root"
thesaurus_passwd = "bit"
thesaurus_dbname = "paper_repo"

# mongo database info
settings = {
    "ip": '127.0.0.1',
    "port": 27017,
    "db_name": "paper_repo",
    "set": "keyphrase"
}

figure_table_name = 'image'
table_table_name = 'ttable'

figure_index_path = r'D:\papershow_April\static\material_results\figure_index'
table_index_path = r'D:\papershow_April\static\material_results\table_index'