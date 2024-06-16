
#librarys

import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
import mysql
import mysql.connector
import pandas as pd
import requests
import json


config = {
    "user":"root","password":"arun2311",
    "host":"127.0.0.1","database":"phonepe"
}

connection = mysql.connector.connect(**config)
cursor = connection.cursor()


with st.sidebar:
    select = option_menu("Menu",
                    ['Home',"Analysis","Insights"])


if select=="Home":
    st.title(':violet[PHONEPE PULSE DATA VISUALISATION]')
    st.subheader(':violet[Phonepe Pulse]:')
    st.write("PhonePe Pulse is a data analytics tool provided by PhonePe, a digital payments platform in India. It offers insights and analytics based on transactions and interactions that occur on the PhonePe platform.")
    st.subheader(':violet[Phonepe Pulse Data Visualisation]:')
    st.write("PhonePe Pulse data visualization is the process of presenting data from PhonePe Pulse in visual formats such as charts, graphs, and tables. This visualization helps users understand and analyze transaction patterns, user behavior, and other insights derived from the data."
             " Visualizing PhonePe Pulse data can provide businesses with valuable insights to improve their services, optimize marketing strategies, and make informed decisions based on the data trends.")
    st.markdown("## :violet[Done by] : ARUNACHALAM K")



if select == "Analysis":
    select = option_menu(None,
                         options=["INDIA","STATE","TOP CATEGORIES"],
                         orientation="horizontal")
    if select == "INDIA":
        tab1,tab2 = st.tabs(["TRANSACTION","USER"])

        with tab1:
            clm1,clm2,clm3 = st.columns(3)

            with clm1:
                trns_year = st.selectbox('Select Year',(2018,2019,2020,2021,2022), key='trns_year')

            with clm2:
                trns_qtr = st.selectbox('Select Quarter', [1, 2, 3, 4], key= 'trns_qtr')

            with clm3:
                trns_type = st.selectbox('Select Transaction_type', [
                                            'Recharge & bill payments', 'Peer-to-peer payments',
                                             'Merchant payments', 'Financial Services', 'Others'], key='trns_type')
                

                                            # SQL Query

            # Transaction Analysis bar chart query
            
            query = "SELECT State, Transaction_amount FROM agg_trans WHERE Year = %s AND Quarter = %s AND Transaction_type = %s;"
            cursor.execute(query,(trns_year,trns_qtr,trns_type))
            anls_bar = cursor.fetchall()
            df_anls_bar = pd.DataFrame (anls_bar, columns=['State', 'Transaction_amount'])
            st.dataframe(df_anls_bar)
            
          

            # Transaction Analysis table query
            query = "SELECT State, Transaction_count, Transaction_amount FROM agg_trans WHERE Year = %s AND Quarter = %s AND Transaction_type = %s;"
            cursor.execute(query,(trns_year,trns_qtr,trns_type))
            anls_tab = cursor.fetchall()
            df_anls_tab = pd.DataFrame(anls_tab,columns=['State', 'Transaction_count', 'Transaction_amount'])
            st.dataframe(df_anls_tab)



            
# ----------------------------/ GEO VISUALISATION FOR TRANS \----------------------------------------#

            # Drop a State column from df_anls_bar  
            df_anls_bar .drop(columns=['State'], inplace=True)
            # Clone the gio data
            url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response = requests.get(url)
            data1 = json.loads(response.content)
            # Extract state names and sort them in alphabetical order
            state_names_tra = [feature['properties']['ST_NM'] for feature in data1['features']]
            state_names_tra.sort()
            # Create a DataFrame with the state names column
            df_state_names_tra = pd.DataFrame({'State': state_names_tra})
            # Combine the Gio State name with df_in_tr_tab_qry_rslt
            df_state_names_tra['Transaction_amount'] = df_anls_bar 
            # convert dataframe to csv file
            df_state_names_tra.to_csv('State_trans.csv', index=False)
            # Read csv
            df_tra = pd.read_csv('State_trans.csv')
            # Geo plot
            fig_tra = px.choropleth(
                df_tra,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM', locations='State', color='Transaction_amount',hover_name="State",
                color_continuous_scale='thermal', title='Transaction Analysis')
            fig_tra.update_geos(fitbounds="locations", visible=False)
            fig_tra.update_layout(title_font=dict(size=33), height=800)
            st.plotly_chart(fig_tra, use_container_width=True)


            
            # Create a bar chart using Plotly
            fig = px.bar(df_anls_tab, x='State', y='Transaction_count', title='Transaction Count by State',color_continuous_scale='thermal',height=600)
            st.plotly_chart(fig)


            
        # USER TAB
        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                user_yr = st.selectbox('**Select Year**', (2018,2019,2020,2021,2022), key='in_us_yr')
            with col2:
                user_qtr = st.selectbox('**Select Quarter**', (1,2,3,4), key='in_us_qtr')


            # SQL Query

            # User Analysis Bar chart query

            query = "SELECT State, SUM(count) FROM agg_user WHERE Year = %s AND Quarter = %s GROUP BY State;"
            cursor.execute(query,(user_yr,user_qtr))
            us_an_br_ch = cursor.fetchall()
            df_us_an_br_ch = pd.DataFrame (us_an_br_ch, columns=['State','count'])
            st.dataframe(df_us_an_br_ch)



            
 #------------------------------/ GEO VISUALIZATION FOR USER \-------------------------#


            # Assuming df_us_an_br_ch is your DataFrame with the 'Transaction_amount' data
            # Check if 'State' column exists and drop it if it does
            if 'State' in df_us_an_br_ch.columns:
                df_us_an_br_ch.drop(columns=['State'], inplace=True)

            # Fetch the geojson data
            url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response = requests.get(url)
            data1 = json.loads(response.content)

            # Extract state names and sort them in alphabetical order
            state_names_tra = [feature['properties']['ST_NM'] for feature in data1['features']]
            state_names_tra.sort()

            # Create a DataFrame with the state names column
            df_state_names_tra = pd.DataFrame({'State': state_names_tra})

            # Ensure df_us_an_br_ch has the 'count' column
            if 'count' in df_us_an_br_ch.columns:
                # Assuming df_us_an_br_ch has the same number of rows as df_state_names_tra
                df_state_names_tra['Transaction_amount'] = df_us_an_br_ch['count'].values
            else:
                st.error("The DataFrame df_us_an_br_ch does not contain the 'count' column.")

            # Convert DataFrame to CSV file
            df_state_names_tra.to_csv('State_user.csv', index=False)

            # Read the CSV back into a DataFrame (if needed)
            df_tra = pd.read_csv('State_user.csv')

            # Geo plot
            fig_tra = px.choropleth(
                df_tra, geojson=data1, featureidkey='properties.ST_NM',
                locations='State', color='Transaction_amount', 
                hover_name='State', color_continuous_scale='thermal',
                title='Transaction Analysis'
            )
            fig_tra.update_geos(fitbounds="locations", visible=False)
            fig_tra.update_layout(title_font=dict(size=33), height=800)
            st.plotly_chart(fig_tra, use_container_width=True)





# -----------------------------/  STATE TAB \----------------------------#
                    
    if select == "STATE":
        tab3,tab4 = st.tabs(["TRANSACTION","USER"])

        #TRANSACTION TAB FOR STATE

        with tab3:
            clm1,clm2,clm3 = st.columns(3)
            with clm1:
                st_tr_st = st.selectbox('**Select State**',('Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                        'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                        'Dadra And Nagar Haveli And Daman And Diu', 'Delhi', 'Goa',
                        'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                        'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                        'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                        'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                        'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                        'Uttarakhand', 'West Bengal') , key = 'st_tr_st')
            
            with clm2:
                st_tr_yr = st.selectbox('**Select Year**',(2018,2019,2020,2021,2022),key='st_tr_yr')
            with clm3:
                st_yr_qtr = st.selectbox('**Select Quarter**',(1,2,3,4),key ='st_yr_qtr')




            # State wise amount analysis

            query = "SELECT State, total_amount FROM map_trans WHERE State = %s AND year = %s AND Quarter = %s;"
            cursor.execute(query,(st_tr_st,st_tr_yr,st_yr_qtr))
            df = cursor.fetchall()
            df1 = pd.DataFrame(df, columns=['State','total_amount'])
            st.dataframe(df1)


            # Total Transaction Amount avg

            query = "select sum(Transaction_amount),avg(Transaction_amount) from agg_trans where State = %s and Year = %s and Quarter =%s;"
            cursor.execute(query,(st_tr_st,st_tr_yr,st_yr_qtr))
            df = cursor.fetchall()
            df1 =pd.DataFrame(df,columns=['Total_amount', 'Average'])
            st.dataframe(df1)

            # Total Transaction Count avg

            query = "SELECT SUM(Transaction_count) AS Total_Transactions, AVG(Transaction_count) AS Average_Transactions FROM agg_trans WHERE State = %s AND Year = %s AND Quarter = %s;"
            cursor.execute(query, (st_tr_st, st_tr_yr, st_yr_qtr))
            df = cursor.fetchall()
            df1 = pd.DataFrame(df, columns=['Total_count', 'Average'])
            st.dataframe(df1)

                    
        with tab4:
            clm4,clm5 = st.columns(2)
            with clm4:
                st_ur_st = st.selectbox('**Select State**',('Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                        'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                        'Dadra And Nagar Haveli And Daman And Diu', 'Delhi', 'Goa',
                        'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                        'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                        'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                        'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                        'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                        'Uttarakhand', 'West Bengal') , key = 'st_ur_st')
            
            with clm5:
                st_ur_yr = st.selectbox('**Select Year**',(2018,2019,2020,2021,2022),key='st_ur_yr')

            # state and district wise user analysis

            query = "SELECT State, Year, District ,registeredUsers FROM map_user where State = %s and Year = %s;" 
            cursor.execute(query, (st_ur_st, st_ur_yr))
            result = cursor.fetchall()
            df = pd.DataFrame(result, columns=['State','Year','District','registeredUsers'])
            st.dataframe(df)


            # state and district wise user analysis scatter plot
            fig = px.scatter(df, x='District', y='registeredUsers', title='registeredUsers by State and District', color='State', 
                            color_continuous_scale='thermal', height=600)
            st.plotly_chart(fig)


            # state wise transaction count analysis in quarter

            query = "select Quarter, sum(count) from agg_user where State =%s and Year = %s group by Quarter;"
            cursor.execute(query, (st_ur_st, st_ur_yr))
            ur_an_bar = cursor.fetchall()
            df_ur_an_bar = pd.DataFrame(ur_an_bar,columns=['Quarter','user_count'])
            st.dataframe(df_ur_an_bar)

            # state wise transaction count analysis in quarter by pie chart

            fig = px.pie(df_ur_an_bar, names='Quarter', values= 'user_count', title='Total count by State',color_discrete_sequence=px.colors.sequential.ice)
            st.plotly_chart(fig)

            # total transaction count average

            query = "select sum(count),  avg (count) from agg_user where State=%s and Year=%s;"
            cursor.execute(query, (st_ur_st, st_ur_yr))
            tl_us_cu_tab = cursor.fetchall()
            df_tl_us_cu_tab = pd.DataFrame(tl_us_cu_tab,columns=['Total', 'count_Average'])
            st.dataframe(df_tl_us_cu_tab)


# -------------------------------/  TOP CATEGORIES  \-----------------------------#



    if select == "TOP CATEGORIES":
        tab5,tab6 = st.tabs(["TRANSACTION", "USER"])

        with tab5:
            top_tr_yr = st.selectbox('**Select Year**',(2018,2019,2020,2021,2022),key ='top_tr_yr')

            # top transaction count by

            query ="SELECT State, SUM(total_count) AS total_count FROM top_trans WHERE Year = %s GROUP BY State ORDER BY total_count DESC LIMIT 10;"
            cursor.execute(query,(top_tr_yr,))
            top_tr_ans_bar = cursor.fetchall()
            df_top_tr_ans_bar = pd.DataFrame(top_tr_ans_bar,columns=['State','total_count'])
            st.dataframe(df_top_tr_ans_bar)

           # top transaction count by in pie chart

            fig = px.pie(df_top_tr_ans_bar, names='State', values='total_count', title='Total count by State',color_discrete_sequence=px.colors.sequential.ice)
            st.plotly_chart(fig)

            # top transaction amount by

            query = "SELECT State, SUM(total_amount) AS total_amount FROM top_trans WHERE Year = %s  GROUP BY State ORDER BY total_amount DESC LIMIT 10;"
            cursor.execute(query, (top_tr_yr,))
            top_tr_ans_tab = cursor.fetchall()
            df_top_tr_ans_tab = pd.DataFrame(top_tr_ans_tab, columns=['State', 'total_amount'])
            st.dataframe(df_top_tr_ans_tab)

            # top transaction amount by in pie chart

            fig = px.pie(df_top_tr_ans_tab, names='State', values='total_amount', title='Total Amount by State',color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig)


        with tab6:
            top_ur_yr = st.selectbox('**Select Year**',(2018,2019,2020,2021,2022),key ='top_ur_yr')


            # total transaction states user by

            query = "SELECT State, SUM(registeredUsers) AS registeredUsers FROM top_user WHERE Year = %s GROUP BY State ORDER BY SUM(registeredUsers) DESC LIMIT 10;"
            cursor.execute(query, (top_ur_yr,))
            top_ur_ans_bar = cursor.fetchall()
            df_top_ur_ans_bar = pd.DataFrame(top_ur_ans_bar, columns=["State", "registeredUsers"])
            st.dataframe(df_top_ur_ans_bar)

            # total transaction states user by pie chart

            fig = px.pie(df_top_ur_ans_bar, names='State', values='registeredUsers', title='Total transaction user by state', color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig)


    

#-------------------------------/ INSIGHTS TAB \---------------------------------------#

if select == "Insights":
    st.title(':violet[BASIC INSIGHTS]')
    st.subheader("The fundamental insights stem from analyzing the PhonePe Pulse data, offering a lucid understanding of the analyzed information.")
    questions = st.selectbox("select your question",
                [" select... ",
    
                "1.Which districts had the highest transaction count in 2018 (top 5)?",
                "2.Which are the top 10 states based on transaction amount?", 
                "3.What are the least 10 districts based on the transaction count in the 'map_trans' table?",
                "4.What are the top 10 mobile brands based on the user count of transactions in the 'agg_user' table?",
                "5.Which states had the lowest transaction count in 2018 according to the 'top_trans' table?",
                "6.What are the top transaction types based on transaction count?",             
                "7.What are the total transaction amounts for the 10 districts with the lowest transaction volume?",
                "8.What are the top 5 states with the highest number of transactions in 2022?",
                "9.Which districts have the top 5 registered users?",
                "10.Which districts have the lowest total transaction count?"
                ])
    
    
    if questions == "1.Which districts had the highest transaction count in 2018 (top 5)?":
        query = "SELECT District, SUM(total_count) AS total_count FROM map_trans  WHERE YEAR = 2018  GROUP BY District  ORDER BY total_count DESC  LIMIT 5;"
        cursor.execute(query)
        df = pd.DataFrame(cursor.fetchall(), columns=['District', 'total_count'])
        fig = px.bar(df, x='District', y='total_count', color='District', 
                    title='Top 5 Districts by Transaction Count in 2018',
                    labels={'total_count': 'Total Transaction Count', 'District': 'District'})
        st.plotly_chart(fig)
                
    
    elif questions == "2.Which are the top 10 states based on transaction amount?":
        query = "SELECT State, SUM(total_amount) AS total_amount FROM top_trans GROUP BY State ORDER BY total_amount DESC LIMIT 10;"
        cursor.execute(query)
        df2 = pd.DataFrame(cursor.fetchall(),columns=["State","total_amount"])
        fig = px.bar(df2, x = "State",y = "total_amount",title = 'top 10 states based on transaction amount')
        st.plotly_chart(fig)   

    elif questions == "3.What are the least 10 districts based on the transaction count in the 'map_trans' table?":
        query = "SELECT District, COUNT(*) AS total_count FROM map_trans GROUP BY District ORDER BY total_count ASC LIMIT 10;"
        cursor.execute(query)
        df3 = pd.DataFrame(cursor.fetchall(), columns=["District", "total_count"])
        fig = px.bar(df3, x="District", y="total_count", title="Top 10 Districts based on Transaction Count", labels={"District": "District", "total_count": "Transaction Count"})
        st.plotly_chart(fig)


    elif questions == "4.What are the top 10 mobile brands based on the user count of transactions in the 'agg_user' table?":
        query = "SELECT brands, COUNT(*) AS count FROM agg_user GROUP BY brands ORDER BY count DESC LIMIT 10;"
        cursor.execute(query)
        df4 = pd.DataFrame(cursor.fetchall(), columns=["brands", "count"])
        fig = px.pie(df4, values="count", names="brands", title="Top 10 Mobile Brands based on User Count")
        st.plotly_chart(fig)

    elif questions == "5.Which states had the lowest transaction count in 2018 according to the 'top_trans' table?":
        query = "SELECT State, COUNT(*) AS total_count FROM top_trans WHERE Year = 2018 GROUP BY State ORDER BY total_count ASC LIMIT 5;"
        cursor.execute(query)
        df5 = pd.DataFrame(cursor.fetchall(), columns=["State","total_count"])
        fig = px.pie(df5, values="total_count", names = "State", title= "lowest transaction count in 2018")
        st.plotly_chart(fig)

    elif questions == "6.What are the top transaction types based on transaction count?":
        query = "SELECT transaction_type, COUNT(*) as transaction_count FROM agg_trans GROUP BY transaction_type ORDER BY transaction_count DESC LIMIT 10;"
        cursor.execute(query)
        df6 = pd.DataFrame(cursor.fetchall(),columns=['Transaction_type','Transaction_count'])
        fig = px.bar(df6, x = 'Transaction_type', y ='Transaction_count', title="top transaction types based on transaction count")
        st.plotly_chart(fig)

    elif questions =="7.What are the total transaction amounts for the 10 districts with the lowest transaction volume?":
        query = "SELECT district,SUM(total_amount) AS total_amount FROM  map_trans GROUP BY District ORDER BY  total_amount LIMIT 10;"
        cursor.execute(query)
        df7 = pd.DataFrame(cursor.fetchall(),columns=['District','total_amount'])
        fig = px.bar(df7, x = 'District', y = 'total_amount', title=' total transaction amounts for the 10 districts')
        st.plotly_chart(fig)

    elif questions =="8.What are the top 5 states with the highest number of transactions in 2022?":
        query = "SELECT State,COUNT(*) AS total_count FROM  map_trans WHERE  YEAR = 2022 GROUP BY State ORDER BY  total_count DESC LIMIT 5;"
        cursor.execute(query)
        df8 = pd.DataFrame(cursor.fetchall(), columns=["State","total_count"])
        fig = px.pie(df8, values="total_count", names="State", title="top 5 states with the highest number of transactions")
        st.plotly_chart(fig)

    elif questions == "9.Which districts have the top 5 registered users?":
            query = "SELECT District, SUM(registeredUsers) AS registeredUsers  FROM map_user  GROUP BY District  ORDER BY registeredUsers DESC  LIMIT 5;"
            cursor.execute(query)
            df = pd.DataFrame(cursor.fetchall(), columns=['District', 'registeredUsers'])
            fig = px.bar(df, x='District', y='registeredUsers', color='District', 
                        title='Top 5 Districts by Number of Registered Users',
                        labels={'registeredUsers': 'Total Registered Users', 'District': 'District'})
            st.plotly_chart(fig)

    elif questions == "10.Which districts have the lowest total transaction count?":
        query = "SELECT District, COUNT(*) AS total_count FROM map_trans GROUP BY District ORDER BY total_count LIMIT 5;"
        cursor.execute(query)
        df10 = pd.DataFrame(cursor.fetchall(), columns=['District','total_count'])
        fig = px.pie(df10, values='total_count', names='District', title='lowest total transaction count')
        st.plotly_chart(fig)

    


    

