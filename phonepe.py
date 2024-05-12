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



def transaction_amount_count_Y(df,year):
    
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


def transaction_amount_count_Y_Q(df,quarter):
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


def aggre_tran_transaction_type(df,state):

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


def aggre_user_plot_1(df,year):
    aguy= df[df["year"]== year]
    aguy.reset_index(drop=True, inplace=True) 

    aguyg=pd.DataFrame(aguy.groupby("Brands")["transaction_count"].sum())
    aguyg.reset_index(inplace= True)

    fig_bar_1= px.bar(aguyg, x= "Brands",y="transaction_count", title= f"{year} BRANDS AND TRANSACTION COUNT",
                    width=800, color_discrete_sequence= px.colors.sequential.haline_r,hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguy
    

    #aggre_user_analysis
def aggre_user_plot_2(df,quarter):
    aguyq= df[df["quarter"]== quarter]
    aguyq.reset_index(drop=True, inplace=True)

    aguyqg=pd.DataFrame(aguyq.groupby("Brands")["transaction_count"].sum())
    aguyqg.reset_index(inplace= True)

    fig_bar_1= px.bar(aguyqg, x= "Brands",y="transaction_count", title= f"{quarter} QUARTER,BRANDS AND TRANSACTION COUNT",
                    width=800, color_discrete_sequence= px.colors.sequential.Magma_r, hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguyq

def aggre_user_plot_3(df,state):
    auyqs= df[df["state"]== state]
    auyqs.reset_index(drop= True, inplace= True)

    fig_line_1= px.line(auyqs, x= "Brands", y= "transaction_count",hover_data="transaction_amount",
                        title= "BRANDS, TRANSACTION COUNT AND PERCENTAGE", width=1000, markers= True)
    st.plotly_chart(fig_line_1)

def map_insur_Districts(df,state):

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


def map_user_plot_1(df, year):
    muy= df[df["year"]== year]
    muy.reset_index(drop=True, inplace=True)

    muyg=(muy.groupby("state")[["RegisteredUsers", "appOpens"]].sum())
    muyg.reset_index(inplace= True)

    fig_line_1= px.line(muyg, x= "state", y= ["RegisteredUsers", "appOpens"],
                        title= f"{year} REGISTEREDUSER AND APPOPENS", width=1000, height=800, markers= True)
    st.plotly_chart(fig_line_1)


    return muy


def map_user_plot_2(df, quarter):
    muyq= df[df["quarter"]== quarter]
    muyq.reset_index(drop=True, inplace=True)

    muyqg=(muyq.groupby("state")[["RegisteredUsers", "appOpens"]].sum())
    muyqg.reset_index(inplace= True)

    fig_line_1= px.line(muyqg, x= "state", y= ["RegisteredUsers", "appOpens"],
                        title= f"{quarter} QUARTER REGISTEREDUSER AND APPOPENS", width=1000, height=800, markers= True)
    st.plotly_chart(fig_line_1)


    return muyq

def map_user_plot_3(df, state):
    muyqs= df[df["state"]== state]
    muyqs.reset_index(drop=True, inplace=True)

    fig_map_user_bar_1= px.bar(muyqs, x= "RegisteredUsers", y="Districts", orientation="h",
                            title=  f"{state.upper()} REGISTERED USER", height= 800, color_discrete_sequence= px.colors.sequential.Greens_r)
    st.plotly_chart(fig_map_user_bar_1)

    fig_map_user_bar_2= px.bar(muyqs, x= "appOpens", y="Districts", orientation="h",
                            title= f"{state.upper()} APPOPENS", height= 800, color_discrete_sequence= px.colors.sequential.Blues)
    st.plotly_chart(fig_map_user_bar_2)

           

#streamlit part

st.set_page_config(layout="wide")
st.title("PHONEPE DATA VISUALIATION AND EXPLORATION")

with st.sidebar:
    
     select= option_menu("main menu",["HOME","DATA EXPLORATION","TOP CHARTS"])

if select == "HOME":
     pass

elif select == "DATA EXPLORATION":

     tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

     with tab1:

          method = st.radio("select the method",["Insurance Analysis","Transaction Analysis","User Analysis"])

          if method == "Insurance Analysis":

               col1,col2= st.columns(2)
               with col1:

                    years= st.slider("select the year",Aggre_insurance["year"].min(),Aggre_insurance["year"].max(),Aggre_insurance["year"].min())
               tac_y= transaction_amount_count_Y(Aggre_insurance,years)
               


               col1,col2= st.columns(2)
               with col1:

                    quarter= st.slider("select the quarter",tac_y["quarter"].min(),tac_y["quarter"].max(),tac_y["quarter"].min())
               transaction_amount_count_Y_Q(tac_y, quarter)

          elif method == "Transaction Analysis":
               
               col1,col2= st.columns(2)
               with col1:

                    years= st.slider("select the year",aggre_transaction["year"].min(),aggre_transaction["year"].max(),aggre_transaction["year"].min())
               aggre_tran_tac_y= transaction_amount_count_Y(aggre_transaction,years)
               
               col1,col2= st.columns(2)
               with col1:
                    state= st.selectbox("select the state",aggre_tran_tac_y["state"].unique())
               aggre_tran_transaction_type(aggre_tran_tac_y,state)

               col1,col2= st.columns(2)
               with col1:

                    quarter= st.slider("select the quarter",aggre_tran_tac_y["quarter"].min(),aggre_tran_tac_y["quarter"].max(),aggre_tran_tac_y["quarter"].min())
               aggre_tran_tac_y_q= transaction_amount_count_Y_Q(aggre_tran_tac_y, quarter)
               
               col1,col2= st.columns(2)
               with col1:
                    state= st.selectbox("select the states",aggre_tran_tac_y_q["state"].unique())
               aggre_tran_transaction_type(aggre_tran_tac_y_q,state)

          elif method == "User Analysis":

               col1, col2 = st.columns(2)
               with col1:

                    years = st.slider("Select the year", aggre_user["year"].min(), aggre_user["year"].max(), aggre_user["year"].min())
               aggre_user_y = aggre_user_plot_1(aggre_user, years)
               
               col1,col2= st.columns(2)
               with col1:

                    quarter= st.slider("select the quarter",aggre_user_y["quarter"].min(),aggre_user_y["quarter"].max(),aggre_user_y["quarter"].min())
               aggre_user_y_q= aggre_user_plot_2(aggre_user_y, quarter)
               
               col1,col2= st.columns(2)
               with col1:
                    state= st.selectbox("select the states",aggre_user_y_q["state"].unique())
               aggre_user_plot_3(aggre_user_y_q,state)

              




     with tab2:

          method_2= st.radio("select the method",["Map Insurance","Map Transaction","Map User"])

          if method_2 == "Map Insurance":

               col1,col2= st.columns(2)
               with col1:

                    years = st.slider("select the year", map_insurance["year"].min(), map_insurance["year"].max(), map_insurance["year"].min(), key="year_slider")

               map_insur_tac_y= transaction_amount_count_Y(map_insurance,years)

               col1,col2= st.columns(2)
               with col1:
                    state= st.selectbox("select the state",map_insur_tac_y["state"].unique())

               map_insur_Districts(map_insur_tac_y,state)

               col1,col2= st.columns(2)
               with col1:

                   quarter = st.slider("select the quarter", map_insur_tac_y["quarter"].min(), map_insur_tac_y["quarter"].max(), map_insur_tac_y["quarter"].min(), key="quarter_slider")

               map_insur_tac_y_q= transaction_amount_count_Y_Q(map_insur_tac_y, quarter)

               col1,col2= st.columns(2)
               with col1:
                    state= st.selectbox("select the states",map_insur_tac_y_q["state"].unique())

               map_insur_Districts(map_insur_tac_y_q,state)


               

               
          
          elif method_2 == "Map Transaction":
               col1,col2= st.columns(2)
               with col1:

                    years = st.slider("select the year", map_transaction["year"].min(), map_transaction["year"].max(), map_transaction["year"].min(), key="year_slider")

               map_tran_tac_y= transaction_amount_count_Y(map_transaction,years)

               col1,col2= st.columns(2)
               with col1:
                    state= st.selectbox("select the state",map_tran_tac_y["state"].unique())

               map_insur_Districts(map_tran_tac_y,state)

               col1,col2= st.columns(2)
               with col1:

                   quarter = st.slider("select the quarter", map_tran_tac_y["quarter"].min(), map_tran_tac_y["quarter"].max(), map_tran_tac_y["quarter"].min(), key="quarter_slider")

               map_tran_tac_y_q= transaction_amount_count_Y_Q(map_tran_tac_y, quarter)

               col1,col2= st.columns(2)
               with col1:
                    state= st.selectbox("select the states",map_tran_tac_y_q["state"].unique())
                    
               map_insur_Districts(map_tran_tac_y_q,state)
          
          elif method_2 == "Map User":
               col1,col2= st.columns(2)
               with col1:

                    years = st.slider("select the year", map_user["year"].min(), map_user["year"].max(), map_user["year"].min())

               map_user_y= map_user_plot_1(map_user,years)

               col1,col2= st.columns(2)
               with col1:

                   quarter = st.slider("select the quarter", map_user_y["quarter"].min(), map_user_y["quarter"].max(), map_user_y["quarter"].min(), key="quarter_slider")

               map_user_y_q= map_user_plot_2(map_user_y, quarter)

               col1,col2= st.columns(2)
               with col1:
                    state= st.selectbox("select the states",map_user_y_q["state"].unique())
                    
               map_user_plot_3(map_user_y_q,state)



     
     with tab3:

          method_3= st.radio("select the method",["Top Insurance","Top Transaction","Top User"])

          if method_3 == "Top Insurance":
               
               col1,col2= st.columns(2)
               with col1:

                    years = st.slider("select the year", top_transaction["year"].min(), top_transaction["year"].max(), top_transaction["year"].min())

               top_insur_tac_y= transaction_amount_count_Y(top_transaction,years)
          
          elif method_3 == "Top Transaction":
               pass
          
          elif method_3 == "Top User":
               pass


elif select == "TOP CHARTS":
     pass


