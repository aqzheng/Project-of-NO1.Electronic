# -*- coding: utf-8 -*-
import os,operator,sys
from flask import Flask, render_template, request, jsonify, make_response, send_from_directory, flash
import mimetypes

app = Flask(__name__)
app.config.from_object('config')

"""init"""
@app.route('/')
@app.route('/index')
def index_view():
    return render_template("index.html")

@app.route('/main')
def main_view():
    return render_template("main.html")

@app.route('/taskall_query')
def taskall_query_view():
    return render_template("taskall_query.html")

@app.route('/user_input')
def user_input_view():
    return render_template("user_input.html")

@app.route('/metadata')
def metadata_view():
    return render_template("metadata.html")

@app.route('/FrameworkContent')
def FrameworkContent_view():
    return render_template("FrameworkContent.html")

@app.route('/quotation')
def quotation_view():
    return render_template("quotation.html")

@app.route('/update_reference')
def update_reference_view():
    return render_template("update_reference.html")

@app.route('/material')
def material_view():
    return render_template("material.html")

@app.route('/figure_query')
def figure_query_view():
    return render_template("figure_query.html")

@app.route('/update_figure')
def update_figure_view():
    return render_template("update_figure.html")

@app.route('/table_query')
def table_query_view():
    return render_template("table_query.html")

@app.route('/task_query')
def task_query_view():
    return render_template("task_query.html")

@app.route('/update_table')
def update_table_view():
    return render_template("update_table.html")

@app.route('/metadata_manage')
def metadata_manage_view():
    return render_template("metadata_manage.html")

@app.route('/material_manage')
def material_manage_view():
    return render_template("material_manage.html")

@app.route('/test')
def test_view():
    return render_template('test.html')

from metadata_query import get_taskall_query
@app.route('/taskall_query/taskall_query', methods=['POST'])
def taskall_query():
    data = {}
    metadata_list_all = get_taskall_query()
    data['metadata'] = metadata_list_all
    if len(data['metadata']) == 0:
        data['status'] = False
    else:
        data['status'] = True
    return jsonify(data)

@app.route('/user_input/run_reset', methods=['POST'])
def run_reset():
    data = {}
    with open(os.path.join(sys.path[0], "config", "done.txt"),"r") as fp:
        done = int(fp.readline())
    if done == 0:
        task_id = int(open(os.path.join(sys.path[0], "config", "task.txt"),"r").readline())
        open(os.path.join(sys.path[0], "config", "task.txt"), "w").write("%s" %(task_id + 1))
        open(os.path.join(sys.path[0], "config", "done.txt"), "w").write("%s" % (1))
    return jsonify(data)

from autopine import get_paper_num, run_pipeline
@app.route('/user_input/query_repo', methods=['POST'])
def query_time_view():
    data = {}
    data['status'] = False
    with open(os.path.join(sys.path[0], "config", "done.txt"),"r") as fp:
        data['done'] = int(fp.readline())
    begin_time = request.form.get('begin_time')
    end_time = request.form.get('end_time')
    table = request.form.get('table_name')
    host = request.form.get('host')
    port = int(request.form.get('port'))
    user = request.form.get('user')
    passwd = request.form.get('passwd')
    db = request.form.get('db')
    if (begin_time != "" and end_time != "" and operator.gt(end_time,begin_time) ) or (table != ""):
        data['status'] = True
        data['paper_num'] = get_paper_num(host, port, user, passwd, db, table, begin_time, end_time )
    return jsonify(data)

@app.route('/user_input/auto_pipeline', methods=['POST'])
def auto_pipeline_view():
    data = {}
    begin_time = request.form.get('begin_time')
    end_time = request.form.get('end_time')
    table = request.form.get('table_name')
    host = request.form.get('host')
    port = int(request.form.get('port'))
    user = request.form.get('user')
    passwd = request.form.get('passwd')
    db = request.form.get('db')
    run_pipeline(host, port, user, passwd, db, table, begin_time, end_time)
    return jsonify(data)


"""quotation part"""
from quotation_query import get_reference, get_paper_id1
@app.route('/quotation/qquery', methods=['POST'])
def qquery_view():
    data = {}
    paper_title = request.form.get('paper_title')
    print(paper_title)
    data['paper_title'] = paper_title
    data['paper_id'] = str(get_paper_id1(paper_title))
    data['reference'] = get_reference(paper_title)
    print(data['paper_id'])
    print(data['reference'])
    if len(data['reference']) == 0:
        data['status'] = False
        print("NO DATA ERROR!")
    else:
        data['status'] = True
    return jsonify(data)

"""quotation update part"""
from quotation_query import update_reference
@app.route('/reference_update/rupdate', methods=['POST'])
def rupdate_view():
    data = {}
    paper_title = request.form.get('paper_title')
    reference_title = request.form.get('reference_title')
    reference_content = request.form.get('reference_content')
    database_id = request.form.get('database_id')
    update_reference(paper_title, reference_title, reference_content,database_id)
    data['status'] = True
    return jsonify(data)

"""figure check part"""
from quotation_query import check_reference
@app.route('/reference/check', methods=['POST'])
def rcheck_view():
    data = {}
    paper_title = request.form.get('paper_title')
    reference_id = request.form.get('reference_id')
    check_reference(paper_title, reference_id)
    return jsonify(data)

"""metadata part"""
from metadata_query import get_metadata
@app.route('/metadata/metaquery', methods=['POST'])
def metaquery_view():
    data = {}
    paper_title = request.form.get('paper_title')
    print(paper_title)
    data['paper_title'] = paper_title
    metadata_list = get_metadata(paper_title)
    if len(metadata_list) == 0 :
        data['status'] = False
    else:
        data['status'] = True
    data['paper_id'] = metadata_list[0][0]
    data['clc_code'] = metadata_list[0][1]
    data['index_word'] = metadata_list[0][2]
    data['type'] = metadata_list[0][3]
    data['contributor'] = metadata_list[0][4]
    data['organization'] = metadata_list[0][5]
    print(data)
    return jsonify(data)

"""material part"""
from material_query import get_figure, get_table, get_paper_id2
@app.route('/material/query', methods=['POST'])
def query_view():
    data = {}
    paper_title = request.form.get('paper_title')
    print(paper_title)
    data['paper_title'] = paper_title
    data['paper_id'] = str(get_paper_id2(paper_title))
    data['figures'] = get_figure(paper_title)
    data['tables'] = get_table(paper_title)
    print(data['paper_id'])
    print(data['figures'])
    print(data['tables'])
    if len(data['figures']) == 0 and len(data['tables']) == 0:
        data['status'] = False
    else:
        data['status'] = True
    return jsonify(data)

"""figure query part"""
from material_query import search_figure
@app.route('/figure_query/fquery', methods=['POST'])
def fquery_view():
    data = {}
    query_word = request.form.get('query_word')
    print(query_word)
    data['results'] = search_figure(query_word)
    if len(data['results']) == 0:
        data['status'] = False
    else:
        data['status'] = True
    return jsonify(data)

"""table query part"""
from material_query import search_table
@app.route('/table_query/tquery', methods=['POST'])
def tquery_view():
    data = {}
    query_word = request.form.get('query_word')
    print(query_word)
    data['results'] = search_table(query_word)
    if len(data['results']) == 0:
        data['status'] = False
    else:
        data['status'] = True
    return jsonify(data)

"""metadata update part"""
from metadata_query import update_metadata
@app.route('/metadata/metaupdate', methods=['POST'])
def metaupdate_view():
    data = {}
    paper_title = request.form.get('paper_title')
    clc_code = request.form.get("clc_code")
    index_word = request.form.get("index_word")
    type = request.form.get("type")
    contributor = request.form.get("contributor")
    organization = request.form.get("organization")

    update_metadata(paper_title, clc_code, index_word, type, contributor, organization)
    data['status'] = True
    return jsonify(data)

"""figure update part"""
from material_query import update_figure
@app.route('/figure_update/fupdate', methods=['POST'])
def fupdate_view():
    data = {}
    paper_title = request.form.get('paper_title')
    figure_id = request.form.get('figure_id')
    figure_title = request.form.get('figure_title')
    update_figure(paper_title, figure_id, figure_title)
    data['status'] = True
    return jsonify(data)

"""figure check part"""
from material_query import check_figure
@app.route('/figure/check', methods=['POST'])
def fcheck_view():
    data = {}
    paper_title = request.form.get('paper_title')
    figure_id = request.form.get('figure_id')
    check_figure(paper_title, figure_id)
    return jsonify(data)

"""table update part"""
from material_query import update_table
@app.route('/table_update/tupdate', methods=['POST'])
def tupdate_view():
    data = {}
    paper_title = request.form.get('paper_title')
    table_id = request.form.get('table_id')
    table_title = request.form.get('table_title')
    update_table(paper_title, table_id, table_title)
    data['status'] = True
    return jsonify(data)

"""table check part"""
from material_query import check_table
@app.route('/table/check', methods=['POST'])
def tcheck_view():
    data = {}
    paper_title = request.form.get('paper_title')
    table_id = request.form.get('table_id')
    check_table(paper_title, table_id)
    return jsonify(data)

"""material_manage part"""
from material_query import get_figure_all, get_table_all
@app.route('/material_manage/mmquery', methods=['POST'])
def mmquery_view():
    data = {}
    data['figures_all'] = get_figure_all()
    data['tables_all'] = get_table_all()
    if len(data['figures_all'])==0 and len(data['tables'])==0:
        data['status'] = False
    else:
        data['status'] = True
    return jsonify(data)


"""File Download And Upload"""
basepath = os.path.dirname(__file__)  # 当前文件所在路径

UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JSON_AS_ASCII'] = False
upload_path = os.path.join(basepath, UPLOAD_FOLDER)

DOWNLOAD_FOLDER = 'download'

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    app.logger.debug('download_file...')
    if os.path.exists(os.path.join(DOWNLOAD_FOLDER, filename)) and os.path.isfile(os.path.join(DOWNLOAD_FOLDER, filename)):
        response = make_response(send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True))
        mime_type = mimetypes.guess_type(filename)[0]
        response.headers['Content-Type'] = mime_type
        response.headers["Content-Disposition"] = "attachment; filename={};".format(filename.encode().decode('latin-1'))
        return response
    return render_template('404.html')

"""metadata flash part"""
from metadata_query import  get_metadata_now
@app.route('/user_input/flash_now', methods=['POST'])
def flash_now():
    data = {}
    metadata_list_all = get_metadata_now()
    data['metadata'] = metadata_list_all
    if len(data['metadata']) == 0:
        data['status'] = False
    else:
        data['status'] = True
    return jsonify(data)

from metadata_query import  get_metadata_all, get_paper_number
@app.route('/user_input/flash', methods=['POST'])
def flash():
    data = {}
    pageSize = int(request.form.get('pageSize'))
    pageIndex = int(request.form.get('pageIndex'))
    task_id = int(request.form.get('task_id'))
    data['paper_num'] = get_paper_number(task_id)
    metadata_list_all = get_metadata_all(task_id, (pageIndex-1)*pageSize, pageIndex*pageSize)
    data['metadata'] = metadata_list_all
    print(data)
    if len(data['metadata']) == 0:
        data['status'] = False
    else:
        data['status'] = True
    return jsonify(data)

"""metadata check part"""
from metadata_query import check_metadata
@app.route('/metadata/check', methods=['POST'])
def metadatacheck_view():
    data = {}
    doc_id = request.form.get('doc_id')
    task_id = request.form.get('task_id')
    check_metadata(doc_id, task_id)
    data['status'] = True
    return jsonify(data)

# 用于判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

import chardet
@app.route('/upload', methods=['POST'])
def upload():
    data = {}
    data['status'] = False
    data['desc'] = ""
    data['file_name'] = ""

    if 'myfile' not in request.files:
        flash('No file part')
        data['desc'] = "请求访问错误！"
        return jsonify(data)

    myfile = request.files['myfile']
    if myfile.filename == "":
        flash('No selected file')
        data['desc'] = "请求文件不存在！"
        return jsonify(data)
    if myfile and allowed_file(myfile.filename):
        file_name = myfile.filename.rsplit('.', 1)[0]
        data['status'] = True
        data['file_name'] = str(file_name)
        return jsonify(data)
    data['desc'] = "文件类型不支持!"
    return jsonify(data)

'''Error Tips'''
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_interval(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
    # app.run()