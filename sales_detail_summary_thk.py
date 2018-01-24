import pandas as pd
import numpy as np


def sales_detail(inputfile, outputfile):
    data_frame = pd.read_excel(inputfile, sheet_name= 'Data') #read data

    sum_value = data_frame.groupby(['Country','Offsetting Account Name','Document currency'],as_index = False)['Amount in doc. curr.',\
                'Amount in local currency'].sum() #sum of value base on condition in other column

    country_value = data_frame.groupby(['Country','Document currency'])['Amount in doc. curr.',\
                'Amount in local currency'].sum() #sum of value base on condition in other column

    sum_value['JPY'] = np.where(sum_value['Document currency'] == 'JPY', sum_value['Amount in doc. curr.'], 0)
    #add column base on condition in other column

    sum_value['USD'] = np.where(sum_value['Document currency'] == 'USD', sum_value['Amount in doc. curr.'], 0)
    #add column base on condition in other column

    sum_value.loc['Total'] = sum_value.sum(numeric_only = True) #add row for the tatol of numeric columns
    del sum_value['Amount in doc. curr.']

    sum_value['SGD'] = sum_value['Amount in local currency']
    del sum_value['Amount in local currency']

    sum_value = sum_value[['Country','Offsetting Account Name','Document currency','JPY','USD','SGD']]

    write_excel = pd.ExcelWriter(outputfile) #output the result to excel file
    sum_value.to_excel(write_excel, 'sheet1')
    country_value.to_excel(write_excel, 'sheet2')

    write_excel.save()

inputfile = 'Sales Detail Dec17.XLSX'
outputfile = 'sales_detail.xlsx'

sales_detail(inputfile, outputfile)