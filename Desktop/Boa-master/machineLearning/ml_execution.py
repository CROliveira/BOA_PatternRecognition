from machineLearning import imports as ip
from machineLearning import ml_algorithm
import json
from collections import OrderedDict

'''
Execution steps:
 1. Run with concate_flag and all_labels as False and execution_flag as True
 2. Run with concate_flag as True. 
 3. Run with concate_flag, all_labels and execution_Flag as False
 4. Repeat steps 2 and 3 by changing file_to_predict until all labels are corrected and covered in train file
 5. Run with concate_flag and execution_flag as False and all_labels flag as True
'''


all_labels = True  # True(when executing all files in single run) or False(when executing individual files)
concate_flag = False  # True(When merging files to train the model)

with open(ml_algorithm.project_dir + "\\fileColumns_dict.json", 'r') as JSON:
    filePath_mapping_dict = OrderedDict(json.load(JSON))

if not concate_flag:
    if all_labels:
        file_name = '201906211104_changeUserPasswordf'  # File with manual labels
        for key, value in filePath_mapping_dict.items():
            if file_name not in key:
                filePath_to_predict = key
                labelled_file_cols = value
                labelled_file_cols.append('Main_Tag_Name')
                labelled_file_cols.append('Main_Tag_Attributes')
                file_to_predict = ml_algorithm.project_dir + "\\" + filePath_to_predict + ".csv"
                predicted_file = ml_algorithm.project_dir + "\\" + filePath_to_predict + "1.csv"
                f = open('predicted_file_dir.txt', 'w')
                f.write(predicted_file)
                f.close()
                y_pred = ml_algorithm.ml_algorithm(file_to_predict, labelled_file_cols, predicted_file, False) # always False as train file is already preprocessed
                print(y_pred)
    else:
        file_name = '201906211104_nationalityf'  # file to predict labels when running individually
        for key in filePath_mapping_dict:
            if file_name in key:
                filePath_to_predict = key
                labelled_file_cols = filePath_mapping_dict.get(key)
                labelled_file_cols.append('Main_Tag_Name')
                labelled_file_cols.append('Main_Tag_Attributes')
                file_to_predict = ml_algorithm.project_dir + "\\" + filePath_to_predict + ".csv"
                predicted_file = ml_algorithm.project_dir + "\\" + filePath_to_predict + "1.csv"
                f = open('predicted_file_dir.txt', 'w')
                f.write(predicted_file)
                f.close()
                y_pred = ml_algorithm.ml_algorithm(file_to_predict, labelled_file_cols, predicted_file, False)  # True(When predicting labels for the first file otherwise always False)
                print(y_pred)
else:
    f = open("predicted_file_dir.txt", "r")
    predicted_fileName = f.read()

    train1 = ip.pd.read_csv(ml_algorithm.merged_labelled_file)
    train2 = ip.pd.read_csv(predicted_fileName)

    train = ip.pd.concat([train1, train2])

    train.to_csv(ml_algorithm.merged_labelled_file, index=False)


