
import streamlit as st
import pandas as pd

st.set_page_config(page_title="ITC Financial Analysis", layout="wide")

st.title("ITC Financial Analysis Platform")

# File Uploader in Sidebar
with st.sidebar:
    st.header("Data Upload")
    
    uploaded_file = st.file_uploader(
        "Upload Excel File (ITC__2_.xlsx)",
        type=['xlsx', 'xls']
    )
    
    if uploaded_file is not None:
        st.success("File uploaded successfully!")
    else:
        st.info("Upload your Excel file to get started")

# Main Content
if uploaded_file is None:
    st.write("Welcome! Please upload your Excel file in the sidebar to begin.")
else:
    try:
        # Load data
        df = pd.read_excel(uploaded_file, sheet_name='P&L')
        st.success("Data loaded successfully!")
        
        # Show preview
        st.write("Data Preview:")
        st.write(df.head())
        
    except Exception as e:
        st.error(f"Error loading file: {e}")
        st.info("Make sure your Excel file has a 'P&L' sheet")
