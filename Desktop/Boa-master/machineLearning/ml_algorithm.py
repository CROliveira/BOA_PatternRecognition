from machineLearning import imports as ip
import os

current_dir=os.path.dirname(os.path.realpath(__file__))
project_dir=current_dir.rsplit('\\', 1)[0]

# File with manual labels
manually_labelled_file = project_dir + "\\nest\\127.0.0.1\\orangehrm-4.3.1\\symfony\\web\\index.php\\orangehrm-4.3.1" \  
                                       "\\symfony\\web\\index.php\\admin\\changeUserPassword" \
                                       "\\201906211104_changeUserPasswordf.csv"

# manually_labelled_file + predicted_labelled_file(after correcting labels manually)
merged_labelled_file = project_dir + "\\nest\\127.0.0.1\\orangehrm-4.3.1\\symfony\\web\\index.php\\orangehrm-4.3.1" \
                                     "\\symfony\\web\\index.php\\admin\\changeUserPassword\\updated_labels_file.csv"


def ml_algorithm(file_to_predict, labelled_file_cols, predicted_file, execution_flag):
    if execution_flag:
        train = ip.pd.read_csv(manually_labelled_file)
    else:
        train = ip.pd.read_csv(merged_labelled_file)
    test = ip.pd.read_csv(file_to_predict)

    if execution_flag:
        train.fillna(value=0, inplace=True)
    test.fillna(value=0, inplace=True)

    if execution_flag:
        train_drop = train.drop(columns=['Main_Tag', 'Unnamed: 0', 'Merged_Binary_Value'])
    test_drop = test.drop(columns=['Main_Tag', 'Unnamed: 0', 'Merged_Binary_Value'])

    if execution_flag:
        categorical_features_train = ['Main_Tag_Name', 'Main_Tag_Attributes', 'Attr_autocomplete',
                                      'Attr_maxlenght', 'Attr_minlength', 'Attr_lang', 'Attr_content', 'Attr_href',
                                      'Attr_rel', 'Attr_type', 'Attr_src', 'Attr_media', 'Attr_id',
                                      'Attr_target', 'Attr_alt', 'Attr_height', 'Attr_width', 'Attr_class',
                                      'Attr_value', 'Attr_action', 'Attr_enctype',
                                      'Attr_method', 'Attr_name', 'Attr_language', 'Attr_title', 'Attr_style',
                                      'Attr_version', 'Attr_viewbox', 'Attr_x',
                                      'Attr_y', 'Attr_d', 'Attr_fill', 'Attr_attributename', 'Attr_attributetype',
                                      'Attr_dur', 'Attr_from',
                                      'Attr_repeatcount', 'Attr_to', 'Attr_onclick', 'Attr_for']

    categorical_features_test = labelled_file_cols

    if execution_flag:
        train_dummy = ip.pd.get_dummies(data=train_drop, columns=categorical_features_train, drop_first=True)
    test_dummy = ip.pd.get_dummies(data=test_drop, columns=categorical_features_test, drop_first=True)

    if execution_flag:
        train_df = train_dummy
    else:
        train_df = train

    train_columns = set(train_df.columns)
    test_columns = set(test_dummy.columns)

    all_columns = train_columns.union(test_columns)
    new_train_columns = all_columns - train_columns
    new_test_columns = all_columns - test_columns
    all_train_columns = train_columns.union(new_train_columns)
    all_test_columns = test_columns.union(new_test_columns)

    for list_item in list(all_train_columns):
        if list_item not in list(train_columns):
            train_df[list_item] = 0

    for list_item in list(all_test_columns):
        if list_item not in list(test_columns):
            test_dummy[list_item] = 0

    train_df = train_df[sorted(train_df.columns)]
    test_dummy = test_dummy[sorted(test_dummy.columns)]

    if execution_flag:
        result = train_df['Result'].astype('category', ordered=False)
        train_df['labels'] = result.cat.codes

    X_train = train_df.drop(['Result', 'labels'], axis=1)
    y_train = train_df['labels']

    if execution_flag:
        X_test = test_dummy.drop(['Result'], axis=1)
    else:
        X_test = test_dummy.drop(['Result', 'labels'], axis=1)

    scaler = ip.StandardScaler(copy=True, with_mean=True, with_std=True)
    scaler.fit_transform(X_train)
    scaler.transform(X_test)

    bernoulli = ip.BernoulliNB(alpha=0.0, binarize=0.0, fit_prior=False, class_prior=None)
    bernoulli.fit(X_train, y_train)
    y_pred = bernoulli.predict(X_test)

    test_dummy['labels'] = y_pred
    test_dummy.to_csv(predicted_file, index=False)
    train_df.to_csv(merged_labelled_file, index=False)

    return y_pred
