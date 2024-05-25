import streamlit as sl
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as pt
import numpy as np
from jj import highlight_cells
from jj import color_config
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-color: #F5F9FE;
background-size: cover;
background-position: center center;
background-repeat: no-repeat;
background-attachment: local;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}
button {{
            background-color: #6EF5E6 !important;
            color: #F42B1A !important;
        }}

</style>"""
sl.set_page_config(page_title="Question", layout="wide", initial_sidebar_state="auto")
sl.markdown(page_bg_img,unsafe_allow_html=True)
url="mysql+mysqlconnector://root:Vinay0511@127.0.0.1:3306/phonepe"
engine=create_engine(url,echo=True)
question=["1.what is the total tranaction, insurance and Users based on State",
          "2.what is the Total Transaction,Insurance, Users based on Year",
          "3.Pie diagram for State wise Tranaction,Insurance and Users in percentage",
          "4.What is 10 least total tranaction based?"]
quest=sl.selectbox(label="Question",options=question)
datae=pd.read_sql("SELECT at.State,at.Year,ROUND(SUM(at.Trans_amount) / 1000000, 2) AS Total_Transaction_Amount,ROUND(SUM(COALESCE(ai.Trans_amount)) / 1000000, 2) AS Total_Insurance_Transaction_Amount,ROUND(SUM(au.Registered_User) / 1000000, 2) AS Total_User FROM Aggregated_transaction at LEFT JOIN aggregated_user_All au ON at.State = au.State AND at.Year = au.Year LEFT JOIN Aggregated_insurance ai ON at.State = ai.State AND at.Year = ai.Year GROUP BY at.State, at.Year",engine)
datae["Total_Insurance_Transaction_Amount"]=datae["Total_Insurance_Transaction_Amount"].fillna(0)
if quest==question[0]:
    sl.write("All values in Lakhs")
    dataframe1=datae.groupby(['State']).sum().reset_index()
    dataframe1=dataframe1.drop(["Year"],axis=1)
    sl.dataframe(highlight_cells(dataframe1,color_config),use_container_width=True,hide_index=True)
    sl.subheader("Total Transaction Amount")
    fig=pt.scatter_3d(dataframe1,x="Total_Transaction_Amount",y="Total_Insurance_Transaction_Amount",z="Total_User",color="State")
    sl.plotly_chart(fig,use_container_width=True)
if quest==question[1]:
    sl.write("All values in Lakhs")
    dataframe1=datae.groupby(['Year']).sum().reset_index()
    dataframe1=dataframe1.drop(["State"],axis=1)
    sl.dataframe(highlight_cells(dataframe1,color_config),use_container_width=True,hide_index=True)
    col1,col2,col3=sl.columns([1,1,1])
    with col1:
        fig=pt.line(dataframe1,x="Year",y="Total_Transaction_Amount",markers=True)
        sl.plotly_chart(fig,use_container_width=True)
    with col2:
        fig=pt.line(dataframe1,x="Year",y="Total_User",markers=True)
        sl.plotly_chart(fig,use_container_width=True)
    with col3:
        fig=pt.line(dataframe1,x="Year",y="Total_Insurance_Transaction_Amount",markers=True)
        sl.plotly_chart(fig,use_container_width=True)
if quest==question[2]:
    sl.write("All values in Lakhs")
    dataframe1=datae.groupby(['State']).sum().reset_index()
    dataframe1=dataframe1.drop(["Year"],axis=1)
    sl.write(f'<p style= "color:#6A006A; font-size:30px; font-weight:Bold; text-align: center;">Total Transaction Amount</p>',unsafe_allow_html=True)
    fig=pt.pie(dataframe1,names="State",values="Total_Transaction_Amount")
    sl.plotly_chart(fig,use_container_width=True)
    sl.write(f'<p style= "color:#6A006A; font-size:30px; font-weight:Bold; text-align: center;">Total User</p>',unsafe_allow_html=True)
    fig=pt.pie(dataframe1,names="State",values="Total_User")
    sl.plotly_chart(fig,use_container_width=True)
    sl.write(f'<p style= "color:#6A006A; font-size:30px; font-weight:Bold; text-align: center;">Total Insurance Transaction Amount</p>',unsafe_allow_html=True)
    fig=pt.pie(dataframe1,names="State",values="Total_Insurance_Transaction_Amount")
    sl.plotly_chart(fig,use_container_width=True)
if quest==question[3]:
    sl.write("All values in Lakhs")
    dataframe1=datae.groupby(['State']).sum().reset_index()
    dataframe1=(dataframe1.sort_values(by=["Total_Transaction_Amount"],ascending=False)).head(10)
    dataframe1=dataframe1.drop(["Total_User","Total_Insurance_Transaction_Amount","Year"],axis=1)
    col1,col2=sl.columns([1,2])
    with col1:
        sl.dataframe(highlight_cells(dataframe1,color_config),hide_index=True,use_container_width=True)
    with col2:
        fig=pt.pie(dataframe1,names="State",values="Total_Transaction_Amount")
        sl.plotly_chart(fig,use_container_width=True)
    