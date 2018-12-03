import pandas as pd
import xlsxwriter

data_frame=pd.read_excel("GL Jan-Jun'18.XLSX")
data_frame = data_frame.fillna(value="missing")

write_excel=pd.ExcelWriter("Provosion_for_tax.xlsx")

add_back_items={}

def auto_sum_expense(accountdata_filter, column_name, account_name, key_name):
    accountdata_filter = data_frame[data_frame[column_name]==account_name]
    add_back_items[key_name] = accountdata_filter["Amount in local currency"].sum()

def auto_sum_expense_contain(accountdata_filter, column_name1, account_name,filtered_data,column_name2,string_contain, key_name):
    accountdata_filter = data_frame[data_frame[column_name1]==account_name]
    filtered_data=accountdata_filter[accountdata_filter[column_name2].str.contains("|".join(string_contain))]
    add_back_items[key_name] = filtered_data["Amount in local currency"].sum()

def breakdown_list_1(accountdata_filter, column_name, account_name, key_name):
    accountdata_filter = data_frame[data_frame[column_name]==account_name]
    return accountdata_filter

def breakdown_list_2(accountdata_filter, column_name1, account_name,filtered_data,column_name2,string_contain, key_name):
    accountdata_filter = data_frame[data_frame[column_name1]==account_name]
    filtered_data=accountdata_filter[accountdata_filter[column_name2].str.contains("|".join(string_contain))]
    return filtered_data

def write_into_excel_sheet(summary__breakdown_list,work_sheet):
    summary__breakdown_list.to_excel(write_excel,work_sheet)


#Vehicel expense_add back
auto_sum_expense("vehicle_exp","Account Text","Vehicle exp","vehicle_expenses")

#Vehicel road tax_add back
auto_sum_expense_contain("tax_dues","Account Text","Taxes and dues", "road_tax", "Text",["Road"],"Vehicle_road_tax")
write_into_excel_sheet(breakdown_list_2("tax_dues","Account Text","Taxes and dues", "road_tax", "Text",["Road"],"Vehicle_road_tax"),"Vehicle_road_tax")

#Vehicel insurance_add back
auto_sum_expense("vehicle_insu","Account Text","Vehicle insurance","Vehicle_insurance")

#Rental_expense_vehicle
auto_sum_expense("rental_vehicle","Account Text","Rental exp vehicle","Rental_expenses_vehicle")
write_into_excel_sheet(breakdown_list_1("rental_vehicle","Account Text","Rental exp vehicle","Rental_expenses_vehicle"),"rental_expe_vehicle")

#Property tax & employment pass fee
auto_sum_expense_contain("tax_dues","Account Text","Taxes and dues","property_tax","Text",["Property"],"Property_tax")
auto_sum_expense_contain("tax_dues","Account Text","Taxes and dues","employ_pass","Text",["pass","visa","permit"],"Employee_pass_fee")
write_into_excel_sheet(breakdown_list_2("tax_dues","Account Text","Taxes and dues","property_tax","Text",["Property"],"Property_tax"),"property_tax")
write_into_excel_sheet(breakdown_list_2("tax_dues","Account Text","Taxes and dues","employ_pass","Text",["pass","visa","permit"],"Employee_pass_fee"),"employee_pass_fee")

#professional_fee
auto_sum_expense("profession_fee","Account Text","Professional fees","Professional_services")
write_into_excel_sheet(breakdown_list_1("profession_fee","Account Text","Professional fees","Professional_services"),"professional_service")

#Welfare expensed _add back
welfare_expense=data_frame[data_frame["Account Text"] =="Welfare exp"]
search_medical=["Medical","medical"]
medical_expen = welfare_expense[welfare_expense["Assignment"].str.contains("|".join(search_medical))]

search_medical_fee=["Medical","medical","Dental","dental","vac","Vac"]
medical_fee = medical_expen[medical_expen["Text"].str.contains("|".join(search_medical_fee))]
add_back_items["Medical_fee"] = medical_fee["Amount in local currency"].sum()
write_into_excel_sheet(medical_fee,"medical_fee")

search_medical_insu=["Hospi","hospi"]
medical_insurance = medical_expen[medical_expen["Text"].str.contains("|".join(search_medical_insu))]
add_back_items["Medical_insurance"] = medical_insurance["Amount in local currency"].sum()
write_into_excel_sheet(medical_insurance,"medical_insurance")

#Misc_income
auto_sum_expense("misllan_income","Account Text","Misc income","Misllanence_income")
write_into_excel_sheet(breakdown_list_1("misllan_income","Account Text","Misc income","Misllanence_income"),"misc_income")

#Office supplies_fine & penalty
auto_sum_expense_contain("office_supplies","Account Text","Office supplies exp", "fine_penalty", "Text",["fine","penalty","Fine","Penalty"],"fine")
write_into_excel_sheet(breakdown_list_2("office_supplies","Account Text","Office supplies exp", "fine_penalty", "Text",["fine","penalty","Fine","Penalty"],"fine"),"Fine_penalty")

#convert dictionary to Series in pandas
df_result = pd.Series(add_back_items,name="Amount")

#Format to be edited
df_result.to_excel(write_excel, sheet_name="provision_summary", startrow=5, startcol=40)
worksheet=write_excel.sheets["provision_summary"] #xlsxwriter to add/append content in excel

header1 = "THK LM SYSTEM PTE LTD"
header2 = "TAX SCHEDULES - YA2019"
schedule = "SCHEDULE"

worksheet.write("A1",header1)
worksheet.write("A2",header2)

worksheet.write("A4",schedule+"2")
worksheet.write("A6", "Motor vehicle expenses - S plated vehicle")
worksheet.write("A7","Vehcle expenses (maintenance, parking, cash card, petrol, etc")
worksheet.write("B7",df_result["vehicle_expenses"])
worksheet.write("A8","Taxes and dues (vehicle road tax")
worksheet.write("B8",df_result["Vehicle_road_tax"])
worksheet.write("A9","Vehicle insurance")
worksheet.write("B9",df_result["Vehicle_insurance"])
worksheet.write_formula("B10","=sum(B7,B8,B9)")#formula
worksheet.write("A12", "Rental expenses vehicle")
worksheet.write("B12", df_result["Rental_expenses_vehicle"])

worksheet.write("A14",schedule+"3")
worksheet.write("A15","Taxes and dues")
worksheet.write("A16","Property Tax for 38 Kaki Bukit Place ($1,941.67/month")
worksheet.write("B16",df_result["Property_tax"])
worksheet.write("A17","Employment pass fee")
worksheet.write("B17",df_result["Employee_pass_fee"])
worksheet.write("A18","Vehicle road tax SGP7676L")
worksheet.write("B18",df_result["Vehicle_road_tax"])
worksheet.write_formula("B19","=sum(B16,B17,B18)")#formula

worksheet.write("A20",schedule+"4")
worksheet.write("A21","Professional service")
professional_service = pd.read_excel("Provosion_for_tax.xlsx",sheet_name="professional_service")
professional_service=professional_service[['Text','Amount in local currency']]
professional_service.to_excel(write_excel, sheet_name="provision_summary", startrow=21, index = False, header = False)
row_count = len(professional_service.index)
next_row = 21+row_count
worksheet.write("B"+str(next_row+1),professional_service['Amount in local currency'].sum())

worksheet.write("A"+str(next_row+2),schedule+"5")
worksheet.write("A"+str(next_row+3),"Unrealised exchange gain &loss for capital &revenue are combines into one accounts under SAP")

worksheet.write("A"+str(next_row+5),schedule+"6")
worksheet.write("A"+str(next_row+6),"Medical fee")
worksheet.write("B"+str(next_row+6),df_result["Medical_fee"])
worksheet.write("A"+str(next_row+7),"Medical insurance")
worksheet.write("B"+str(next_row+7),df_result["Medical_insurance"])


worksheet.write("A"+str(next_row+9),schedule+"7")
worksheet.write("A"+str(next_row+10),"Misc income")
misc_income = pd.read_excel("Provosion_for_tax.xlsx",sheet_name="misc_income")
misc_income=misc_income[['Text','Amount in local currency']]
misc_income.to_excel(write_excel, sheet_name="provision_summary", startrow=next_row+10, index = False, header = False)
row_count_a = len(misc_income.index)

worksheet.write("A"+str(next_row+12+row_count_a),schedule+"10")
worksheet.write("A"+str(next_row+13+row_count_a),"Office supplies")
fine = pd.read_excel("Provosion_for_tax.xlsx",sheet_name="Fine_penalty")
fine=fine[['Text','Amount in local currency']]
fine.to_excel(write_excel, sheet_name="provision_summary", startrow=next_row+13+row_count_a, index = False, header = False)

write_excel.save()
write_excel.close()
