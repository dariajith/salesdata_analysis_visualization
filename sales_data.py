import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
#read file
df=pd.read_csv("/home/dari/Downloads/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/Sales_April_2019.csv")
print(df.columns)
print(df.shape)
#read all csv files in sales_data folder
folder=[file for file in
       os.listdir("/home/dari/Downloads/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data")]
for files in folder:
    print(files)

#merge 12 month of dataset
all_month=pd.DataFrame()
for file in folder:
    df=pd.read_csv("/home/dari/Downloads/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/"+file)
    all_month=pd.concat([all_month,df])

#export file
all_month.to_csv("/home/dari/Downloads/all_month_data.csv",index=False)
all_month_data_df=pd.read_csv("/home/dari/Downloads/all_month_data.csv")


print(all_month_data_df["Order Date"].head())
#add new column and split the date_only
all_month_data_df["date_only"]=all_month_data_df["Order Date"].str[3:5]
print(all_month_data_df.head())
print(all_month_data_df.shape)
all_month_data_df["month_only"]=all_month_data_df["Order Date"].str[0:2]
print(all_month_data_df.head())
#add month column and filter null values and error values("data_clean")
all_month_data_df.dropna(inplace=True,axis=0)
all_month_data_df=all_month_data_df[all_month_data_df["month_only"]!="Or"]
print(all_month_data_df)

#all_month_data_df["month_only"]=all_month_data_df.month_only.astype("int")


print(all_month_data_df["month_only"].astype("int"))

#clean data: romove null in row and error data(er)

all_month_data_df.date_only[all_month_data_df.date_only=="er"]=np.nan
all_month_data_df.dropna(axis=0,inplace=True)
#convert string to integer
all_month_data_df.date_only=all_month_data_df.date_only.astype("int")
print(all_month_data_df.dtypes)
#add sales column and convert correct data type

all_month_data_df["Quantity Ordered"]=all_month_data_df["Quantity Ordered"].astype("int")
all_month_data_df["Price Each"]=all_month_data_df["Price Each"].astype(float)
#print(all_month_data_df.dtypes)
all_month_data_df["sales"]=all_month_data_df["Quantity Ordered"]*all_month_data_df["Price Each"]

#best month sales and earning

def sales_group():
    month_wise_sales_data=all_month_data_df.groupby("month_only").sum()
    no_of_month=range(1,13)
    #data visulation
    plt.bar(no_of_month,month_wise_sales_data["sales"])
    plt.xticks(no_of_month)
    plt.ylabel("sales")
    plt.xlabel("no of month")
    plt.show()
def sold_city():
    all_month_data_df["city"]=all_month_data_df["Purchase Address"].apply(lambda x: x.split(",")[1])
    all_month_data_df["state"] = all_month_data_df["Purchase Address"].apply(lambda x: x.split(",")[2].split(" ")[1])
    all_month_data_df["city_state"] = all_month_data_df.city + "(" + all_month_data_df.state + ")"
    city_wise_sales = all_month_data_df.groupby("city_state").sales.sum().max()
#sold_city()

#which time selling is peak
def time_selling():

    all_month_data_df["Order Date"]=pd.to_datetime(all_month_data_df["Order Date"])
    all_month_data_df["hour"]=all_month_data_df["Order Date"].dt.hour
    all_month_data_df["minutes"]=all_month_data_df["Order Date"].dt.minute

#what product are most ofter sold
def product_sold():

    df=all_month_data_df[all_month_data_df["Order ID"].duplicated(keep=False)]
    df["grouped"]=df.groupby("Order ID")["Product"].transform(lambda x: ",".join(x))
    df.drop_duplicates(subset=["Order ID"],inplace=True)


#what product sold most and why sold most
def most_product_sold():
    product_group=all_month_data_df.groupby("Product")
    quantity_ordered=product_group.sum()["Quantity Ordered"]

    product=[i for i,j in product_group]
    plt.bar(product,quantity_ordered)
    plt.xticks(product,rotation="vertical",size=8)

    price=all_month_data_df.groupby("Product")["Price Each"].mean()

    fig,ax1=plt.subplots()
    ax2=ax1.twinx()
    ax1.bar(product,quantity_ordered,color="b")
    ax2.plot(product,price,color='g')
    #ax1.set_xticklabels(rotation='vertical',size=8)
    ax1.set_xticklabels(product,rotation='vertical',size=9)
    plt.show()
if __name__=='__main__':

    sales_group()
    sold_city()
    time_selling()
    product_sold()
    most_product_sold()