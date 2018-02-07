import csv
import pandas as pd
import glob
import os


item_number_to_be_found = []
filereader = csv.reader(open(r'item_numbers_to_find.csv', 'r', newline=''), delimiter = ",")
for row in filereader:
    item_number_to_be_found.append(row[0])

filewriter = csv.writer(open('test.csv','a', newline = ''))

for input_file in glob.glob(os.path.join(r'C:\Users\jingjing\workspace\data_analytics_python\file_archive','*.*')):
    if input_file.split('.')[1] == 'csv':
        filereader_a = csv.reader(open(input_file,'r',newline=''))
        header = next(filereader_a)
        for row in filereader_a:
            row_of_output = []
            for column in range(len(header)):
                row_of_output.append(row[column])

            row_of_output.append(os.path.basename(input_file))
            if row[0] in item_number_to_be_found:
                filewriter.writerow(row_of_output)

    elif input_file.split('.')[1] == 'xlsx' or input_file.split('.')[1] == 'xls':
        data_frames = []
        data_frame = pd.read_excel(input_file, sheetname= None, index_col=None)
        for worksheet_name, data in data_frame.items():
            data['Source'] = os.path.basename(input_file)
            data_frames.append(data[data['Item Number'].isin(item_number_to_be_found)])
        all_data_concate = pd.concat(data_frames, axis = 0, ignore_index= True)

        data_dict = all_data_concate.to_dict(orient = 'index')
        row_of_output = []
        for data_index_len in range(len(all_data_concate)):
            row_of_output.append(list(data_dict[data_index_len].values()))

        for value in row_of_output:
            filewriter.writerow(value)








