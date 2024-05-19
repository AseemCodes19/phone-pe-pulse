import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import mysql.connector
import plotly.express as px
import requests
import json




# Establish MySQL connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    port="3306",
    password="1234",
    database="phonepe_pulse"
)
mycursor = mydb.cursor()

#aggre_transaction_df
mycursor = mydb.cursor()
mycursor.execute( "SELECT * FROM aggregated_insurance")
table1 = mycursor.fetchall()

# Convert the result into a DataFrame
Aggre_insurance = pd.DataFrame(table1, columns=("state","year","quarter","transaction_type","transaction_count","transaction_amount"))



#aggre_user_df
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM aggre_transaction")
table2 = mycursor.fetchall()

# Convert the result into a DataFrame
aggre_transaction = pd.DataFrame(table2, columns=("state","year","quarter","transaction_type","transaction_count","transaction_amount"))




mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM aggre_user")
table3 = mycursor.fetchall()

# Convert the result into a DataFrame
aggre_user = pd.DataFrame(table3, columns=("state","year","quarter","Brands","transaction_count","transaction_amount"))



# Execute the query and fetch data
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM map_insurance")
table4 = mycursor.fetchall()

# Convert the result into a DataFrame
map_insurance = pd.DataFrame(table4, columns=("state","year","quarter","Districts","transaction_count","transaction_amount"))


# Execute the query and fetch data
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM map_transaction")
table5 = mycursor.fetchall()

# Convert the result into a DataFrame
map_transaction = pd.DataFrame(table5, columns=("state","year","quarter","Districts","transaction_count","transaction_amount"))



# Execute the query and fetch data
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM map_user")
table6 = mycursor.fetchall()

# Convert the result into a DataFrame
map_user = pd.DataFrame(table6, columns=("state","year","quarter","Districts","RegisteredUsers","appOpens"))


# Execute the query and fetch data
mycursor = mydb.cursor()
mycursor.execute( "SELECT * FROM top_insurance")
table7 = mycursor.fetchall()

# Convert the result into a DataFrame
top_insurance = pd.DataFrame(table7, columns=("state","year","quarter","pincodes","transaction_count","transaction_amount"))


# Execute the query and fetch data
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM top_transaction")
table8 = mycursor.fetchall()

# Convert the result into a DataFrame
top_transaction = pd.DataFrame(table8, columns=("state","year","quarter","pincodes","transaction_count","transaction_amount"))


# Execute the query and fetch data
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM top_user")
table9 = mycursor.fetchall()

# Convert the result into a DataFrame
top_user = pd.DataFrame(table9, columns=("state","year","quarter","pincodes","Registeredusers"))



def plot_yearly_transaction_summary(df,year):
    
    tacy= df[df["year"]== year]
    tacy.reset_index(drop= True,inplace=True)

    tacyg=tacy.groupby("state")[["transaction_count","transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2= st.columns(2)
    with col1:

     fig_amount= px.bar(tacyg,x="state", y="transaction_amount",title=f"{year} TRANSACTION AMOUNT",height= 550,width=600)
     st.plotly_chart(fig_amount)

    with col2:

     fig_count= px.bar(tacyg,x="state", y="transaction_count",title=f"{year} TRANSACTION COUNT",height= 550,width=600)
     st.plotly_chart(fig_count)

    col1,col2= st.columns(2)
    with col1:

     url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
     response = requests.get(url)
     data1= json.loads(response.content)

     states_name=[]
     for feature in data1["features"]:
          states_name.append(feature["properties"]["ST_NM"])

     states_name.sort()

     fig_india_1 = px.choropleth(tacyg, geojson=data1, locations="state", featureidkey="properties.ST_NM",
                                   color="transaction_amount", color_continuous_scale="rainbow",
                                   range_color=(tacyg["transaction_amount"].min(), tacyg["transaction_amount"].max()),
                                   hover_name="state", title=f"{year} TRANSACTION AMOUNT", fitbounds= "locations",
                                   height=600, width=600)
     fig_india_1.update_geos(visible= False)
     st.plotly_chart(fig_india_1)
     

    with col2:
     
     fig_india_2 = px.choropleth(tacyg, geojson=data1, locations="state", featureidkey="properties.ST_NM",
                                        color="transaction_count", color_continuous_scale="tropic",
                                        range_color=(tacyg["transaction_count"].min(), tacyg["transaction_count"].max()),
                                        hover_name="state", title=f"{year} TRANSACTION COUNT", fitbounds= "locations",
                                        height=600, width=600)
     fig_india_2.update_geos(visible= False)
     st.plotly_chart(fig_india_2)

    return tacy


def plot_quarterly_transaction_summary(df,quarter):
    tacy= df[df["quarter"]== quarter]
    tacy.reset_index(drop= True,inplace=True)

    tacyg=tacy.groupby("state")[["transaction_count","transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)


    col1,col2= st.columns(2)
    with col1:

          fig_amount= px.bar(tacyg,x="state", y="transaction_amount",title=f"{tacy['year'].unique()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",height= 550,width=600)
          st.plotly_chart(fig_amount)

    with col2:
          fig_count= px.bar(tacyg,x="state", y="transaction_count",title=f"{tacy['year'].unique()} YEAR {quarter} QUARTER TRANSACTION COUNT",height= 550,width=600)
          st.plotly_chart(fig_count)

    col1,col2= st.columns(2)
    with col1:
         
          url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
          response = requests.get(url)
          data1= json.loads(response.content)

          states_name=[]
          for feature in data1["features"]:
               states_name.append(feature["properties"]["ST_NM"])

          states_name.sort()

          fig_india_1 = px.choropleth(tacyg, geojson=data1, locations="state", featureidkey="properties.ST_NM",
                                        color="transaction_amount", color_continuous_scale="tropic",
                                        range_color=(tacyg["transaction_amount"].min(), tacyg["transaction_amount"].max()),
                                        hover_name="state", title=f"{tacy['year'].unique()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", fitbounds= "locations",
                                        height=550, width=600)
          fig_india_1.update_geos(visible= False)
          st.plotly_chart(fig_india_1)
          st.dataframe(tacyg)

    with col2:
          
          fig_india_2 = px.choropleth(tacyg, geojson=data1, locations="state", featureidkey="properties.ST_NM",
                                        color="transaction_count", color_continuous_scale="tropic",
                                        range_color=(tacyg["transaction_count"].min(), tacyg["transaction_count"].max()),
                                        hover_name="state", title=f"{tacy['year'].unique()} YEAR {quarter} QUARTER TRANSACTION COUNT", fitbounds= "locations",
                                        height=550, width=600)
          fig_india_2.update_geos(visible= False)
          st.plotly_chart(fig_india_2)
     
    return tacy


def plot_transaction_type_summary(df,state):

    tacy= df[df["state"]== state]
    tacy.reset_index(drop= True,inplace=True)

    tacyg=tacy.groupby("transaction_type")[["transaction_count","transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2= st.columns(2)
    with col1:

          fig_pie_1= px.pie(data_frame=tacyg, names="transaction_type", values="transaction_amount",
                              width= 600, title=f"{state.upper()} TRANSACTION_AMOUNT", hole= 0.5)

          st.plotly_chart(fig_pie_1)
    with col2:

          fig_pie_2= px.pie(data_frame=tacyg, names="transaction_type", values="transaction_count",
                              width= 600, title=f"{state.upper()} TRANSACTION_COUNT", hole= 0.5)
          
          st.plotly_chart(fig_pie_2)


def plot_yearly_user_summary_1(df,year):
    aguy= df[df["year"]== year]
    aguy.reset_index(drop=True, inplace=True) 

    aguyg=pd.DataFrame(aguy.groupby("Brands")["transaction_count"].sum())
    aguyg.reset_index(inplace= True)

    fig_bar_1= px.bar(aguyg, x= "Brands",y="transaction_count", title= f"{year} BRANDS AND TRANSACTION COUNT",
                    width=800, color_discrete_sequence= px.colors.sequential.haline_r,hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguy
    

    #aggre_user_analysis
def plot_yearly_user_summary_2(df,quarter):
    aguyq= df[df["quarter"]== quarter]
    aguyq.reset_index(drop=True, inplace=True)

    aguyqg=pd.DataFrame(aguyq.groupby("Brands")["transaction_count"].sum())
    aguyqg.reset_index(inplace= True)

    fig_bar_1= px.bar(aguyqg, x= "Brands",y="transaction_count", title= f"{quarter} QUARTER,BRANDS AND TRANSACTION COUNT",
                    width=800, color_discrete_sequence= px.colors.sequential.Magma_r, hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguyq

def plot_yearly_user_summary_3(df,state):
    auyqs= df[df["state"]== state]
    auyqs.reset_index(drop= True, inplace= True)

    fig_line_1= px.line(auyqs, x= "Brands", y= "transaction_count",hover_data="transaction_amount",
                        title= "BRANDS, TRANSACTION COUNT AND PERCENTAGE", width=1000, markers= True)
    st.plotly_chart(fig_line_1)

def plot_district_transaction_summary(df,state):

    tacy= df[df["state"]== state]
    tacy.reset_index(drop= True,inplace=True)

    tacyg=tacy.groupby("Districts")[["transaction_count","transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    col1,col2= st.columns(2)
    with col1:

          fig_bar_1= px.bar(tacyg, x="transaction_amount", y= "Districts", orientation= "h", height=600,
                              title= f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence= px.colors.sequential.Mint_r)

          st.plotly_chart(fig_bar_1)
    with col2:

          fig_bar_2= px.bar(tacyg, x="transaction_count", y= "Districts", orientation= "h", height=600,
                              title= f"{state.upper()} DISTRICT AND TRANSACTION COUNT", color_discrete_sequence= px.colors.sequential.Mint_r)

          st.plotly_chart(fig_bar_2)


def plot_yearly_user_engagement_1(df, year):
    muy= df[df["year"]== year]
    muy.reset_index(drop=True, inplace=True)

    muyg=(muy.groupby("state")[["RegisteredUsers", "appOpens"]].sum())
    muyg.reset_index(inplace= True)

    fig_line_1= px.line(muyg, x= "state", y= ["RegisteredUsers", "appOpens"],
                        title= f"{year} REGISTEREDUSER AND APPOPENS", width=1000, height=800, markers= True)
    st.plotly_chart(fig_line_1)


    return muy


def plot_yearly_user_engagement_2(df, quarter):
    muyq= df[df["quarter"]== quarter]
    muyq.reset_index(drop=True, inplace=True)

    muyqg=(muyq.groupby("state")[["RegisteredUsers", "appOpens"]].sum())
    muyqg.reset_index(inplace= True)

    fig_line_1= px.line(muyqg, x= "state", y= ["RegisteredUsers", "appOpens"],
                        title= f"{quarter} QUARTER REGISTEREDUSER AND APPOPENS", width=1000, height=800, markers= True)
    st.plotly_chart(fig_line_1)


    return muyq

def plot_yearly_user_engagement_3(df, state):
    muyqs= df[df["state"]== state]
    muyqs.reset_index(drop=True, inplace=True)
    

    fig_map_user_bar_1= px.bar(muyqs, x= "RegisteredUsers", y="Districts", orientation="h",
                            title=  f"{state.upper()} REGISTERED USER", height= 800, color_discrete_sequence= px.colors.sequential.Greens_r)
    st.plotly_chart(fig_map_user_bar_1)

    fig_map_user_bar_2= px.bar(muyqs, x= "appOpens", y="Districts", orientation="h",
                            title= f"{state.upper()} APPOPENS", height= 800, color_discrete_sequence= px.colors.sequential.Blackbody_r)
    st.plotly_chart(fig_map_user_bar_2)





#top_insurance_plot_1
def plot_top_insurance_transactions(df,state):
    tiy= df[df["state"]== state]
    tiy.reset_index(drop=True, inplace=True)

    col1,col2= st.columns(2)
    with col1:
          fig_top_insur_bar_1= px.bar(tiy, x= "quarter", y="transaction_amount", hover_data= "pincodes",
                                   title= "TRANSACTION AMOUNT", height= 800, color_discrete_sequence= px.colors.sequential.Greens_r)
          st.plotly_chart(fig_top_insur_bar_1)
    with col2:
          fig_top_insur_bar_2= px.bar(tiy, x= "quarter", y="transaction_count", hover_data= "pincodes",
                                   title= "TRANSACTION COUNT", height= 800, color_discrete_sequence= px.colors.sequential.Greens_r)
          st.plotly_chart(fig_top_insur_bar_2)

def plot_yearly_top_users_1(df, year):
    tuy= df[df["year"]== year]
    tuy.reset_index(drop=True, inplace=True)

    tuyg= pd.DataFrame(tuy.groupby(["state", "quarter"])["Registeredusers"].sum())
    tuyg.reset_index(inplace= True)
    

    fig_top_plot_1= px.bar(tuyg, x= "state", y= "Registeredusers", color= "quarter", 
                        width= 800, height=800, color_discrete_sequence= px.colors.sequential.Agsunset_r, hover_data= "state", title= f"{year} REGISTERED USERS")
    st. plotly_chart(fig_top_plot_1)

    return tuy

def plot_yearly_top_users_2(df,state):
    tuys= df[df["state"]== state]
    tuys.reset_index(drop=True, inplace=True)

    fig_top_plot_2= px.bar(tuys, x= "quarter", y= "Registeredusers", hover_data="pincodes",
                        title= "REGISTERED USERS,PINCODES,QUARTERS",width=800, height=800,
                        color_continuous_scale= px.colors.sequential.Magenta,color="Registeredusers")
    st.plotly_chart(fig_top_plot_2)
    

# Establish MySQL connection
def top_chart_transaction_amount(table_name):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        port="3306",
        password="1234",
        database="phonepe_pulse"
    )
    mycursor = mydb.cursor()

    query1= f'''SELECT state, sum(transaction_amount) as transaction_amount
                FROM {table_name}
                group by state
                order by transaction_amount desc
                limit 10;'''
    mycursor.execute(query1)
    table_1= mycursor.fetchall()
    mydb.commit()
    
    df_1= pd.DataFrame(table_1, columns=("states", "transaction_amount"))
    
    col1,col2= st.columns(2)
    with col1:

          fig_bar_1= px.bar(df_1, x= "states",y="transaction_amount", title=  "TOP 10 OF TRANSACTION AMOUNT ",
                              width=800, color_discrete_sequence= px.colors.sequential.haline_r, hover_name="states")
          st.plotly_chart(fig_bar_1)

    query2= f'''SELECT state, sum(transaction_amount) as transaction_amount
                FROM {table_name}
                group by state
                order by transaction_amount 
                limit 10;'''
    mycursor.execute(query2)
    table_2= mycursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("states", "transaction_amount"))

    with col2:

          fig_bar_2= px.bar(df_2, x= "states",y="transaction_amount", title=  "LAST 10 OF TRANSACTION AMOUNT ",
                              width=800, color_discrete_sequence= px.colors.sequential.haline_r, hover_name="states")
          st.plotly_chart(fig_bar_2)


    query3= f'''SELECT state, avg(transaction_amount) as transaction_amount
                FROM {table_name}
                group by state
                order by transaction_amount;'''
    mycursor.execute(query3)
    table_3= mycursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("states", "transaction_amount"))

    fig_bar_3= px.bar(df_3, x= "transaction_amount",y="states", title=  "AVERAGE OF TRANSACTION AMOUNT ", orientation="h",
                    width=800, color_discrete_sequence= px.colors.sequential.haline_r, hover_name="states")
    st.plotly_chart(fig_bar_3)


# Establish MySQL connection
def top_chart_transaction_count(table_name):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        port="3306",
        password="1234",
        database="phonepe_pulse"
    )
    mycursor = mydb.cursor()

    query1= f'''SELECT state, sum(transaction_count) as transaction_count
                FROM {table_name}
                group by state
                order by transaction_count desc
                limit 10;'''
    mycursor.execute(query1)
    table_1= mycursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("states", "transaction_count"))
    
    col1,col2= st.columns(2)
    with col1:
          fig_bar_1= px.bar(df_1, x= "states",y="transaction_count", title=  "TOP 10 OF TRANSACTION COUNT ",
                              width=800, color_discrete_sequence= px.colors.sequential.haline_r, hover_name="states")
          st.plotly_chart(fig_bar_1)

    query2= f'''SELECT state, sum(transaction_count) as transaction_count
                FROM {table_name}
                group by state
                order by transaction_count 
                limit 10;'''
    mycursor.execute(query2)
    table_2= mycursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("states", "transaction_count"))

    with col2:
          fig_bar_2= px.bar(df_2, x= "states",y="transaction_count", title=  "LAST 10 OF TRANSACTION COUNT ",
                              width=800, color_discrete_sequence= px.colors.sequential.haline_r, hover_name="states")
          st.plotly_chart(fig_bar_2)


    query3= f'''SELECT state, avg(transaction_count) as transaction_count
                FROM {table_name}
                group by state
                order by transaction_count;'''
    mycursor.execute(query3)
    table_3= mycursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("states", "transaction_count"))

    fig_bar_3= px.bar(df_3, x= "transaction_count",y="states", title=  "AVERAGE OF TRANSACTION COUNT ", orientation="h",
                    width=800, color_discrete_sequence= px.colors.sequential.haline_r, hover_name="states")
    st.plotly_chart(fig_bar_3)

# Establish MySQL connection
def top_chart_registered_user(table_name,state):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        port="3306",
        password="1234",
        database="phonepe_pulse"
    )
    mycursor = mydb.cursor()

    query1= f'''select Districts, sum(RegisteredUsers) as registeredusers
                from {table_name}
                where state= "{state}"
                group by Districts
                order by RegisteredUsers desc
                limit 10;'''
    mycursor.execute(query1)
    table_1= mycursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("Districts", "registeredusers"))
    
    col1,col2= st.columns(2)
    with col1:
          fig_bar_1= px.bar(df_1, x= "Districts",y="registeredusers", title=  "TOP 10 OF REGISTERED USER",
                              width=800, color_discrete_sequence= px.colors.sequential.haline_r, hover_name="Districts")
          st.plotly_chart(fig_bar_1)

    query2= f'''select Districts, sum(RegisteredUsers) as registeredusers
                from {table_name}
                where state= "{state}"
                group by Districts
                order by RegisteredUsers 
                limit 10;'''
    mycursor.execute(query2)
    table_2= mycursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("Districts", "registeredusers"))
    
    with col2:
          fig_bar_2= px.bar(df_2, x= "Districts",y="registeredusers", title=  "LAST 10 OF REGISTERED USER ",
                              width=800, color_discrete_sequence= px.colors.sequential.haline_r, hover_name="Districts")
          st.plotly_chart(fig_bar_2)


    query3= f'''select Districts, avg(RegisteredUsers) as registeredusers
                from {table_name}
                where state= "{state}"
                group by Districts
                order by RegisteredUsers;'''
    mycursor.execute(query3)
    table_3= mycursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("Districts", "registeredusers"))

    fig_bar_3= px.bar(df_3, x= "registeredusers",y="Districts", title=  "AVERAGE OF REGISTERED USER ", orientation="h",
                    width=800, color_discrete_sequence= px.colors.sequential.haline_r, hover_name="Districts")
    st.plotly_chart(fig_bar_3)


# Establish MySQL connection
def top_chart_appOpens(table_name,state):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        port="3306",
        password="1234",
        database="phonepe_pulse"
    )
    mycursor = mydb.cursor()

    query1= f'''select Districts, sum(appOpens) as appOpens
                from {table_name}
                where state= "{state}"
                group by Districts
                order by appOpens desc
                limit 10;'''
    mycursor.execute(query1)
    table_1= mycursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("Districts", "appOpens"))
    
    col1,col2= st.columns(2)
    with col1:
          fig_bar_1= px.bar(df_1, x= "Districts",y="appOpens", title=  "TOP 10 OF APPOPENS",
                              width=800, color_discrete_sequence= px.colors.sequential.haline_r, hover_name="Districts")
          st.plotly_chart(fig_bar_1)

    query2= f'''select Districts, sum(appOpens) as appOpens
                from {table_name}
                where state= "{state}"
                group by Districts
                order by appOpens 
                limit 10;'''
    mycursor.execute(query2)
    table_2= mycursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("Districts", "appOpens"))
    with col2:
          fig_bar_2= px.bar(df_2, x= "Districts",y="appOpens", title=  "LAST 10 OF APPOPENS ",
                              width=800, color_discrete_sequence= px.colors.sequential.haline_r, hover_name="Districts")
          st.plotly_chart(fig_bar_2)


    query3= f'''select Districts, avg(appOpens) as appOpens
                from {table_name}
                where state= "{state}"
                group by Districts
                order by appOpens;'''
    mycursor.execute(query3)
    table_3= mycursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("Districts", "appOpens"))

    fig_bar_3= px.bar(df_3, x= "appOpens",y="Districts", title=  "AVERAGE OF APPOPENS ", orientation="h",
                    width=800, color_discrete_sequence= px.colors.sequential.haline_r, hover_name="Districts")
    st.plotly_chart(fig_bar_3)


# Establish MySQL connection
def top_chart_registered_users(table_name):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        port="3306",
        password="1234",
        database="phonepe_pulse"
    )
    mycursor = mydb.cursor()

    query1= f'''select state, sum(Registeredusers) as Registeredusers
                from {table_name}
                group by state
                order by Registeredusers desc
                limit 10;'''
    mycursor.execute(query1)
    table_1= mycursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("state", "Registeredusers"))
    col1,col2= st.columns(2)

    with col1:
          fig_bar_1= px.bar(df_1, x= "state",y="Registeredusers", title=  "TOP 10 OF REGISTERED USERS",
                              width=800, color_discrete_sequence= px.colors.sequential.haline_r, hover_name="state")
          st.plotly_chart(fig_bar_1)

    query2= f'''select state, sum(Registeredusers) as Registeredusers
                from {table_name}
                group by state
                order by Registeredusers 
                limit 10;'''
    mycursor.execute(query2)
    table_2= mycursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("state", "Registeredusers"))
     
    with col2:
          fig_bar_2= px.bar(df_2, x= "state",y="Registeredusers", title=  "LAST 10 OF REGISTERED USERS ",
                              width=800, color_discrete_sequence= px.colors.sequential.haline_r, hover_name="state")
          st.plotly_chart(fig_bar_2)


    query3= f'''select state, avg(Registeredusers) as Registeredusers
                from {table_name}
                group by state
                order by Registeredusers;'''
    mycursor.execute(query3)
    table_3= mycursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("state", "Registeredusers"))

    fig_bar_3= px.bar(df_3, x= "Registeredusers",y="state", title=  "AVERAGE OF REGISTERED USERS ", orientation="h",
                    width=800, color_discrete_sequence= px.colors.sequential.haline_r, hover_name="state")
    st.plotly_chart(fig_bar_3)


           

# Setting up page configuration
st.set_page_config(page_title="Phonepe Pulse Data Visualization",
                   layout="wide",
                   initial_sidebar_state="expanded",
                   menu_items={'About': """# This dashboard app is created for PhonePe Data Visualization!
                                          Data has been cloned from Phonepe Pulse Github Repository"""})

st.sidebar.header(":wave: :violet[**Welcome to the dashboard!**]")

# Creating option menu in the side bar
with st.sidebar:
    selected = option_menu("Menu", ["Top Charts", "Explore Data", "About"], 
                icons=["house", "graph-up-arrow", "bar-chart-line", "exclamation-circle"],
                menu_icon="menu-button-wide",
                default_index=2,
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F99AD"},
                        "nav-link-selected": {"background-color": "#6F36AD"}})

     # MENU 1 - ABOUT
if selected == "About":
     # Page header
     st.markdown("# :blue[Data Visualization and Exploration]")
     st.markdown("## :blue[A User-Friendly Tool Using Streamlit and Plotly]")

     # Tabs for better organization
     tabs = st.tabs(["Overview", "Technologies Used", "Features", "Contact"])

     # Tab 1: Overview
     with tabs[0]:
          col1, col2 = st.columns([3, 1], gap="medium")
          with col1:
               st.markdown("### :blue[Domain:] Fintech")
               st.markdown("This Streamlit app can be used to visualize the PhonePe pulse data and gain lots of insights on transactions, number of users, top 10 states, districts, and pincodes.")
               st.markdown("Bar charts, pie charts, and geo map visualizations are used to get insights.")
          with col2:
               st.image("C:/Users/USER/Downloads/ICN.png", use_column_width=True)
               
     # Tab 2: Technologies Used
     with tabs[1]:
          st.markdown("### :blue[Technologies Used:]")
          tech_images = {
               "GitHub": "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png",
               "Python": "https://www.python.org/static/community_logos/python-logo.png",
               "Pandas": "https://pandas.pydata.org/static/img/pandas_white.svg",
               "MySQL": "https://dev.mysql.com/common/logos/mysql-logo.svg?v2",
               "Streamlit": "https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png",
               "Plotly": "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
          }
          col1, col2, col3 = st.columns(3)
          col1.image(tech_images["GitHub"], width=100)
          col1.image(tech_images["Python"], width=100)
          col2.image(tech_images["Pandas"], width=100)
          col2.image(tech_images["MySQL"], width=100)
          col3.image(tech_images["Streamlit"], width=100)
          col3.image(tech_images["Plotly"], width=100)

     # Tab 3: Features
     with tabs[2]:
          st.markdown("### :blue[Features:]")
          st.markdown("- Interactive visualizations using Plotly")
          st.markdown("- User-friendly interface with Streamlit")
          st.markdown("- Comprehensive data from PhonePe Pulse")
          with st.expander("More Features"):
               st.markdown("- Customizable dashboards")
               st.markdown("- Responsive design")
               st.markdown("- Real-time data updates")

     # Tab 4: Contact
     with tabs[3]:
          st.markdown("### :blue[Contact:]")
          st.markdown("For more information, please visit [PhonePe Pulse GitHub Repository](https://github.com/PhonePe/pulse) or contact us at [support@phonepe.com](mailto:support@phonepe.com).")
          st.markdown("[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/PhonePe/pulse)")

     # Add a footer with additional information
     st.markdown("---")
     st.markdown("### :blue[About This App]")
     st.markdown("This dashboard is designed to help you explore and visualize data from PhonePe Pulse. Use the side menu to navigate through different sections and discover insights.")
     st.markdown("#### Created by:")
     st.markdown("- [ASEEM](https://github.com/AseemCodes19/AseemCodes19)")
     





     

elif selected == "Explore Data":

     tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

     with tab1:

          method = st.radio("select the method",["Insurance Analysis","Transaction Analysis","User Analysis"])

          if method == "Insurance Analysis":

               col1,col2= st.columns(2)
               with col1:

                    years= st.slider("select the year",Aggre_insurance["year"].min(),Aggre_insurance["year"].max(),Aggre_insurance["year"].min())
               tac_y= plot_yearly_transaction_summary(Aggre_insurance,years)
               


               col1,col2= st.columns(2)
               with col1:

                    quarter= st.slider("select the quarter",tac_y["quarter"].min(),tac_y["quarter"].max(),tac_y["quarter"].min())
               plot_quarterly_transaction_summary(tac_y, quarter)

          elif method == "Transaction Analysis":
               
               col1,col2= st.columns(2)
               with col1:

                    years= st.slider("select the year_ta",aggre_transaction["year"].min(),aggre_transaction["year"].max(),aggre_transaction["year"].min())
               aggre_tran_tac_y= plot_yearly_transaction_summary(aggre_transaction,years)
               
               col1,col2= st.columns(2)
               with col1:
                    state= st.selectbox("select the state_ta",aggre_tran_tac_y["state"].unique())
               plot_transaction_type_summary(aggre_tran_tac_y,state)

               col1,col2= st.columns(2)
               with col1:

                    quarter= st.slider("select the quarter_ta",aggre_tran_tac_y["quarter"].min(),aggre_tran_tac_y["quarter"].max(),aggre_tran_tac_y["quarter"].min())
               aggre_tran_tac_y_q= plot_quarterly_transaction_summary(aggre_tran_tac_y, quarter)
               
               col1,col2= st.columns(2)
               with col1:
                    state= st.selectbox("select the states_ta",aggre_tran_tac_y_q["state"].unique())
               plot_transaction_type_summary(aggre_tran_tac_y_q,state)

          elif method == "User Analysis":

               col1, col2 = st.columns(2)
               with col1:

                    years = st.slider("Select the year_ua", aggre_user["year"].min(), aggre_user["year"].max(), aggre_user["year"].min())
               aggre_user_y = plot_yearly_user_summary_1(aggre_user, years)
               
               col1,col2= st.columns(2)
               with col1:

                    quarter= st.slider("select the quarter_ua",aggre_user_y["quarter"].min(),aggre_user_y["quarter"].max(),aggre_user_y["quarter"].min())
               aggre_user_y_q= plot_yearly_user_summary_2(aggre_user_y, quarter)
               
               col1,col2= st.columns(2)
               with col1:
                    state= st.selectbox("select the states_ua",aggre_user_y_q["state"].unique())
               plot_yearly_user_summary_3(aggre_user_y_q,state)

              




     with tab2:

          method_2= st.radio("select the method",["Map Insurance","Map Transaction","Map User"])

          if method_2 == "Map Insurance":

               col1,col2= st.columns(2)
               with col1:

                    years = st.slider("select the year_mi", map_insurance["year"].min(), map_insurance["year"].max(), map_insurance["year"].min(), key="year_slider")

               map_insur_tac_y= plot_yearly_transaction_summary(map_insurance,years)

               col1,col2= st.columns(2)
               with col1:
                    state= st.selectbox("select the state_mi",map_insur_tac_y["state"].unique())

               plot_district_transaction_summary(map_insur_tac_y,state)

               col1,col2= st.columns(2)
               with col1:

                   quarter = st.slider("select the quarter_mi", map_insur_tac_y["quarter"].min(), map_insur_tac_y["quarter"].max(), map_insur_tac_y["quarter"].min(), key="quarter_slider")

               map_insur_tac_y_q= plot_quarterly_transaction_summary(map_insur_tac_y, quarter)

               col1,col2= st.columns(2)
               with col1:
                    state= st.selectbox("select the states_mi",map_insur_tac_y_q["state"].unique())

               plot_district_transaction_summary(map_insur_tac_y_q,state)


               

               
          
          elif method_2 == "Map Transaction":
               col1,col2= st.columns(2)
               with col1:

                    years = st.slider("select the year_mt", map_transaction["year"].min(), map_transaction["year"].max(), map_transaction["year"].min(), key="year_slider")

               map_tran_tac_y= plot_yearly_transaction_summary(map_transaction,years)

               col1,col2= st.columns(2)
               with col1:
                    state= st.selectbox("select the state_mt",map_tran_tac_y["state"].unique())

               plot_district_transaction_summary(map_tran_tac_y,state)

               col1,col2= st.columns(2)
               with col1:

                   quarter = st.slider("select the quarter_mt", map_tran_tac_y["quarter"].min(), map_tran_tac_y["quarter"].max(), map_tran_tac_y["quarter"].min(), key="quarter_slider")

               map_tran_tac_y_q= plot_quarterly_transaction_summary(map_tran_tac_y, quarter)

               col1,col2= st.columns(2)
               with col1:
                    state= st.selectbox("select the states_mt",map_tran_tac_y_q["state"].unique())
                    
               plot_district_transaction_summary(map_tran_tac_y_q,state)
          
          elif method_2 == "Map User":
               col1,col2= st.columns(2)
               with col1:

                    years = st.slider("select the year_mu", map_user["year"].min(), map_user["year"].max(), map_user["year"].min())

               map_user_y= plot_yearly_user_engagement_1(map_user,years)

               col1,col2= st.columns(2)
               with col1:

                   quarter = st.slider("select the quarter_mu", map_user_y["quarter"].min(), map_user_y["quarter"].max(), map_user_y["quarter"].min(), key="quarter_slider")

               map_user_y_q= plot_yearly_user_engagement_2(map_user_y, quarter)

               col1,col2= st.columns(2)
               with col1:
                    state= st.selectbox("select the states_mu",map_user_y_q["state"].unique())
                    
               plot_yearly_user_engagement_3(map_user_y_q,state)



     
     with tab3:

          method_3= st.radio("select the method",["Top Insurance","Top Transaction","Top User"])

          if method_3 == "Top Insurance":
               
               col1,col2= st.columns(2)
               with col1:

                    years = st.slider("select the year_ti", top_insurance["year"].min(), top_insurance["year"].max(), top_insurance["year"].min())

               top_insur_tac_y= plot_yearly_transaction_summary(top_insurance,years)

               col1,col2= st.columns(2)
               with col1:
                    state= st.selectbox("select the states_ti",top_insur_tac_y["state"].unique())
                    
               plot_top_insurance_transactions(top_insur_tac_y,state)
               
               col1,col2= st.columns(2)
               with col1:

                   quarter = st.slider("select the quarter_ti", top_insur_tac_y["quarter"].min(), top_insur_tac_y["quarter"].max(), top_insur_tac_y["quarter"].min())

               top_insur_tac_y_q= plot_quarterly_transaction_summary(top_insur_tac_y, quarter)

          
          elif method_3 == "Top Transaction":
               col1,col2= st.columns(2)
               with col1:

                    years = st.slider("select the year_tt", top_transaction["year"].min(), top_transaction["year"].max(), top_transaction["year"].min())

               top_tran_tac_y= plot_yearly_transaction_summary(top_transaction,years)

               col1,col2= st.columns(2)
               with col1:
                    state= st.selectbox("select the states_tt",top_tran_tac_y["state"].unique())
                    
               plot_top_insurance_transactions(top_tran_tac_y,state)
               
               col1,col2= st.columns(2)
               with col1:

                   quarter = st.slider("select the quarter_tt", top_tran_tac_y["quarter"].min(), top_tran_tac_y["quarter"].max(), top_tran_tac_y["quarter"].min())

               top_tran_tac_y_q= plot_quarterly_transaction_summary(top_tran_tac_y, quarter)
          
          elif method_3 == "Top User":

               col1,col2= st.columns(2)
               with col1:

                    years = st.slider("select the year_tu", top_user["year"].min(), top_user["year"].max(), top_user["year"].min())

               top_user_y= plot_yearly_top_users_1(top_user,years)

               col1,col2= st.columns(2)
               with col1:
                    state= st.selectbox("select the states_tu",top_user_y["state"].unique())
                    
               plot_yearly_top_users_2(top_user_y,state)


elif selected == "Top Charts":
     
     question= st.selectbox("select the question",[
          "1. transaction amount and count of aggregated insurance ",
          "2. transaction amount and count of map insurance ",
          "3. transaction amount and count of top insurance ",
          "4. transaction amount and count of aggregated transaction ",
          "5. transaction amount and count of map transaction ",
          "6. transaction amount and count of top transaction ",
          "7. transaction count of aggregated user ",
          "8. registered users of map user",
          "9. app oppens of map user ",
          "10. registered users of top user ",

     ])

     if question == "1. transaction amount and count of aggregated insurance ":
          
          st.subheader("TRANSACTION AMOUNT")
          top_chart_transaction_amount("aggregated_insurance")

          st.subheader("TRANSACTION COUNT")
          top_chart_transaction_count("aggregated_insurance")
     
     elif question == "2. transaction amount and count of map insurance ":
          
          st.subheader("TRANSACTION AMOUNT")
          top_chart_transaction_amount("map_insurance")

          st.subheader("TRANSACTION COUNT")
          top_chart_transaction_count("map_insurance")

     elif question == "3. transaction amount and count of top insurance ":
          
          st.subheader("TRANSACTION AMOUNT")
          top_chart_transaction_amount("top_insurance")

          st.subheader("TRANSACTION COUNT")
          top_chart_transaction_count("top_insurance")

     elif question == "4. transaction amount and count of aggregated transaction ":
          
          st.subheader("TRANSACTION AMOUNT")
          top_chart_transaction_amount("aggre_transaction")

          st.subheader("TRANSACTION COUNT")
          top_chart_transaction_count("aggre_transaction")

     elif question == "5. transaction amount and count of map transaction ":
          
          st.subheader("TRANSACTION AMOUNT")
          top_chart_transaction_amount("map_transaction")

          st.subheader("TRANSACTION COUNT")
          top_chart_transaction_count("map_transaction")

     elif question == "6. transaction amount and count of top transaction ":
          
          st.subheader("TRANSACTION AMOUNT")
          top_chart_transaction_amount("top_transaction")

          st.subheader("TRANSACTION COUNT")
          top_chart_transaction_count("top_transaction")

     elif question == "7. transaction count of aggregated user ":

          st.subheader("TRANSACTION COUNT")
          top_chart_transaction_count("aggre_user")

     elif question == "8. registered users of map user":
          
          state= st.selectbox("select the state",map_user["state"].unique()) 
          st.subheader("REGISTERED USERS")
          top_chart_registered_user("map_user",state)

     elif question == "9. app oppens of map user ":
          
          state= st.selectbox("select the state",map_user["state"].unique()) 
          st.subheader("APPOPENS")
          top_chart_appOpens("map_user",state)

     elif question == "10. registered users of top user ":
     
           
          st.subheader("REGISTERED USERS")
          top_chart_registered_users("top_user")