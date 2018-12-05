import numpy as np
import pandas as pd
import quandl
import matplotlib.pyplot as plt

api_key = quandl.ApiConfig.api_key = '54sdgtjsmKrgizUjttjP'
us_code = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')
us_code_abb = us_code[0][1]

main_df = pd.DataFrame()
write_excel = pd.ExcelWriter("House_Price.xlsx")

for abb in us_code_abb[1:]:
    if abb == "AL" or abb == "AZ":
        query = "FMAC/HPI_" + str(abb)
        df = quandl.get(query, authtoken = api_key)
        df = df.rename(columns = {"NSA Value": abb, "SA Value": abb+" SA"})
        df = df.loc['2000-01-01':'2010-12-31']
        print(df)

        if main_df.empty:
            main_df = df

        else:
            main_df = main_df.join(df)

#print(main_df.head(2))

# main_df.to_excel(write_excel, "price")
# write_excel.save()
# write_excel.close()

main_df.plot()
plt.show()

#print(main_df.head())
