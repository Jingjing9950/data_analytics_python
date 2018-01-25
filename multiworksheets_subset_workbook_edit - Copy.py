import pandas as pd


#Select specific columns of subset of worksheets in workbook
def multiworksheets_select_columns(input_file, output_file):
    worksheet = [1,2]
    data_frame = pd.read_excel(input_file, sheet_name= worksheet, index_col= None)
    row_output = []
    for worksheet_name, data in data_frame.items():
        row_output.append(data.loc[:, ['Customer Name', 'Sale Amount']])
    filter_rows = pd.concat(row_output, axis =0, ignore_index=True)
    writer = pd.ExcelWriter(output_file)
    filter_rows.to_excel(writer, sheet_name = 'Sale_amount_gt2000', index = False)
    writer.save()

input_file = 'sales_excel_2013.xlsx'
output_file = 'test.xlsx'
multiworksheets_select_columns(input_file,output_file)