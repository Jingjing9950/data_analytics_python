import pandas as pd
import glob
import os
import numpy as np

#concatenate multi workbooks
def multiworkboos_concatenate(input_path, output_file):
    input_files = glob.glob(os.path.join(input_path, '*.xlsx*'))
    data_frames = []
    worksheet_names = []
    worksheet_sum = []
    worksheet_average = []
    for input_file in input_files:
        data_frame = pd.read_excel(input_file, sheet_name= None, index_col= None)
        for worksheet_name, data in data_frame.items():
            worksheet_names.append(worksheet_name)
            worksheet_sum.append(data['Sale Amount'].sum())
            worksheet_average.append(data['Sale Amount'].mean())

    print(worksheet_names)
    print(worksheet_sum)
    print(worksheet_average)

    data_frames.append(worksheet_names)
    data_frames.append(worksheet_sum)
    data_frames.append(worksheet_average)
    print(data_frames)

    data_frames = pd.DataFrame(data = data_frames, index = ['Name','Sum','Mean'], columns = np.arange(1,len(worksheet_names)+1))


    writer = pd.ExcelWriter(output_file)
    data_frames.to_excel(writer, sheet_name = 'Sales', index= True)

    writer.save()


input_path = r'C:\Users\jingjing\workspace\data_analytics_python\sales'
output_file = 'test.xlsx'
multiworkboos_concatenate(input_path,output_file)