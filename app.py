import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
st.set_page_config(layout="wide",page_title="StartUp Analysis")

df=pd.read_csv("startup_cleaned.csv")
df['date'] = pd.to_datetime(df['date'],errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

def load_overall_analysis():
    st.title("Overall Analysis")

    #total invested amount
    total=round(df["amount"]).sum()
    
    #max amount infused in a startup
    max_funding=df.groupby("startup")["amount"].max().sort_values(ascending=False).head(1).values[0]

    #avarage ticket size
    avg_funding=df.groupby("startup")["amount"].sum().mean()

    #total funded start up
    num_startup=df["startup"].nunique()

    col1,col2,col3,col4=st.columns(4)
    with col1:
         st.metric("Total",str(total)+"cr")
    with col2:
         st.metric("Maximum",str(max_funding)+"cr")
    with col3:
         st.metric("Average",str(round(avg_funding))+"cr")
    with col4:
         st.metric("No. Startup",str(num_startup))
    
    st.header("MoM graph")
    selected_option=st.selectbox("Select Type",["Total","Count"])
    if selected_option=="Total":
         temp_df=df.groupby(["year","month"])["amount"].sum().reset_index()
         
    else:
         temp_df=df.groupby(["year","month"])["amount"].count().reset_index()

    temp_df["x-axis"]=temp_df["month"].astype("str")+"-"+temp_df["year"].astype("str")
    temp_df[["amount","x-axis"]]
    fig3, ax3 = plt.subplots()
    ax3.plot(temp_df["x-axis"],temp_df["amount"])
    st.pyplot(fig3)

def load_investor_details(investor):
    st.title(investor)

    #load recent 5 investments of the investor
    last5_df=df[df["investors"].str.contains(investor)].head(5)[["date","startup","vertical",'city',"round","amount"]]
    st.subheader("Most Recent Investments")
    st.dataframe(last5_df)

    col1,col2=st.columns(2)
    with col1:

         #biggest investments
         big_series=df[df["investors"].str.contains(investor)].groupby("startup")["amount"].sum().head(5).sort_values(ascending=False)
         st.subheader("Biggest Investments")
         fig, ax=plt.subplots()
         ax.bar(big_series.index,big_series.values)
         st.pyplot(fig)
    with col2:
        #pie investment vertical
        vertical_series=df[df["investors"].str.contains(investor)].groupby("vertical")["amount"].sum()
        st.subheader("Sectors Invested in")
        fig1, ax1=plt.subplots()
        ax1.pie(vertical_series,labels=vertical_series.index,autopct="%0.01f%%")
        st.pyplot(fig1)

    print(df.info())

    df['year'] = df['date'].dt.year
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()

    st.subheader('YoY Investment')
    fig2, ax2 = plt.subplots()
    ax2.plot(year_series.index,year_series.values)

    st.pyplot(fig2)



st.sidebar.title("Startup Funding Analysis")


option=st.sidebar.selectbox("Select One",["Overall Analysis","StartUp","Investor"])

if option=="Overall Analysis":
    #btn0=st.sidebar.button("Show Overall Analysis")
    #if btn0:
        load_overall_analysis()
elif option=="StartUp":
    st.sidebar.selectbox("select startup",sorted(df["startup"].unique().tolist()))
    btn1=st.sidebar.button("Find start-up Details")
    st.title("Stater Analysis")

else:
    selected_investor=st.sidebar.selectbox("select Investors",sorted(set(df["investors"].str.split(",").sum())))
    btn2=st.sidebar.button("Find Investor Details")
    if btn2:
        load_investor_details(selected_investor)
    