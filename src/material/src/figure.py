# -*- coding:UTF-8 -*-

import os, re
from .config import figure_jar_dir, figure_jar, figure_out_dir
from xml.dom.minidom import parse
import xml.dom.minidom

image_class = 'edu.isi.bmkeg.lapdf.bin.ExtractFigureImagesFromFile'
text_class = 'edu.isi.bmkeg.lapdf.bin.Blockify'
out_arg = '-outDir'
pdf_arg = '-pdf'
stem_arg = "-stem"
cmd_list = ['java', '-cp', figure_jar]

def extract_figure(filename, pdf_path):
    out_dir = os.path.join(figure_out_dir, filename)
    new_cmd_list = cmd_list[:]
    new_cmd_list.append(image_class)
    new_cmd_list.append(out_arg)
    new_cmd_list.append(out_dir)
    new_cmd_list.append(pdf_arg)
    new_cmd_list.append(pdf_path)
    new_cmd_list.append(stem_arg)
    new_cmd_list.append('f')
    new_cmd = ' '.join(new_cmd_list)
    print(new_cmd)
    os.chdir(figure_jar_dir)
    os.system(new_cmd)

def extract_figure_caption(filename, pdf_path):
    out_dir = os.path.join(figure_out_dir, filename)
    new_cmd_list = cmd_list[:]
    new_cmd_list.append(text_class)
    new_cmd_list.append(pdf_path)
    new_cmd_list.append(out_dir)
    new_cmd = ' '.join(new_cmd_list)
    print(new_cmd)
    os.chdir(figure_jar_dir)
    os.system(new_cmd)

def get_figure_caption(filename):
    out_dir = os.path.join(figure_out_dir, filename)
    xml_file_path = os.path.join(out_dir, filename[:-4]+'_lapdf.xml')
    try:
        DOMTree = xml.dom.minidom.parse(xml_file_path)
        paper = DOMTree.documentElement
        words_list = paper.getElementsByTagName("words")
        all_figure_result = []
        all_captions = []
        for words in words_list:
            wd_list = words.getElementsByTagName('wd')
            if len(wd_list) > 0:
                first_wd = wd_list[0]
                if 'Fig' in first_wd.getAttribute('t'):
                    caption_word_list = []
                    for wd in wd_list:
                        caption_word_list.append(wd.getAttribute('t'))
                    caption = ' '.join(caption_word_list)
                    all_captions.append(caption)
        for caption in all_captions:
            fig_num = caption.split()[1]
            if re.match('\d+(:|.|,)', fig_num):
                fig_num = re.split(r'[:|.|,]', fig_num)[0]
                fig_file_name = 'f_fig_'+fig_num+'.png'
                fig_page_file_name = 'f_fig_'+fig_num+'_page.png'
                if os.path.exists(os.path.join(out_dir, fig_file_name)) and \
                    os.path.exists(os.path.join(out_dir, fig_page_file_name)):
                    all_figure_result.append(
                        (fig_num,
                         caption,
                         fig_file_name,
                         fig_page_file_name)
                        )
        return all_figure_result
    except Exception:
        return False

