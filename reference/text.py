import os,sys,re
from bs4 import BeautifulSoup
import requests

def solve(xml_path):
    xmlfile = open(xml_path, 'r',encoding='utf8')
    htmlhandle = xmlfile.read()
    soup = BeautifulSoup(htmlhandle, "html.parser")
    for st in soup.find_all('td'):
        path = 'http://172.16.155.32/allpdf/IELDVD/2018009/Disk201809-09/8421409/'+st.get_text()
        if '.pdf' in path:
            f = requests.get(path)
            now = 'D:\\final\\newpdf'
            now = os.path.join(now,st.get_text())
            with open(now,'wb') as code:
                code.write(f.content)


if __name__ == "__main__":
    solve('C:\\Users\\Administrator\\Desktop\\Index.html')