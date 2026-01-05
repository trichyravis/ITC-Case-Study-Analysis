
import streamlit as st
import pandas as pd

st.set_page_config(page_title="ITC Financial Analysis", layout="wide")

st.title("📊 ITC Financial Analysis")

# File Uploader
with st.sidebar:
    st.header("📁 Data Upload")
    
    uploaded_file = st.file_uploader(
        "Upload Excel File (ITC__2_.xlsx)",
        type=['xlsx', 'xls']
    )
    
    if uploaded_file is not None:
        st.success("✅ File uploaded successfully!")
    else:
        st.info("Upload your Excel file to get started")

st.write("Hello! If you see this, the app is working!")
