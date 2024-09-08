# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 00:37:52 2024

@author: dstan
"""

import streamlit as st
import pandas as pd

st.set_page_config(page_title='Customers', page_icon='🤵')
st.title("🤵  Customer")

# Check if the DataFrame is available in session state
if 'df' in st.session_state:
    df = st.session_state.df
    
    customer_name = st.text_input('Start typing the customer name and press Enter to see the options')
    if customer_name:
        filtered_names = df[df['Όνομα'].str.contains(customer_name, case=False, na=False)]['Όνομα'].unique()
        selected_name = st.selectbox('**Select a customer  ➡️**', filtered_names)
        
        # Display the filtered DataFrame based on the selected name
        if selected_name:
            filtered_df = df[df['Όνομα'] == selected_name]
            st.write(filtered_df[['Όνομα','Χώρα', 'Ημερομηνία', 'Ημέρα', 'Διαμέρισμα','Τιμή', 'Κανάλι']].to_html(index=False), unsafe_allow_html=True)
    else:
        st.write("Please start typing to see matching customer names.")
    
    
else:
    st.write("No DataFrame found in session state. Please upload a CSV file on the main page.")       
    
 

