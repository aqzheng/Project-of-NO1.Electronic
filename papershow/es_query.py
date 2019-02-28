from elasticsearch import Elasticsearch
import os
def connect_es(ip="127.0.0.1"):
    return Elasticsearch([ip],http_auth=('zheng','zheng'),port=9202)

def query(begin_time, end_time):
    es = connect_es()
    body = {
        "query": {
            "range": {
                "fromtime": {
                    "gte": begin_time,
                    "lte": end_time,
                    "format": "yyyy-MM-dd"
                }
            }
        }
    }
    query = es.search(body=body, size=10000)
    results = query['hits']['hits']
    return results

def get_paper_num(begin_time, end_time):
    return len(query(begin_time, end_time))

def run_pipeline(begin_time, end_time):
    results=query(begin_time, end_time)
    #download_file(results,begin_time)
    process_pdf(results,begin_time)

def process_pdf(results,begin_time):
    os.system(os.path.join(os.getcwd(), 'process_pdf.bat %s %s') % (
    os.path.join(os.getcwd(), "download_file", begin_time + str("_")), len(results)/1000))

def download_file(results,begin_time):
    cwd_path = os.getcwd()
    folder_path = os.path.join(cwd_path,"download_file")
    file_block = 0
    file_num = 0
    for hit in results:
        now_file_block = os.path.join(folder_path,begin_time+str("_")+str(file_block))
        if file_num == 0:
            makedir(now_file_block)
        file_path = str('http://172.16.155.32/allpdf')+hit['_source']['file_list']

        if '.pdf' in file_path:
            file_open = requests.get(file_path)
            file_position = os.path.join(now_file_block,requests['_source']['id'])
            with open(file_position, 'wb') as file_write:
                file_write.write(file_open.content)

        file_num += 1
        if file_num == 1000 :
            file_block += 1
            file_num = 0


