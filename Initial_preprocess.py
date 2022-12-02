import pandas as pd
import numpy as np
from Functions import get_features, get_metro, get_area, condition_windows, condition_furniture


df1 = pd.read_excel(r'C:\Users\slava\PycharmProjects\pythonProject6\venv\Вторичка_студии_1к _2.xlsx')
df2 = pd.read_excel(r'C:\Users\slava\PycharmProjects\pythonProject6\venv\Вторичка_234 _2.xlsx')

data = pd.concat([df1, df2])
data = data.drop_duplicates()
data = data.reset_index(drop = True)

parameters = ['Количество комнат', 'Общая площадь', 'Площадь кухни', 'Жилая площадь',
 'Этаж','Высота потолков', 'Санузел', 'Окна', 'Ремонт', 'Мебель']
parameters2 = ['Тип дома', 'Год постройки']
#for primary
# parameters2 = ['Тип дома']

# get features from raw columns
data = get_features(parameters, data, 'Description')
data = get_features(parameters2, data, 'House_info')
data = get_metro(data, 'Metro')

#get year the house was built in - ONLY FOR SECONDARY MARKET
data['Год постройки'] = data['Год постройки'].astype('Int64')
data['Год постройки'] = data['Год постройки'].apply(lambda row:  2022 - row)
data.rename(columns = {'Год постройки': 'House_age'})

#FOR PRIMARY MARKET
# data['Год постройки'] = 2022

#strip m^2
data = get_area(data, ['Общая площадь', 'Площадь кухни', 'Жилая площадь', 'Высота потолков'])

#floors
data['Total_floors'] = data['Этаж'].apply(lambda row: row.split(' ')[3])
data['Floor'] = data['Этаж'].apply(lambda row: row.split(' ')[1])

#windows
data['Окна'] = data['Окна'].apply(condition_windows)

#furniture
data['Мебель'] = data['Мебель'].apply(condition_furniture)

#assigning secondary or primary market label
data['Housing_type'] = 'Secondary'

#location
data['Location'] = data['Location'].apply(lambda row: row[17:])

data.drop(['Unnamed: 0', 'Title', 'Description', 'Metro', 'House_info', 'Этаж'], inplace = True, axis =1)

data.to_excel('Secondary_stage1_batch2.xlsx')

pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 28)
print(data.head(10))