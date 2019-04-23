# -*- coding:UTF-8 -*-

from .config import *
from xml.dom.minidom import parse
import xml.dom.minidom
import os

def get_dir_path(source_dir):
    for root, dirnames, filenames in os.walk(source_dir):
        for dirname in dirnames:
            yield dirname, os.path.join(root, dirname)

def get_file_path(source_dir):
    for root, dirnames, filenames in os.walk(source_dir):
        for dirname in dirnames:
            get_file_path(dirname)
        for filename in filenames:
            if filename.endswith('.pdf'):
                yield filename, os.path.join(root, filename)

def get_paper_title(xml_file_path):
    try:
        DOMTree = xml.dom.minidom.parse(xml_file_path)
        paper = DOMTree.documentElement
        paper_title = paper.getElementsByTagName("article-title")[0].childNodes[0].data
        if paper_title:
            return paper_title
        else:
            return False
    except Exception:
        return False


def get_paper_abstract(xml_file_path):
    try:
        DOMTree = xml.dom.minidom.parse(xml_file_path)
        paper = DOMTree.documentElement
        paper_abstract = paper.getElementsByTagName("abstract")[0].getElementsByTagName("p")[0].childNodes[0].data
        print(paper_abstract)
        if paper_abstract:
            return paper_abstract
        else:
            return False
    except Exception:
        return False