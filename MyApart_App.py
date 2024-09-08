# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 12:37:10 2024

@author: dstan
"""

import streamlit as st
import pandas as pd

# Initialize session state for the uploaded file and DataFrame
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'df' not in st.session_state:
    st.session_state.df = None

# create tabs
tab1, tab2, tab3 = st.tabs(["Upload File", "View Data", "Filter Data"])

# Tab1: Upload File
with tab1:
    st.header("Upload CSV File")
    st.session_state.uploaded_file = st.file_uploader('Select a File', 'csv') #Variables stored in st.session_state persist across different interactions with the app
    if st.session_state.uploaded_file is not None:
        st.session_state.df = pd.read_csv(st.session_state.uploaded_file, index_col=False)
        st.success("File uploaded successfully!")

# Tab2: View Data    
# Tab2: View Data    
with tab2:
    st.header("View Data")
    if st.session_state.df is not None:
        My_Views = ['View All', 'View Top5']
        selected_view = st.selectbox('Select View', My_Views)
        if selected_view == 'View All':
            st.subheader('View All')
            st.dataframe(st.session_state.df, hide_index=True)#instead of st.write(st.session_state.df) because i dont want the index
            # st.write(st.session_state.df)
        else:
            st.subheader('View Top5')
            st.dataframe(st.session_state.df.head(),hide_index= True)
            # st.write(st.session_state.df.head())
    else:
            st.warning("Please upload a file in the 'Upload File' tab.")            
# Tab3: Filter Data    
with tab3:  
    st.header("Filter Data")
    if st.session_state.df is not None:
        columns = st.session_state.df.columns.tolist()
        selected_column = st.selectbox('Select Column', columns)
        unique_of_selected_col = st.session_state.df[selected_column].unique()
        selected_value = st.selectbox(f'Select of {selected_column}', unique_of_selected_col)
        selected_df = st.session_state.df[st.session_state.df[selected_column]==selected_value]
        st.dataframe(selected_df, hide_index=True) # instead of st.write(selected_df) because i dont want the index
        # st.write(selected_df)
    else:
        st.warning("Please upload a file in the 'Upload File' tab.")   
