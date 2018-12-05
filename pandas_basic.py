import pandas as pd

df = pd.read_csv('tasla.csv')
#print(df.columns)

#-----------------------rename a column of a dataframe
#method 1
df.rename(columns = {'Date':'date','High':'high'}, inplace= True)

#method 2
df_cols = ['Date','Hight_price','Low_price','Open_price','Close_price','Volum','Adjusted close']
df.columns = df_cols

#method 3
df = pd.read_csv('tasla.csv', names= df_cols)

#method 4 replace part of column name
df.columns = df.columns.str.replace(' ','_')


#------------------------remove columns and rows from dataframe
#drop columns
df.drop(['Hight_price','Low_price'],axis = 1, inplace= True)

#drop rows by index
df.drop([0,1],axis = 0, inplace= True)

#------------------------sort dataframe columns
df = df.sort_values('Adjusted_close',ascending=False)

#-------------------------filter rows of pandas dataframe by column value
df = df[df['Adjusted_close'].astype(float) > 100]

print(df)
