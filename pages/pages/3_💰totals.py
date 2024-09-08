# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 22:47:18 2024

@author: dstan
"""

import streamlit as st
import pandas as pd

st.set_page_config(page_title='Totals', page_icon='💰')
st.title("💰  Totals")
# create tabs
tab1, tab2 = st.tabs(["Totals Tables 🥇", "Average Price Table 🥈"])

# Check if the DataFrame is available in session state
if 'df' in st.session_state:
    df = st.session_state.df
    
    # Ensure the date column is in datetime format
    df['Ημερομηνία'] = pd.to_datetime(df['Ημερομηνία']).dt.date
    # Ensure the 'Έτος' column is an integer
    df['Έτος'] = df['Έτος'].astype(int)
    
    with tab1:
    ############### totals per year month    
        unique_apartments = df['Διαμέρισμα'].unique()
        selected_apartments = st.multiselect('Select Apartments for the tables of this tab', unique_apartments, default=unique_apartments)
        df_filtered = df[df['Διαμέρισμα'].isin(selected_apartments)]
        
        df_pivot_table = df_filtered.pivot_table(values='Τιμή',index='Έτος',columns='Μήνας',aggfunc='sum',fill_value=0, margins=True, margins_name='Total')
        custom_order = ["Jun", "Jul", "Aug", "Sep", "OffSea", "Total"]
        df_pivot_table = df_pivot_table.reindex(columns=custom_order, fill_value=0)
        df_pivot_table = df_pivot_table.round(decimals=0)
    
    ############# No Customer
        df_available = df_filtered[df_filtered['ΚΕΝΑ']==1]
        df_pivot_table2 = df_available.pivot_table(values='Ημερομηνία',index=['Έτος'],columns='Μήνας',aggfunc='count',fill_value=0, margins=True, margins_name='Total')
        custom_order = ["Jun", "Jul", "Aug", "Sep", "OffSea"]
        df_pivot_table2 = df_pivot_table2.reindex(columns=custom_order, fill_value=0)
        
    ############### totals per type of customer 
        df_pivot_table4 = df_filtered.pivot_table(values='Τιμή',index='Έτος',columns='Κανάλι',aggfunc='sum',fill_value=0, margins=True, margins_name='Total')
        df_pivot_table4 = df_pivot_table4.round(decimals=0)
    
    ############### totals per country 
        df_pivot_table5 = df_filtered.pivot_table(values='Τιμή',index='Έτος',columns='Χώρα',aggfunc='sum',fill_value=0, margins=True, margins_name='Total')
        df_pivot_table5= df_pivot_table5.round(decimals=0)
      
    ############# display 
        st.subheader("Totals per Year / Month")
        st.dataframe(df_pivot_table)
        st.subheader("No Customers")
        st.dataframe(df_pivot_table2)
        st.subheader("Totals per Type of Customer")
        st.dataframe(df_pivot_table4)
        st.subheader("Totals per Country")
        st.dataframe(df_pivot_table5)
        
    with tab2:
        ############# average price 
        df_booked = df[df['ΚΕΝΑ']==0]
        df_pivot_table3 = df_booked.pivot_table(values='Τιμή',index=['Διαμέρισμα', 'Έτος'],columns='Μήνας',aggfunc='mean',fill_value=0)
        custom_order = ["Jun", "Jul", "Aug", "Sep", "OffSea"]
        df_pivot_table3 = df_pivot_table3.reindex(columns=custom_order, fill_value=0)
        df_pivot_table3 = df_pivot_table3.round(decimals=0)
    # Format the MultiIndex to display the year correctly
        df_pivot_table3.index = df_pivot_table3.index.set_levels(
        df_pivot_table3.index.levels[1].map(lambda x: f'{x:.0f}'), level=1)
        
        ############# display 
        st.subheader("Avg Price per Year / Apartment / Month")
        st.dataframe(df_pivot_table3)

else:
    st.write("No DataFrame found in session state. Please upload a CSV file on the main page.")    