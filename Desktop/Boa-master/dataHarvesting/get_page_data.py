import csv
import re
from dataHarvesting import main_file as mf, properties_file as pf
from featureEngineering import feature_file as ff
# import time
# import datetime
# from bs4 import BeautifulSoup
# from lxml import html, etree
import xml.etree.ElementTree as eT
import pandas as pd

dom_list = []


def count_parent_func(elem, func, level=0):
    func(elem, level)
    for child in elem.getchildren():
        count_parent_func(child, func, level+1)


def print_level(elem, level):
    dom_list.append([str(level) + ',' + eT.tostring(elem).decode('utf8')])
    return dom_list


def get_page_data(url, file_name):
    html_dom = mf.fetch_page_data(url, pf.login_flag)
    html_str = str(html_dom).replace('xlink:', '')

    # This code is to write file in json format
    # js = mf.HTMLtoJSONParser.to_json(html_str)
    # page_data = {
    #         'Date': datetime.datetime.fromtimestamp(time.time()).strftime(pf.time_stamp_format),
    #         'Url': url,
    #         'PageData_json': js,
    #         'PageData_Str': html_str
    #     }
    #
    # mf.file_writer(page_data, mf.file_directory(file_name) + file_name.replace('/', '_').replace(':', '_')
    #                .replace('-', '').replace('.', ''), pf.file_type)

    file_path_xhtml = mf.file_writer(html_str, mf.file_directory(file_name) + file_name.replace('/', '_')
                                     .replace(':', '_').replace('-', '').replace('.', ''), 'xhtml')
    root = eT.parse(file_path_xhtml + '.xhtml')
    count_parent_func(root.getroot(), print_level)
    mf.file_writer(dom_list, mf.file_directory(file_name) + file_name.replace('/', '_').replace(':', '_')
                   .replace('-', '').replace('.', ''),
                   'csv')

    csv_data = pd.read_csv(file_path_xhtml + '.csv')
    for name in csv_data.iteritems():
        name_list = list(name)
        edited_name_list = []
        for n in name_list:
            a = re.sub("ns[\d*]:", "", str(n))
            edited_name_list.append(a)
        name_tuple = tuple(edited_name_list)
        with open(file_path_xhtml + 'f' + '.csv', 'a') as csvFile:
            file = csv.writer(csvFile)
            file.writerow(name_tuple)
    df = pd.read_csv(file_path_xhtml + 'f' + '.csv', header=None)
    df.rename(columns={0: 'Dom_Content', 1: 'Description'}, inplace=True)

    df.to_csv(file_path_xhtml + 'f' + '.csv', index=False)
    # To write formetted data in excel file
    # df_formated = pd.read_csv(file_path_xhtml+ 'formated' +'.csv')
    # Excel_writer = pd.ExcelWriter(file_path_xhtml+'.xlsx')
    # df_formated.to_excel(Excel_writer, index=False)
    # Excel_writer.save()
    dom_list.clear()

    ff.feature_columns(file_path_xhtml + 'f')

    return mf.gather_page_links(html_dom.find_all(pf.link_tag))









