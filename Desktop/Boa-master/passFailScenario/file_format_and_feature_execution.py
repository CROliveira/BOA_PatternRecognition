import re
import csv
import os
import lxml
import lxml.html
import lxml.etree
import xml.etree.ElementTree as eT
from passFailScenario import features as f_file

import pandas as pd

dom_list = []
unique_diff_files_list = []
current_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = current_dir.rsplit('\\', 1)[0]
curr_diff_col_set = set()
hist_diff_col_set = set()
final_col_set = set()


def fetch_file_path_list(sub_dir_name):
    dir_name = project_dir + '\\' + sub_dir_name
    list_of_files = list()
    for (dir_path, dir_names, file_names) in os.walk(dir_name):
        list_of_files += [os.path.join(dir_path, file) for file in file_names ]
    return list_of_files


def file_writer(data, file_name, file_type):
    if 'csv' == file_type:
        with open(file_name + ".csv", 'w') as csvFile:
            csv_file = csv.writer(csvFile)
            csv_file.writerow(data)
        csvFile.close()
    elif 'xhtml' == file_type:
        html_dom = lxml.html.fromstring(data)
        xhtml_file = open(file_name + '.xhtml', 'wb')
        xhtml_file.write(lxml.etree.tostring(html_dom))
        xhtml_file.close()
    else:
        print(file_type + ' is not a valid file type')
    return file_name


def count_parent_func(elem, func, level=0):
    func(elem, level)
    for child in elem.getchildren():
        count_parent_func(child, func, level+1)


def print_level(elem, level):
    dom_list.append([str(level) + ',' + eT.tostring(elem).decode('utf8')])
    return dom_list


def format_file(file_name):
    with open(file_name + '.txt', 'r') as data_file:
        dom_data = data_file.read()
    xhtml_file = file_writer(dom_data, file_name, 'xhtml')
    root = eT.parse(xhtml_file + '.xhtml')
    count_parent_func(root.getroot(), print_level)
    file_writer(dom_list, file_name, 'csv')
    csv_data = pd.read_csv(xhtml_file + '.csv')
    for name in csv_data.iteritems():
        name_list = list(name)
        edited_name_list = []
        for n in name_list:
            a = re.sub("ns[\d*]:", "", str(n))
            edited_name_list.append(a)
        name_tuple = tuple(edited_name_list)
        with open(xhtml_file + 'f' + '.csv', 'a') as csvFile:
            file = csv.writer(csvFile)
            file.writerow(name_tuple)
    df = pd.read_csv(xhtml_file + 'f' + '.csv', header=None)
    df.rename(columns={0: 'Dom_Content', 1: 'Description'}, inplace=True)
    df.to_csv(xhtml_file + 'f' + '.csv', index=False)
    dom_list.clear()
    os.remove(xhtml_file + ".txt")
    os.remove(xhtml_file + ".xhtml")
    os.remove(xhtml_file + ".csv")


latestPass_files_list = fetch_file_path_list('latestPass')
current_files_list = fetch_file_path_list('testData')

for latestPass_file_path in latestPass_files_list:
    if '.txt' in latestPass_file_path:
        file_path = latestPass_file_path.split('.')
        format_file(file_path[0])
        f_file.initial_feature_columns(file_path[0] + 'f')

for current_file_path in current_files_list:
    if '.txt' in current_file_path:
        file_path = current_file_path.split('.')
        format_file(file_path[0])
        f_file.initial_feature_columns(file_path[0] + 'f')


latestPass_files_list = fetch_file_path_list('latestPass')
current_files_list = fetch_file_path_list('testData')

# Code to know unique rows of curr and hist files with filename
for path_h in latestPass_files_list:
    for path_c in current_files_list:
        if '.csv' in path_h and '.csv' in path_c:
            path_h_file_name = path_h.split('\\')[len(path_h.split('\\'))-1]
            path_c_file_name = path_c.split('\\')[len(path_c.split('\\'))-1]
            if path_h_file_name == path_c_file_name:
                compare_df_1 = pd.read_csv(path_c)
                compare_df_2 = pd.read_csv(path_h)

                compare_df_1 = compare_df_1['Main_Tag']
                current_main_tag_set = set(compare_df_1)

                compare_df_2 = compare_df_2['Main_Tag']
                historic_main_tag_set = set(compare_df_2)

                unique_current_set = current_main_tag_set - historic_main_tag_set
                unique_historic_set = historic_main_tag_set - current_main_tag_set

                unique_diff_set = sorted(unique_current_set.symmetric_difference(unique_historic_set))
                unique_diff_empty_df = pd.DataFrame()
                unique_diff_empty_df['Main_Tag'] = list(unique_diff_set)
                unique_diff_empty_df['Page'] = path_h_file_name.split('.')[0]

                for index, row in unique_diff_empty_df.iterrows():
                    if row['Main_Tag'] in unique_current_set:
                        unique_diff_empty_df.at[index, 'Symm_Diff'] = "curr_minus_hist"
                    else:
                        unique_diff_empty_df.at[index, 'Symm_Diff'] = "hist_minus_curr"
                if not os.path.exists(path_h.rsplit('\\', 1)[0] + "\\unique_diff"):
                    os.makedirs(path_h.rsplit('\\', 1)[0] + "\\unique_diff")
                unique_diff_empty_df.to_csv(path_h.rsplit('\\', 1)[0] + "\\unique_diff\\" +
                                            path_h_file_name.split('.')[0] + '.csv', index=False)


'''   
Code to get unique rows of main tag            
for path_h in latestPass_files_list:
    for path_c in current_files_list:
        if '.csv' in path_h and '.csv' in path_c:
            path_h_file_name = path_h.split('\\')[len(path_h.split('\\'))-1]
            path_c_file_name = path_c.split('\\')[len(path_c.split('\\'))-1]
            if path_h_file_name == path_c_file_name:
                compare_df_1 = pd.read_csv(path_c)
                compare_df_2 = pd.read_csv(path_h)

                compare_df_1 = compare_df_1['Main_Tag']
                current_main_tag_set = set(compare_df_1)

                compare_df_2 = compare_df_2['Main_Tag']
                historic_main_tag_set = set(compare_df_2)

                unique_current_set = current_main_tag_set - historic_main_tag_set
                unique_historic_set = historic_main_tag_set - current_main_tag_set

                unique_diff_set = sorted(unique_current_set.symmetric_difference(unique_historic_set))

                unique_diff_empty_df = pd.DataFrame()

                unique_diff_empty_df['Main_Tag'] = list(unique_diff_set)

                unique_diff_empty_df = unique_diff_empty_df.sort_values(by='Main_Tag')

                if not os.path.exists(path_h.rsplit('\\', 1)[0] + "\\unique_diff"):
                    os.makedirs(path_h.rsplit('\\', 1)[0] + "\\unique_diff")
                unique_diff_empty_df.to_csv(path_h.rsplit('\\', 1)[0] + "\\unique_diff\\" +
                                            path_h_file_name.split('.')[0] + '.csv', index=False)
'''

'''
Code to get unique column names 
for path_h in latestPass_files_list:
    for path_c in current_files_list:
        if '.csv' in path_h and '.csv' in path_c:
            path_h_file_name = path_h.split('\\')[len(path_h.split('\\')) - 1]
            path_c_file_name = path_c.split('\\')[len(path_c.split('\\')) - 1]
            if path_h_file_name == path_c_file_name:
                compare_df_1 = pd.read_csv(path_c)
                compare_df_2 = pd.read_csv(path_h)

                compare_df_1 = compare_df_1['Main_Tag']
                current_main_tag_set = set(compare_df_1)

                compare_df_2 = compare_df_2['Main_Tag']
                historic_main_tag_set = set(compare_df_2)

                unique_current_set = current_main_tag_set - historic_main_tag_set
                unique_historic_set = historic_main_tag_set - current_main_tag_set

                curr_empty_df = pd.DataFrame()
                hist_empty_df = pd.DataFrame()
                curr_empty_df['Main_Tag'] = list(unique_current_set)
                hist_empty_df['Main_Tag'] = list(unique_historic_set)
                curr_empty_df = curr_empty_df.sort_values(by ='Main_Tag')
                hist_empty_df = hist_empty_df.sort_values(by='Main_Tag')
                curr_empty_df.to_csv('current_diff.csv', index=False)
                hist_empty_df.to_csv('historical_diff.csv', index=False)

                f_file.feature_columns('current_diff')
                f_file.feature_columns('historical_diff')

                curr_diff_df = pd.read_csv('current_diff.csv')
                hist_diff_df = pd.read_csv('historical_diff.csv')

                curr_diff_col_set = curr_diff_df.columns
                hist_diff_col_set = hist_diff_df.columns
                unique_col_names_set = sorted(curr_diff_col_set.symmetric_difference(hist_diff_col_set))
                if not os.path.exists(path_h.rsplit('\\', 1)[0] + "\\unique_columns"):
                    os.makedirs(path_h.rsplit('\\', 1)[0] + "\\unique_columns")
                if len(unique_col_names_set) is not 0:
                    file_writer(unique_col_names_set, path_h.rsplit('\\', 1)[0] + "\\unique_columns\\" +
                                path_h_file_name.split('.')[0], 'csv')
'''








