from bs4 import BeautifulSoup
import requests
from dataHarvesting import get_page_data as gpd, properties_file as pf
from featureEngineering import feature_file as ff
from dataHarvesting import main_file as mf

main_url = pf.url
page_names = {}
done = []
headers = pf.headers
login_data = pf.login_data

todo = list(gpd.get_page_data(main_url, pf.time_stamp + '_homepage'))

while len(todo) != 0:
    fullLink = todo.pop(0)
    currentItem = fullLink.split('?')[0]
    searchQuery = fullLink.split('?')[1]
    if pf.host not in currentItem:
        host = pf.host
        fullLink = fullLink.replace('/', '', 1)
    else:
        host = ''

    if currentItem in done:
        page_names[currentItem].append(searchQuery)
    else:
        with requests.Session() as ss:
            if pf.login_flag:
                response = ss.get(pf.login_pg_url, headers=headers)
                soup = BeautifulSoup(response.content, 'html.parser')
                login_data[pf.token_name] = soup.find('input', id=pf.token_id)['value']
                ss.post(pf.login_pg_url, data=login_data, headers=headers)
            response = ss.get(host + fullLink, headers=headers, allow_redirects=False)
        if str(response.status_code) == '200' or str(response.status_code) == '302':
            new_links = list(gpd.get_page_data(host + fullLink, pf.time_stamp + '_' + fullLink.split('?')[0]))

        page_names[currentItem] = [searchQuery]
        done.append(currentItem)
        todo += new_links

mf.file_writer(ff.file_col_dict, 'fileColumns_dict', 'json')









