from sqlalchemy import create_engine
import pandas as pd
import streamlit as sl
import plotly.express as pt
from jj import highlight_cells
from jj import color_config
from streamlit_extras.stateful_button import button

url="mysql+mysqlconnector://root:Vinay0511@127.0.0.1:3306/phonepe"
engine=create_engine(url,echo=True)
#Page colure mapping  
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

sl.set_page_config(page_title="Phonepe pulse", page_icon="OIP.jpg", layout="wide", initial_sidebar_state="auto")
sl.markdown(page_bg_img,unsafe_allow_html=True)
sl.write(f'<p class="fa-solid fa-eye" style="color: #6A006A; font-size: 40px;font-weight: bold">Phonepe Pulse and Data Visualzation</p>',unsafe_allow_html=True)
quaters={1:"Jan-Mar",2:"Apr-Jun",3:"Jul-Sep",4:"Oct-Dec"}
data_types=["Transaction","Users","Insurance"]
if "All_data" not in sl.session_state:
    sl.session_state["All_data"]="Transaction"
if "year_data" not in sl.session_state:
    sl.session_state["year_data"]=2018
if "qtr" not in sl.session_state:
    sl.session_state["qtr"]=1
with sl.sidebar:
    sl.session_state["All_data"]=sl.selectbox(options=data_types,label="select")
    if sl.session_state["All_data"]==data_types[0]:
        dta=pd.read_sql('select Year, Quater from Aggregated_transaction',engine)
        sl.session_state["year_data"]=sl.selectbox(options=list(dta.Year.unique()),label="Year")
        sl.session_state["qtr"]=sl.selectbox(options=list(dta.Quater.unique()),label="Quater")
    elif sl.session_state["All_data"]==data_types[1]:
        dta=pd.read_sql('SELECT Year, Quater from Aggregated_user',engine)
        sl.session_state["year_data"]=sl.selectbox(options=list(dta.Year.unique()),label="Year")
        sl.session_state["qtr"]=sl.selectbox(options=list(dta.Quater.unique()),label="Quater")
    elif sl.session_state["All_data"]==data_types[2]:
        dta=pd.read_sql('SELECT Year, Quater from Aggregated_insurance',engine)
        sl.session_state["year_data"]=sl.selectbox(options=list(dta.Year.unique()),label="Year")
        sl.session_state["qtr"]=sl.selectbox(options=list(dta.Quater.unique()),label="Quater")
    
        
da=f'Selected {sl.session_state["All_data"]} and Period Of { sl.session_state["year_data"]} {quaters[sl.session_state["qtr"]]}'
if sl.session_state["All_data"]==data_types[0]:
    df=pd.read_sql(f'select UPPER(State) as State,sum(Trans_count) as Total_Tranaction, sum(Trans_amount) as Total_Amount from Aggregated_transaction where Year= {sl.session_state["year_data"]} and Quater= {sl.session_state["qtr"]} group by state order by state',engine)
    df1=pd.read_csv("state_names.csv")
    df["state"]=df1["state"]
    df["Total_Amount"]=round(df["Total_Amount"]/100000,2)
    fig=pt.choropleth(data_frame=df,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='state',
                    color='Total_Amount',
                    color_continuous_scale=pt.colors.sequential.Blues_r,
                    hover_data=["state","Total_Tranaction","Total_Amount"])
    fig.update_layout(height=600,title_text = da,coloraxis_colorbar_tickformat='M', coloraxis_colorbar_title="Total Transaction Amount<br> in lakhs")
    fig.update_traces(hovertemplate='<b>State: %{customdata[0]}</b><br>Total Transaction Amount:₹ %{customdata[2]} lakhs<br>Total Tranaction: %{customdata[1]}')
    fig.update_geos(fitbounds="locations", visible=False)
    sl.plotly_chart(fig,use_container_width=True)
    sl.write('<p style= "color:#6A006A; font-size:35px; font-weight:Bold; text-align: center;">Top 10 Tranaction</p>',unsafe_allow_html=True)
    tab,char=sl.columns([1,1])
    with tab:
        but1,but2,but3=sl.columns([1,1,1])
        tarn=pd.read_sql(f'select UPPER(State) as State,sum(Trans_count) as Total_Tranaction, sum(Trans_amount) as Total_Amount from aggregated_transaction where Year= {sl.session_state["year_data"]} and Quater= {sl.session_state["qtr"]} group by state order by state',engine)
        top_df=(tarn.sort_values(by=["Total_Amount"],ascending=False)).head(10)
        data=top_df
        lable="State Wise"
        with but1:
            if sl.button(label="State Wise",use_container_width=True):
                data=top_df
        with but2:
            if sl.button(label="District Wise",use_container_width=True):
                lable="District Wise"
                distr=pd.read_sql(f"select State,UPPER(District) as District,sum(Trans_count) as Total_Tranaction, round(sum(Trans_amount),2) as Total_Amount from map_transacion where Year= {sl.session_state['year_data']} and Quater={sl.session_state['qtr']} group by State,District order by Total_Amount DESC",engine)
                data=((distr.sort_values(by=["Total_Amount"],ascending=False)).head(10).drop(["State"],axis=1))
        with but3:
            if sl.button(label="Pincode Wise",use_container_width=True):
                lable="Pincode Wise"
                distr=pd.read_sql(f"select State,Pincodes,sum(Trans_count) as Total_Tranaction, sum(Trans_amount) as Total_Amount from top_transaction where Year= {sl.session_state['year_data']} and Quater={sl.session_state['qtr']} group by State,Pincodes order by Total_Amount DESC",engine)
                distr["Pincodes"]=distr["Pincodes"].astype(str)
            
                data=((distr.sort_values(by=["Total_Amount"],ascending=False).head(10)).drop(["State"],axis=1))

        sl.dataframe(highlight_cells(pd.DataFrame(data),color_config),hide_index=True,use_container_width=True)
    with char:
        sl.write(f'<p style= "color:#6A006A; font-size:20px; font-weight:Bold; text-align: center;">{lable}</p>',unsafe_allow_html=True)
        colum=data.columns
        s_d_p=colum[0]
        total_am=colum[2]
        total_tra=colum[1]
        fig=pt.treemap(data,path=[s_d_p,"Total_Amount"],values=total_am,color=s_d_p)
        fig.update_layout(
                title='Treemap of Transaction Amount by State and Year',
                margin=dict(t=50, l=25, r=25, b=25)
                    )
        sl.plotly_chart(fig,use_container_width=True)
        
    sl.write('<p style= "color:#6A006A; font-size:35px; font-weight:Bold; text-align: center;">Transaction Based on State</p>',unsafe_allow_html=True)
    col1,col2=sl.columns([1,1])
    with col1:
        select_state=sl.selectbox(options=df["State"].unique(),label_visibility="hidden",label="State")
        sl.write('<p style="padding-top: 1rem;"></p>',unsafe_allow_html=True)
        trans_type=pd.read_sql(f"select Tranaction_type, sum(Trans_count) as Total_Tranaction, round(sum(Trans_amount),2) as Total_Amount from aggregated_transaction where (Year= {sl.session_state['year_data']} and State = '{select_state}' and Quater= {sl.session_state['qtr']}) group by Tranaction_type order by tranaction_type",engine)
        trans_type["Total_Amount"]= trans_type["Total_Amount"]/100000
        fig=pt.bar(trans_type,x="Tranaction_type",y="Total_Amount",labels={'Trans_amount': 'Total Transaction'})
        fig.update_layout(yaxis=dict(tickformat=',d'),height=400)
        fig.update_traces(texttemplate='%{y}<br>lakhs', textposition='outside',hovertemplate='<b>%{x}</b><br>Total Transaction Amount: ₹%{y} lakhs')
        sl.plotly_chart(fig,use_container_width=True)
    with col2:
        sl.write(f'<p style= "color:#6A006A; font-size:20px; font-weight:Bold; text-align: center;padding-top: 20px;">{select_state}</p>',unsafe_allow_html=True)
        fig_pie=pt.pie(trans_type,names="Tranaction_type",values="Total_Amount")
        fig_pie.update_traces(hovertemplate='<b>%{label}</b><br>Total Transaction Amount: ₹%{text} lakhs')
        sl.plotly_chart(fig_pie,use_container_width=True)
if sl.session_state["All_data"]==data_types[1]:
    df_user=pd.read_sql(f'select UPPER(State) as State,sum(user) as Total_Users from aggregated_user where Year= {sl.session_state["year_data"]} and Quater= {sl.session_state["qtr"]} group by state order by state',engine)
    df1=pd.read_csv("state_names.csv")
    df_user["state"]=df1["state"]
    fig=pt.choropleth(data_frame=df_user,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='state',
                    color='Total_Users',
                    color_continuous_scale=pt.colors.sequential.Blues_r,
                    hover_data=["State","Total_Users"])
    fig.update_layout(height=600,title_text = da,coloraxis_colorbar_tickformat='M', coloraxis_colorbar_title="Total Users")
    fig.update_traces(hovertemplate='<b>State: %{customdata[0]}</b><br>Total Users:%{customdata[1]}')
    fig.update_geos(fitbounds="locations", visible=False)
    sl.plotly_chart(fig,use_container_width=True)
    sl.write('<p style= "color:#6A006A; font-size:35px; font-weight:Bold; text-align: center;">Top 10 Tranaction</p>',unsafe_allow_html=True)
    tab,char=sl.columns([1,1])
    with tab:
        but1,but2,but3=sl.columns([1,1,1])
        df_user1=pd.read_sql(f'select UPPER(State) as State,sum(user) as Total_Users from aggregated_user where Year= {sl.session_state["year_data"]} and Quater= {sl.session_state["qtr"]} group by state order by Total_Users',engine)
        top_df=(df_user1.sort_values(by=["Total_Users"],ascending=False)).head(10)
        data=top_df
        lable="State Wise"
        with but1:  
            if sl.button(label="State Wise",use_container_width=True):
                data=top_df
        with but2:
            if sl.button(label="District Wise",use_container_width=True):
                lable="District Wise"
                distr=pd.read_sql(f"select UPPER(District) as District,sum(Registered_User) as Total_Users, round(sum(Apps_Opens)) as Apps_Opens from map_user where Year= {sl.session_state['year_data']} and Quater={sl.session_state['qtr']} group by District order by Total_Users DESC",engine)
                data=((distr.sort_values(by=["Total_Users"],ascending=False)).head(10))
        with but3:
            if sl.button(label="Pincode Wise",use_container_width=True):
                lable="Pincode Wise"
                distr=pd.read_sql(f"select Pincodes,sum(Registered_User) as Total_Users from top_user where Year= {sl.session_state['year_data']} and Quater={sl.session_state['qtr']} group by Pincodes order by Total_Users DESC",engine)
                distr["Pincodes"]=distr["Pincodes"].astype(str)
                data=((distr.sort_values(by=["Total_Users"],ascending=False).head(10)))

        sl.dataframe(highlight_cells(pd.DataFrame(data),color_config),
                     hide_index=True,use_container_width=True)
    with char:
        sl.write(f'<p style= "color:#6A006A; font-size:20px; font-weight:Bold; text-align: center;">{lable}</p>',unsafe_allow_html=True)
        colum=data.columns
        s_d_p=colum[0]
        total_tra=colum[1]
        fig=pt.treemap(data,path=[s_d_p,"Total_Users"],values=total_tra,color=s_d_p)
        fig.update_layout(
                title='Treemap of Transaction Amount by State and Year',
                margin=dict(t=50, l=25, r=25, b=25)
                    )
        sl.plotly_chart(fig,use_container_width=True)
        
    sl.write('<p style= "color:#6A006A; font-size:35px; font-weight:Bold; text-align: center;">Device Based Users</p>',unsafe_allow_html=True)
    col1,col2=sl.columns([1,1])
    with col1:
        select_state=sl.selectbox(options=df_user["State"].unique(),label_visibility="hidden",label="State")
        sl.write('<p style="padding-top: 1rem;"></p>',unsafe_allow_html=True)
        trans_type=pd.read_sql(f'SELECT upper(State) as State, upper(Brand) as Brand_Name, sum(User) as Total_Users from Aggregated_user where Year={sl.session_state["year_data"]} and Quater={sl.session_state["qtr"]} and State="{select_state}" group by State,Brand order by Brand',engine)
        fig=pt.bar(trans_type,x="Brand_Name",y="Total_Users",labels={'Trans_Users': 'Brand_Name'})
        fig.update_layout(yaxis=dict(tickformat=',%d'),height=400)
        #fig.update_traces(texttemplate='%{y}<br>lakhs', textposition='outside',hovertemplate='<b>%{x}</b><br>Total Transaction Amount: ₹%{y} lakhs')
        sl.plotly_chart(fig,use_container_width=True)
    with col2:
        sl.write(f'<p style= "color:#6A006A; font-size:20px; font-weight:Bold; text-align: center;padding-top: 20px;">{select_state}</p>',unsafe_allow_html=True)
        fig_pie=pt.pie(trans_type,names="Brand_Name",values="Total_Users")
        fig_pie.update_traces(hovertemplate='<b>%{label}</b><br>Total Users: %{values}')
        sl.plotly_chart(fig_pie,use_container_width=True)
if sl.session_state["All_data"]==data_types[2]:
    df=pd.read_sql(f'select UPPER(State) as State,sum(Trans_count) as Total_Tranaction, sum(Trans_amount) as Total_Amount from Aggregated_insurance where Year= {sl.session_state["year_data"]} and Quater= {sl.session_state["qtr"]} group by state order by state',engine)
    df1=pd.read_csv("state_names.csv")
    df["state"]=df1["state"]
    df["Total_Amount"]=round(df["Total_Amount"]/100000,2)
    fig=pt.choropleth(data_frame=df,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='state',
                    color='Total_Amount',
                    color_continuous_scale=pt.colors.sequential.Blues_r,
                    hover_data=["state","Total_Tranaction","Total_Amount"])
    fig.update_layout(height=600,title_text = da,coloraxis_colorbar_tickformat='M', coloraxis_colorbar_title="Total Transaction Amount<br> in lakhs")
    fig.update_traces(hovertemplate='<b>State: %{customdata[0]}</b><br>Total Transaction Amount:₹ %{customdata[2]} lakhs<br>Total Tranaction: %{customdata[1]}')
    fig.update_geos(fitbounds="locations", visible=False)
    sl.plotly_chart(fig,use_container_width=True)
    sl.write('<p style= "color:#6A006A; font-size:35px; font-weight:Bold; text-align: center;">Top 10 Insurance Transaction</p>',unsafe_allow_html=True)
    tab,char=sl.columns([1,1])
    with tab:
        but1,but2,but3=sl.columns([1,1,1])
        tarn=pd.read_sql(f'select UPPER(State) as State,sum(Trans_count) as Total_Tranaction, sum(Trans_amount) as Total_Amount from aggregated_insurance where Year= {sl.session_state["year_data"]} and Quater= {sl.session_state["qtr"]} group by state order by Total_Amount DESC',engine)
        top_df=(tarn.sort_values(by=["Total_Amount"],ascending=False)).head(10)
        data=top_df
        lable="State Wise"
        with but1:
            if sl.button(label="State Wise",use_container_width=True):
                data=top_df
        with but2:
            if sl.button(label="District Wise",use_container_width=True):
                lable="District Wise"
                distr=pd.read_sql(f"select State,UPPER(District) as District,sum(Trans_count) as Total_Tranaction, round(sum(Trans_amount),2) as Total_Amount from map_insurance where Year= {sl.session_state['year_data']} and Quater={sl.session_state['qtr']} group by State,District order by Total_Amount DESC",engine)
                data=((distr.sort_values(by=["Total_Amount"],ascending=False)).head(10).drop(["State"],axis=1))
        with but3:
            if sl.button(label="Pincode Wise",use_container_width=True):
                lable="Pincode Wise"
                distr=pd.read_sql(f"select State,Pincodes,sum(Trans_count) as Total_Tranaction, round(sum(Trans_amount),2) as Total_Amount from top_insurance where Year= {sl.session_state['year_data']} and Quater={sl.session_state['qtr']} group by State,Pincodes order by Total_Amount DESC",engine)
                distr["Pincodes"]=distr["Pincodes"].astype(str)
                data=((distr.sort_values(by=["Total_Amount"],ascending=False).head(10)).drop(["State"],axis=1))

        sl.dataframe(highlight_cells(pd.DataFrame(data),color_config),hide_index=True,use_container_width=True)
    with char:
        sl.write(f'<p style= "color:#6A006A; font-size:20px; font-weight:Bold; text-align: center;">{lable}</p>',unsafe_allow_html=True)
        colum=data.columns
        s_d_p=colum[0]
        total_am=colum[2]
        total_tra=colum[1]
        fig=pt.treemap(data,path=[s_d_p,"Total_Amount"],values=total_am,color=s_d_p)
        fig.update_layout(
                title='Treemap of Transaction Amount by State and Year',
                margin=dict(t=50, l=25, r=25, b=25)
                    )
        sl.plotly_chart(fig,use_container_width=True)
