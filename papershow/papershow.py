# -*- coding: utf-8 -*-
import os
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

@app.route('/metadata')
def metadata_view():
    return render_template("metadata.html")

@app.route('/quotation')
def quotation_view():
    return render_template("quotation.html")

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

"""quotation part"""
from quotation_query import get_reference, get_paper_id1
@app.route('/quotation/qquery', methods=['POST'])
def qquery_view():
    data = {}
    file_name = request.form.get('file_name')
    print(file_name)
    data['file_name'] = file_name
    data['paper_id'] = str(get_paper_id1(file_name))
    data['reference'] = get_reference(file_name)
    print(data['paper_id'])
    print(data['reference'])
    if len(data['reference']) == 0:
        data['status'] = False
        print("NO DATA ERROR!")
    else:
        data['status'] = True
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
    app.run(debug=True)
    #app.run(host='0.0.0.0', port=80)