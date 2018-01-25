import pandas as pd
import glob
import os

#concatenate multi workbooks
def multiworkboos_concatenate(input_path, output_file):
    input_files = glob.glob(os.path.join(input_path, '*.xlsx*'))
    data_frames = []
    for input_file in input_files:
        data_frame = pd.read_excel(input_file, sheet_name= None, index_col= None)
        for worksheet_name, data in data_frame.items():
            data_frames.append(data)

    all_data_concatenate = pd.concat(data_frames, axis =0, ignore_index=True)
    writer = pd.ExcelWriter(output_file)
    all_data_concatenate.to_excel(writer, sheet_name = 'Sales', index = False)
    writer.save()


input_path = r'C:\Users\jingjing\workspace\data_analytics_python\sales'
output_file = 'test.xlsx'
multiworkboos_concatenate(input_path,output_file)