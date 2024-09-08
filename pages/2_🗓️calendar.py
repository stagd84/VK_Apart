# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 13:39:38 2024

@author: dstan
"""

import streamlit as st
import pandas as pd

st.set_page_config(page_title='Calendar', page_icon='🗓️')
st.title("🗓️  My Calendar")

# Check if the DataFrame is available in session state
if 'df' in st.session_state:
    df = st.session_state.df
    
    # Ensure the date column is in datetime format
    df['Ημερομηνία'] = pd.to_datetime(df['Ημερομηνία']).dt.date

    # Filter data for the current year
    available_years = df['Έτος'].unique()
    available_years=sorted(available_years, reverse=True)
    current_year = st.selectbox("Select Year", options=available_years)
    df_current_year = df[df['Έτος'] == current_year]

    # Month slider
    available_months = df_current_year['Μήνας'].unique()
    month_order = ['Jun', 'Jul', 'Aug', 'Sep', 'OffSea']
    month = st.selectbox("Select Month", options=available_months)

    # Filter data for the selected month
    df_filtered = df_current_year[df_current_year['Μήνας'] == month]

######################## 1st Pivot Table
    # Create pivot table
    df_pivot_table = df_filtered.pivot_table(values='Τιμή',index='Ημερομηνία',columns='Διαμέρισμα',aggfunc='sum',fill_value=0)
    # Apply conditional formatting to flag zero values
    def highlight_zero(val):
        color = 'red' if val == 0 else ''
        return f'background-color: {color}'
    styled_pivot_table = df_pivot_table.style.applymap(highlight_zero)
    
############################ 2nd Pivot
    df_pivot = df_filtered.pivot(index='Ημερομηνία', columns='Διαμέρισμα', values='Όνομα')
    df_pivot=df_pivot.fillna('Κενό')
    # Apply conditional formatting to flag zero values
    def highlight_nan(val):
        color = 'red' if val == 'Κενό' else ''
        return f'background-color: {color}'
    styled_pivot = df_pivot.style.applymap(highlight_nan)

############################# 3rd df
    df_vac = df_filtered[df_filtered['ΚΕΝΑ']==1]
    
# Display the pivot & pivot table
    st.subheader(f"Calendar with Names for {month} of {current_year}")
    st.dataframe(styled_pivot)
    st.subheader(f"Calendar with Prices for {month} of {current_year}")
    st.dataframe(styled_pivot_table)
    st.subheader(f"Available Dates for {month} of {current_year} : {len(df_vac)}")
    st.dataframe(df_vac[['Ημερομηνία', 'Διαμέρισμα']].sort_values(by='Ημερομηνία'), hide_index=True)
    
else:
    st.write("No DataFrame found in session state. Please upload a CSV file on the main page.")
