import csv
import glob
import os
import pandas as pd
from xlrd import open_workbook
from xlwt import Workbook

#basic information of files to be processed
file_counter = 0
for input_file in glob.glob(os.path.join('Foundations for data analytics', 'sales_*')):
    row_counter = 1
    with(open(input_file, 'r', newline="")) as csv_file:
        filereader = csv.reader(csv_file)
        header = next(filereader)
        for row in filereader:
            row_counter += 1

    print('{0!s}: \t{1:d} \t{2:d}'.format(os.path.basename(input_file), row_counter, len(header)))

    file_counter += 1

print('Numnber of files: {0:d}'.format(file_counter))

#concatenate multiple files into one by using basic python
first_file = True
for input_file in glob.glob(os.path.join('Foundations for data analytics', 'sales_*')):
    with(open(input_file, 'r', newline= "")) as csv_in_file:
        with(open('output.csv', 'a', newline= "")) as csv_out_file:
            filereader = csv.reader(csv_in_file)
            filewriter = csv.writer(csv_out_file)
            if first_file:
                for row in filereader:
                    filewriter.writerow(row)
                first_file = False
            else:
                header = next(filereader, None)
                for row in filereader:
                    filewriter.writerow(row)


all_files = glob.glob(os.path.join('Foundations for data analytics', 'sales_*'))
all_data_frams = []
for file in all_files:
    data_frame = pd.read_csv(file, index_col = None)
    all_data_frams.append(data_frame)
data_frame_concate = pd.concat(all_data_frams, axis = 0, ignore_index= True)
data_frame_concate.to_csv('output1.csv', index = False)


outfile_workbook = Workbook()
outfile_worksheet = outfile_workbook.add_sheet('jan_2013')
with(open_workbook('sales_2013.xlsx')) as workbook:
    worksheet = workbook.sheet_by_name('january_2013')
    for row_index in range(worksheet.nrows):
        for col_index in range(worksheet.ncols):
            outfile_worksheet.write(row_index, col_index, worksheet.cell_value(row_index, col_index))

outfile_workbook.save('output.xls')
