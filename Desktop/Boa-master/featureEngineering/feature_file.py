import pandas as pd
import re


attributes_dict = {}
tags = set()
class_dummy = set()
class_dummy_col_set = set()
file_path_set = set()
attribute_col_name_set = set()
file_col_dict = {}


def main_tag(tag):
    return re.findall('<.*?>', str(tag))


def find_digit(tag):
    return re.findall('\d*', tag)


def attributes_regex(tag):
    return re.findall("(?<=\s)[\w]*=['\"]+[^'\"]*['\"]+(?=>|\s)", str(tag))


def attribute_name(value):
    split_regex = re.compile("=['\"]").split(value)
    attr_name = split_regex[0]
    return attr_name


def attribute_value(value):
    split_regex = re.compile("=['\"]").split(value)
    attr_value = re.sub("['\"]", "", split_regex[1])
    return attr_value


def no_of_parents(tag):
    return re.findall("'.*?,", str(tag))


def binary_to_decimal(binary):
    return int(binary, 2)


def feature_columns(file_name):
    data = pd.read_csv(file_name + ".csv")
    df = pd.DataFrame(data)
    df = df.drop(columns='Description')
    df['Parent_Count'] = df['Dom_Content'].apply(no_of_parents).str[0].str.replace("'", "").str.replace(",", "")
    df['Full_Content'] = df['Dom_Content'].str.split(',', 1).str[1].str.replace("']", '').str.strip()
    df = df.drop(columns='Dom_Content')
    df['Char_Count'] = df['Full_Content'].str.len()
    df['Main_Tag'] = df['Full_Content'].apply(main_tag).str[0]
    df['Main_Tag_Char_Count'] = df['Main_Tag'].str.len()
    df['Main_Tag_Name'] = df['Main_Tag'].str.split().str[0].str.replace('<', '').str.replace('>', '')
    df['Main_Tag_Attributes'] = df['Main_Tag'].apply(attributes_regex)
    for index, row in df.iterrows():
        tags.add(row['Main_Tag_Name'])
    for tag in tags:
        df['Tag_Count_' + str(tag)] = df['Full_Content'].str.count('<' + str(tag) + '>|<' + str(tag) + ' ')
    df = df.drop(columns='Full_Content')
    for v in df['Main_Tag_Attributes']:
        for val in v:
            attribute_column_name = attribute_name(val)
            attribute_column_value = attribute_value(val)
            attribute_col_name_set.add('Attr_' + attribute_column_name)
            if attribute_column_name not in attributes_dict.keys():
                attributes_dict[attribute_column_name] = attribute_column_value
                df['Attr_' + attribute_column_name] = ""
    for i in range(0, df.shape[0]):
        for v in df.at[i, 'Main_Tag_Attributes']:
            attribute_column_name = attribute_name(v)
            attribute_column_value = attribute_value(v)
            df.at[i, 'Attr_' + attribute_column_name] = attribute_column_value
            if attribute_column_name == 'class':
                class_dummy.update(set(attribute_column_value.split()))
                for dummy in class_dummy:
                    if dummy in set(attribute_column_value.split()):
                        df.at[i, 'Attribute_Value_' + str(dummy)] = "1"
                    else:
                        df.at[i, 'Attribute_Value_' + str(dummy)] = "0"
                    df['Attribute_Value_' + str(dummy)].fillna(value="0", inplace=True)
                    class_dummy_col_set.add('Attribute_Value_' + str(dummy))
    class_dummy_col_list = list(class_dummy_col_set)
    df['Merged_Binary_Value'] = df[class_dummy_col_list].apply(lambda x: ' '.join(x), axis=1)
    for index, row in df.iterrows():
        bin_to_dec = binary_to_decimal(row['Merged_Binary_Value'].replace(" ", ""))
        df.at[index, 'Class_Dummy_Decimal_Value'] = bin_to_dec
    file_path = file_name.replace("/\\", "\\").replace("/", "\\")
    file_path_set.add(file_path)
    file_col_dict[file_path] = list(attribute_col_name_set)
    attribute_col_name_set.clear()
    class_dummy.clear()
    class_dummy_col_set.clear()
    class_dummy_col_list.clear()
    tags.clear()
    df.to_csv(file_name + ".csv")
