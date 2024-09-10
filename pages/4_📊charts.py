# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 22:52:51 2024

@author: dstan
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter # for putting % in yaxis of chart

st.set_page_config(page_title='Charts', page_icon='📊')
st.title("📊  Charts")

# Check if the DataFrame is available in session state
if 'df' in st.session_state:
    df = st.session_state.df
    
    # Ensure the column format
    df['Ημερομηνία'] = pd.to_datetime(df['Ημερομηνία']).dt.date
    df['Έτος'] = df['Έτος'].astype(int)

    #### new column period
    def determine_period(month):
        if month in ['Jul', 'Aug']:
            return '☝️ High'
        else:
            return '👇 Low'
    df['Period'] = df['Μήνας'].apply(determine_period)
    
    ### new column type of customer and some changes
    df['Κανάλι Πελάτη'] = df['Κανάλι']
    df.loc[(df['Κανάλι'] == 'TripAdvisor') & (df['Έτος'] == 2017), 'Κανάλι Πελάτη'] = 'Booking'
    df.loc[(df['Κανάλι'] == 'TripAdvisor') & (df['Έτος'] == 2022), 'Κανάλι Πελάτη'] = 'AirBnb'
    df.loc[(df['Κανάλι'] == 'Chalkidiki'), 'Κανάλι Πελάτη'] = 'MyClient'
    
    ### new column country of customer
    Balkans = ['RO', 'MK', 'MO', 'BG', 'SR', 'MN', 'AL']
    USSR = ['RU', 'UK', 'BY']
    df['Χώρα Πελάτη'] = 'Rest'
    df.loc[(df['Χώρα'] == 'GR'), 'Χώρα Πελάτη'] = 'Greek'
    df.loc[(df['Χώρα'].isin(USSR)), 'Χώρα Πελάτη'] = 'USSR'
    df.loc[(df['Χώρα'].isin(Balkans)), 'Χώρα Πελάτη'] = 'Balkans'
    
    unique_periods = df['Period'].unique()
    selected_periods = st.multiselect('**Select Period for charts of this tab ➡️   Low = Jun-Sep-OffSea  /  High = Jul-Aug**', unique_periods, default=unique_periods)
    df_filtered = df[df['Period'].isin(selected_periods)]
    st.markdown("<br>", unsafe_allow_html=True) # adds blank line
    
    available_columns=['Διαμέρισμα','Κανάλι Πελάτη', 'Χώρα Πελάτη']
    my_col_chart = st.selectbox("**Select Field for the next two Charts**", options=available_columns)
    df_pivot_table = df_filtered.pivot_table(values='Τιμή',index='Έτος',columns=my_col_chart, aggfunc='sum',fill_value=0)
    
    colors = {'Apartment 1': 'brown', 'Apartment 2': 'green', 'Cottage 1': 'red', 'Cottage 2':'yellow'}
    widths = {'Apartment 1': 2, 'Apartment 2': 2, 'Cottage 1': 2, 'Cottage 2':2}
    
    fig, ax = plt.subplots(figsize=(10, 6))
    for column in df_pivot_table.columns:
        if my_col_chart=='Διαμέρισμα':
            ax.plot(df_pivot_table.index, df_pivot_table[column], label=column, color=colors.get(column, '#000000'), linewidth=widths.get(column, 1))
        else:
            ax.plot(df_pivot_table.index, df_pivot_table[column], label=column, linewidth=2)
    ax.set_xlabel('Year')
    ax.set_ylabel('Price')
    ax.set_title('Absolute Values by Year',bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
    ax.legend(title=my_col_chart)
    ax.grid(True)
    st.pyplot(fig)
    
    df_pivot_table_percentage = df_pivot_table.div(df_pivot_table.sum(axis=1), axis=0) * 100
    fig, ax = plt.subplots(figsize=(10, 6))
    for column in df_pivot_table_percentage.columns:
        if my_col_chart=='Διαμέρισμα':
            ax.plot(df_pivot_table_percentage.index, df_pivot_table_percentage[column], label=column, color=colors.get(column, '#000000'), linewidth=widths.get(column, 1))
        else:
            ax.plot(df_pivot_table_percentage.index, df_pivot_table_percentage[column], label=column, linewidth=2)
    ax.set_xlabel('Year')
    ax.set_ylabel('Percentage')
    ax.set_title('Percentage Values by Year', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:.0f}%'))
    ax.legend(title=my_col_chart)
    ax.grid(True)
    st.pyplot(fig)
    
    st.markdown('---') # Add a solid black line to differentiate the third chart
    df_vacancies = df_filtered.pivot_table(values='ΚΕΝΑ',index='Έτος',columns='Διαμέρισμα', aggfunc='sum',fill_value=0)
    fig, ax = plt.subplots(figsize=(10, 6))
    for column in df_vacancies.columns:
        ax.plot(df_vacancies.index, df_vacancies[column], label=column, color=colors.get(column, '#000000'), linewidth=widths.get(column, 1))
    ax.set_xlabel('Year')
    ax.set_ylabel('ΚΕΝΑ')
    ax.set_title('Total Vacancies by Year',bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
    ax.legend(title='Διαμέρισμα')
    ax.grid(True)
    st.pyplot(fig)
    
    st.markdown('---') # Add a solid black line to differentiate the third chart
    selected_percentage = st.slider('**Select a percentage threshold for the next two Charts**', 2, 20, value=5, step=1)
    df_country_percentage = df_filtered.pivot_table(values='Τιμή', index='Έτος', columns='Χώρα', aggfunc='sum', fill_value=0)
    df_country_percentage = df_country_percentage.div(df_country_percentage.sum(axis=1), axis=0) * 100
    df_filtered_percentage = df_country_percentage.loc[:, (df_country_percentage > selected_percentage).any()]
    fig, ax = plt.subplots(figsize=(10, 6))
    df_filtered_percentage.plot(kind='bar', stacked=True, ax=ax)
    ax.set_xlabel('Year')
    ax.set_ylabel('Percentage')
    ax.set_title(f'Countries with Percentage > {selected_percentage}% by Year', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:.0f}%'))
    ax.legend(title='Χώρα')
    ax.grid(True)
    st.pyplot(fig)
    
    st.write("\n" * 5) # add blank lines
    df_total_percentage = df_filtered.pivot_table(values='Τιμή', index='Χώρα', aggfunc='sum', fill_value=0)
    df_total_percentage = df_total_percentage.div(df_total_percentage.sum()) * 100
    df_total_filtered_percentage = df_total_percentage[df_total_percentage['Τιμή'] > selected_percentage]
    fig, ax = plt.subplots(figsize=(14, 8))
    df_total_filtered_percentage.plot(kind='pie', y='Τιμή', ax=ax, autopct='%1.1f%%', legend=False)
    ax.set_ylabel('')
    ax.set_title(f'Total Percentage of Countries with > {selected_percentage}%', fontsize=10, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
    st.pyplot(fig)
    
else:
    st.write("No DataFrame found in session state. Please upload a CSV file on the main page.")       