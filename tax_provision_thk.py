import pandas as pd

data_frame=pd.read_excel("GL Jan_Apr18 THK LM.XLSX")
data_frame = data_frame.fillna(value="missing")

write_excel=pd.ExcelWriter("Provosion_for_tax.xlsx")

add_back_items={}

def auto_sum_expense(accountdata_filter, column_name, account_name, key_name):
    accountdata_filter = data_frame[data_frame[column_name]==account_name]
    add_back_items[key_name] = accountdata_filter["Amount in local currency"].sum()

def auto_sum_expense_contain(accountdata_filter, column_name1, account_name,filtered_data,column_name2,string_contain, key_name,):
    accountdata_filter = data_frame[data_frame[column_name1]==account_name]
    filtered_data=accountdata_filter[accountdata_filter[column_name2].str.contains("|".join(string_contain))]
    add_back_items[key_name] = filtered_data["Amount in local currency"].sum()

def breakdown_list_1(accountdata_filter, column_name, account_name, key_name):
    accountdata_filter = data_frame[data_frame[column_name]==account_name]
    return accountdata_filter

def breakdown_list_2(accountdata_filter, column_name1, account_name,filtered_data,column_name2,string_contain, key_name,):
    accountdata_filter = data_frame[data_frame[column_name1]==account_name]
    filtered_data=accountdata_filter[accountdata_filter[column_name2].str.contains("|".join(string_contain))]
    return filtered_data

def write_into_excel_sheet(summary__breakdown_list,work_sheet):
    summary__breakdown_list.to_excel(write_excel,work_sheet)

#Vehicel expense_add back
auto_sum_expense("vehicle_exp","Account Text","Vehicle exp","vehical_expenses")

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

#convert dictionary to Series in pandas
df_result = pd.Series(add_back_items,name="Amount")

write_into_excel_sheet(df_result,"provision_summary")
write_excel.save()
write_excel.close()

