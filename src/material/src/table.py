# -*- coding:UTF-8 -*-

import os, re
from .config import table_jar_dir, table_jar, table_out_dir
from xml.dom.minidom import parse
import xml.dom.minidom

table_class = 'edu.psu.seersuite.extractors.tableextractor.extraction.BatchExtractor'
cmd_list = ['java', '-cp', table_jar, table_class]

number_map = ['0','I','II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI']

def extract_table(dirname, dir_path):
    out_dir = os.path.join(table_out_dir, 'task_'+dirname)
    new_cmd_list = cmd_list[:]
    new_cmd_list.append(dir_path)
    new_cmd_list.append(out_dir)
    new_cmd_list.append('pdfbox')
    new_cmd = ' '.join(new_cmd_list)
    print(new_cmd)
    os.chdir(table_jar_dir)
    os.system(new_cmd)

def get_table_caption(task_id, filename, file_path):
    xml_file_path = os.path.join(table_out_dir, 'task_'+task_id, 'xml')
    # xml_file_path = re.sub('pdf_file', 'material_results/table_out', file_path)
    xml_file_path = os.path.join(xml_file_path, filename[:-4]+'.xml')
    print(xml_file_path)
    try:
        DOMTree = xml.dom.minidom.parse(xml_file_path)
        paper = DOMTree.documentElement
        caption_list = paper.getElementsByTagName("caption")
        all_table_result = []
        all_captions = []
        for caption in caption_list:
            all_captions.append(caption.childNodes[0].data)
        print(all_captions)
        for caption in all_captions:
            table_num = caption.split()[1]
            if re.match('\d+(:|.|,)', table_num):
                table_num = re.split(r'[:|.|,]', table_num)[0]
                table_file_name = filename[:-4]+'.xml'
                all_table_result.append(
                        (table_num,
                         caption,
                         table_file_name,
                         xml_file_path)
                        )
            else:
                table_num = number_map.index(table_num)
                table_file_name = filename[:-4] + '.xml'
                all_table_result.append(
                    (table_num,
                     caption,
                     table_file_name,
                     xml_file_path)
                )
        return all_table_result
    except Exception:
        return False

