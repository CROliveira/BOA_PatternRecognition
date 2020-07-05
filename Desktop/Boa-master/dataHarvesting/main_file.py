from bs4 import BeautifulSoup
from dataHarvesting import properties_file as pf
import requests
import json
import csv
import html
import os
import lxml
import lxml.html
import lxml.etree


def fetch_page_data(url, login_flag):
    headers = pf.headers
    login_data = pf.login_data
    with requests.Session() as s:
        if login_flag:
            response = s.get(pf.login_pg_url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            login_data[pf.token_name] = soup.find('input', id=pf.token_id)['value']
            s.post(pf.login_pg_url, data=login_data, headers=headers)
        response = s.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        html_home = soup.html
    return html_home


class HTMLtoJSONParser(html.parser.HTMLParser):
    def __init__(self, raise_exception=True):
        html.parser.HTMLParser.__init__(self)
        self.doc = {}
        self.path = []
        self.cur = self.doc
        self.line = 0
        self.raise_exception = raise_exception

    @property
    def json(self):
        return self.doc

    @staticmethod
    def to_json(content, raise_exception=True):
        parser = HTMLtoJSONParser(raise_exception=raise_exception)
        parser.feed(content)
        return parser.json

    def handle_starttag(self, tag, attrs):
        self.path.append(tag)
        attrs = {k: v for k, v in attrs}
        if tag in self.cur:
            if isinstance(self.cur[tag], list):
                self.cur[tag].append({"__parent__": self.cur})
                self.cur = self.cur[tag][-1]
            else:
                self.cur[tag] = [self.cur[tag]]
                self.cur[tag].append({"__parent__": self.cur})
                self.cur = self.cur[tag][-1]
        else:
            self.cur[tag] = {"__parent__": self.cur}
            self.cur = self.cur[tag]

        for a, v in attrs.items():
            self.cur["#" + a] = v
        self.cur[""] = ""

    def handle_endtag(self, tag):
        if tag != self.path[-1] and self.raise_exception:
            raise Exception(
                "html is malformed around line: {0} (it might be because of a tag <br>, <hr>, <img .. > not closed)".format(
                    self.line))
        del self.path[-1]
        memo = self.cur
        self.cur = self.cur["__parent__"]
        self.clean(memo)

    def handle_data(self, data):
        self.line += data.count("\n")
        if "" in self.cur:
            self.cur[""] += data

    def clean(self, values):
        keys = list(values.keys())
        for k in keys:
            v = values[k]
            if isinstance(v, str):
                # print ("clean", k,[v])
                c = v.strip(" \n\r\t")
                if c != v:
                    if len(c) > 0:
                        values[k] = c
                    else:
                        del values[k]
        del values["__parent__"]


def gather_page_links(lists):
    link_set = set()
    for link in lists:
        href = str(link.get('href'))
        if href == '#' or href == '/' or href.lower() == 'none' or 'mailto:' in href.lower() \
                or (href.split(':')[0] == 'http' and pf.host not in href) \
                or (href.split(':')[0] == 'https' and pf.host not in href) or 'sampleCsvDownload' in href \
                or '.pdf' in href or 'javascript' in href or (pf.local_host and pf.address not in href):
            continue
        else:
            if "?" in href:
                current_item = href.split('?')[0]
                search_query = href.split('?')[1]
            else:
                current_item = href
                search_query = ''
            pf.link_dict[current_item] = search_query
    for current_item, search_query in pf.link_dict.items():
        if current_item != '':
            link_set.add(current_item.strip() + '?' + search_query.strip())
    return link_set


def file_writer(data, file_name, file_type):
    file_name = file_name.split('_')[0] + '_' + (file_name.split('_')[-1] if file_name.split('_')[-1] != ''
                                                 else file_name.split('_')[-2])
    if 'csv' == file_type:
        with open(file_name + ".csv", 'w') as csvFile:
            file = csv.writer(csvFile)
            file.writerow(data)
        csvFile.close()
    elif 'txt' == file_type:
        with open(file_name + ".txt", 'w') as txtFile:
            txtFile.write(data)
        txtFile.close()
    elif 'xhtml' == file_type:
        html_dom = lxml.html.fromstring(data)
        xhtml_file = open(file_name + '.xhtml', 'wb')
        xhtml_file.write(lxml.etree.tostring(html_dom))
        xhtml_file.close()
    elif 'json' == file_type:
        with open(file_name + '.json', 'w') as jsonFile:
            json.dump(data, jsonFile, indent=1)
        jsonFile.close()
    else:
        print(file_type + ' is not a valid file type')
    return file_name


def file_directory(file_name):
    os.chdir(pf.folder_directory)
    if '_homepage' in file_name:
        dl_path = 'nest\\' + \
                  pf.url.split('//')[1] + '\\' + 'Home' + '\\'
        if not os.path.exists(dl_path):
            os.makedirs(dl_path)
    else:
        dl_path = 'nest\\' + \
                  pf.url.split('//')[1] + '\\' + str(file_name).split('_')[1].replace(':', '').replace('//', '.') + "\\"
        if not os.path.exists(dl_path):
            os.makedirs(dl_path)

    return dl_path
