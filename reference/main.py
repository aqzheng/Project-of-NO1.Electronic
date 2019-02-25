# -- coding: utf-8 --
import sys,os,re,datetime
import pymysql
import nltk.tokenize as tk
from bs4 import BeautifulSoup
from nltk.tokenize import WordPunctTokenizer
database_MirrorFileInfo = "MirrorFileInfo"
database_Citation = "Citation"
database_FrameworkContent = "FrameworkContent"

def debug(LIST):
    if isinstance(LIST, list):
        for sentence in LIST:
            print (sentence)
    else:
        print (LIST)

def extract_citation_list(soup):
    """
    :param soup: beautifulsoup 对象
    :return: 引文的三元组列表 （引文的全部信息，引文标题，引文在数据库中的id）
    """
    citation_list = []
    for ref in soup.find_all('ref'):
        Reference = ' '.join(ref.get_text().split())
        for title_soup in soup.find_all('article-title'):
            citation_title = title_soup.get_text()
            if citation_title == 'and':
                continue
            if citation_title in Reference:
                citation_list.append((Reference, citation_title))
                break

    return citation_list

def extract_sentences(soup,paper_id,paper_title,citation_list):
    sentence_contain = dict()
    for st in soup.find_all('xref'):
        Reference = st.get_text().replace('\n',' ').replace('et al.','et al')
        #continue
        refs = st.get_text().replace('\n',' ').replace('(','').replace(')','').replace('[','').replace(']','').split(';')
        #debug(refs)
        for ref in refs:
            citation = find_citation(ref, citation_list)
            #debug(citation)
            if citation == None:
                continue

            fa = st.find_parent()
            paragraph = ' '.join(fa.get_text().split()).replace('et al.','et al')
            #debug(paragraph)
            tokens = tk.sent_tokenize(paragraph)
            if ref[0].isdigit():
                regular = '\[[0-9 ,]*' + ref + '[0-9 ,]*\]'
                for sentence in tokens:
                    if re.search(regular, sentence) != None:
                        min_lenth_sentence = sentence[0:min(14, len(sentence))]
                        if min_lenth_sentence in sentence_contain:
                            if ref not in sentence_contain[min_lenth_sentence]:
                                sentence_contain[min_lenth_sentence].append(ref)
                                insert_into_Citation(paper_id,paper_title,0, citation,sentence)
                                break
                        else:
                            sentence_contain[min_lenth_sentence] = list(ref)
                            insert_into_Citation(paper_id, paper_title,0, citation, sentence)
                            break
            else:
                for sentence in tokens:
                    if Reference in sentence:
                        min_lenth_sentence = sentence[0:min(14, len(sentence))]
                        if min_lenth_sentence in sentence_contain:
                            if ref not in sentence_contain[min_lenth_sentence]:
                                sentence_contain[min_lenth_sentence].append(ref)
                                insert_into_Citation(paper_id, paper_title,0, citation, sentence.replace('et al','et al.'))
                                break
                        else:
                            sentence_contain[min_lenth_sentence] = list(ref)
                            insert_into_Citation(paper_id, paper_title,0, citation, sentence.replace('et al','et al.'))
                            break

def clean_ref(ref):
    """
    清洗从文章中搜索到的引用，以便在引文列表中搜索
    :param ref: 未清洗的引用 
    :return: 清洗后的引用
    """
    for i in range(len(ref) - 1, -1, -1):
        if ref[i][0].isdigit():
            continue
        elif ref[i][0].isalpha():
            if ref[i] == 'et' or ref[i] == 'al':
                ref.pop(i)
        else:
            ref.pop(i)
    if ref[0].isdigit():
        for num in range(len(ref)):
            s = '[' + ref[num] + ']'
            ref[num] = s
    return ref

def find_citation(ref,citation_list):
    """
    :param ref: 文章中的引用
    :param citation_list: 引文列表
    :return: 从引文列表中找到引用的文章id
    """
    ref = WordPunctTokenizer().tokenize(ref)
    ref = clean_ref(ref)
    num = len(ref)
    for citation in citation_list:
        tot = 0
        for words in ref:
            if words in citation[0]:
                tot = tot + 1
        if tot == num :
            return citation[1]
    return None

def insert_into_Citation(paper_id,paper_title,reference_id,reference_title,reference_sentence):

    try:
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql_insert = 'INSERT INTO %s (docid,title,reference_id,reference_paper,reference_sentence,finish_time,bool_check) VALUES (%d,"%s",%d,"%s","%s","%s",0)' % (
            database_Citation,paper_id, paper_title, reference_id, reference_title, reference_sentence,dt)
        cursor.execute(sql_insert)
        connect.commit()
    except Exception as e:
        connect.rollback()

def insert_into_FrameworkContent(paper_id,paper_title,subsequence,subtitle,content):

    try:
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql_insert = 'INSERT INTO %s (docid,title,subsequence,subtitle,content,finish_time,bool_check) VALUES (%d,"%s",%d,"%s","%s","%s",0)' % (
            database_FrameworkContent,paper_id, paper_title, subsequence, subtitle, content,dt)
        cursor.execute(sql_insert)
        connect.commit()
    except Exception as e:
        connect.rollback()

def insert_into_MirrorFileInfo(paper_id,paper_title,author,organization):
    try:
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql_insert = 'INSERT INTO %s (docid,title,type,finish_time,contributor,organization,bool_check) VALUES (%d,"%s",1,"%s","%s","%s",0)' % (
            database_MirrorFileInfo, paper_id, paper_title, dt, author, organization)
        cursor.execute(sql_insert)
        connect.commit()
    except Exception as e:
        connect.rollback()

def extract_Info(soup,paper_id,paper_title):
    author = soup.find('string-name')#.get_text()
    if author !=None:
        author = author.get_text()
    organization = soup.find('institution')#.get_text()
    if organization != None:
        organization = organization.get_text()
    insert_into_MirrorFileInfo(paper_id,paper_title,author,organization)

def extract_text(soup, paper_id, paper_title):
    subsequence = 0

    for st in soup.find_all(name='sec',attrs={"id":re.compile(r"sec-[0-9]+$")}):
        subsequence = subsequence + 1
        subtitle = st.get_text().strip().split('\n')[0]
        content = ' '.join(st.get_text().split())
        insert_into_FrameworkContent(paper_id,paper_title,subsequence,subtitle,content)

def extract_citation(soup,paper_id,paper_title):

    citation_list = extract_citation_list(soup)
    #debug(citation_list)
    extract_sentences(soup,paper_id,paper_title,citation_list)

def solve(xml_path):
    xmlfile = open(xml_path, 'r',encoding='utf8')
    htmlhandle = xmlfile.read()
    soup = BeautifulSoup(htmlhandle, "html.parser")

    paper_id = int(os.path.basename(xml_path).split('.')[0])
    paper_title = soup.find('article-title')
    if paper_title != None:
        paper_title = paper_title.get_text()
        extract_Info(soup,paper_id,paper_title)
        extract_text(soup,paper_id,paper_title)
        extract_citation(soup,paper_id,paper_title)
        xmlfile.close()

def gci(filepath):
    if os.path.isfile(filepath):
        if os.path.splitext(filepath)[1]=='.cermxml':
            solve(filepath)
    else:
        files = os.listdir(filepath)
        for fi in files:
            fi_d = os.path.join(filepath, fi)
            if os.path.isdir(fi_d):
                gci(fi_d)
            elif os.path.splitext(fi)[1]=='.cermxml':
                solve(fi_d)

if __name__ == "__main__":

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
    path = sys.argv[1]
    gci(path)
    connect.close()

