import re
import pandas as pd
def get_features(parameters, data, column):
    dataf = data.copy()
    for ind, val in enumerate(data[column]):
        feature_list = [i.split(':') for i in data[column].iloc[ind].split('\n')]
        for i in parameters:
            for j in feature_list:
                if i == j[0]:
                    dataf.at[ind, i] = j[1]
    return dataf

def get_metro(data, column):
    dataf = data.copy()
    for ind, val in enumerate(data[column]):
        time_metro = re.findall(r'\d+', data[column][ind])
        if 'мин' in val:
            if len(time_metro) == 2:
                dataf.at[ind, 'time_to_metro'] = (int(time_metro[0]) + int(time_metro[1])) / 2
            else:
                dataf.at[ind, 'time_to_metro'] = int(time_metro[0])
        else:
            dataf.at[ind, 'time_to_metro'] = None
    return dataf

def get_area(data, col_list):
    for i in range(len(col_list)):
        data[col_list[i]] = data[col_list[i]].apply(lambda row: row if pd.isnull(row) else row.split(' ')[1])
    return data

def condition_windows(x):
    if x == ' во двор, на солнечную сторону':
        return ' во двор'
    elif x ==  'на улицу, на солнечную сторону':
        return ' на улицу'
    elif x == ' во двор, на улицу, на солнечную сторону':
        return ' во двор, на улицу'
    elif x == ' на солнечную сторону':
        return None
    else:
        return x

def condition_furniture(x):
    if x == ' кухня, хранение одежды, спальные места' or x == ' кухня, хранение одежды' or x == ' кухня, спальные места':
        return 'furnished'
    elif x ==' кухня':
        return 'kitchen_only'
    elif x == ' хранение одежды, спальные места' or x == ' спальные места' or x == ' хранение одежды':
        return 'no_kitchen'
    else:
        return None