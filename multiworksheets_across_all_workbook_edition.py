import pandas as pd


#Filter for specific rows across all worksheets_condition "Sale amount' > 2000
def multiworksheets_filter_row(input_file, output_file):
    data_frame = pd.read_excel(input_file, sheet_name= None, index_col= None)
    row_output = []
    for worksheet_name, data in data_frame.items():
        row_output.append(data[data['Sale Amount'].astype(float) > 2000])
    filter_rows = pd.concat(row_output, axis =0, ignore_index=True)
    writer = pd.ExcelWriter(output_file)
    filter_rows.to_excel(writer, sheet_name = 'Sale_amount_gt2000', index = False)
    writer.save()


#Select specific columns across all worksheets
def multiworksheets_select_columns(input_file, output_file):
    data_frame = pd.read_excel(input_file, sheet_name= None, index_col= None)
    row_output = []
    for worksheet_name, data in data_frame.items():
        row_output.append(data.loc[:, ['Customer Name', 'Sale Amount']])
    filter_rows = pd.concat(row_output, axis =0, ignore_index=True)
    writer = pd.ExcelWriter(output_file)
    filter_rows.to_excel(writer, sheet_name = 'Sale_amount_gt2000', index = False)
    writer.save()


