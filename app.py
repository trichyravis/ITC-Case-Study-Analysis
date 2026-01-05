
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf

st.set_page_config(page_title="ITC Financial Analysis", layout="wide")

# ============================================================================
# FILE UPLOADER
# ============================================================================

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

# ============================================================================
# MAIN APP
# ============================================================================

st.title("ITC Financial Analysis Platform")

if uploaded_file is None:
    st.write("Welcome! Please upload your Excel file in the sidebar to begin.")
else:
    try:
        # First, show available sheets
        st.subheader("Diagnostic: Available Sheets")
        
        excel_file = pd.ExcelFile(uploaded_file)
        sheet_names = excel_file.sheet_names
        
        st.write("**Sheets found in your Excel file:**")
        for i, sheet in enumerate(sheet_names, 1):
            st.write(f"{i}. `{sheet}`")
        
        st.divider()
        st.info("Use the sheet names above in the app configuration")
        
        # Try to load with common sheet names
        df_pl = None
        df_bs = None
        df_cf = None
        
        # Try different possible sheet names
        pl_names = ['P&L', 'P and L', 'PL', 'P/L', 'Profit & Loss', 'Income Statement']
        bs_names = ['Balance Sheet', 'BalanceSheet', 'BS', 'Balance_Sheet']
        cf_names = ['Cash Flow', 'CashFlow', 'CF', 'Cash_Flow']
        
        # Load P&L
        for name in pl_names:
            if name in sheet_names:
                df_pl = pd.read_excel(uploaded_file, sheet_name=name)
                st.success(f"✅ Loaded P&L from sheet: `{name}`")
                break
        
        # Load Balance Sheet
        for name in bs_names:
            if name in sheet_names:
                df_bs = pd.read_excel(uploaded_file, sheet_name=name)
                st.success(f"✅ Loaded Balance Sheet from sheet: `{name}`")
                break
        
        # Load Cash Flow
        for name in cf_names:
            if name in sheet_names:
                df_cf = pd.read_excel(uploaded_file, sheet_name=name)
                st.success(f"✅ Loaded Cash Flow from sheet: `{name}`")
                break
        
        st.divider()
        
        if df_pl is not None:
            st.subheader("P&L Statement Preview")
            st.write(df_pl.head())
            st.write(f"Shape: {df_pl.shape}")
        
        if df_bs is not None:
            st.subheader("Balance Sheet Preview")
            st.write(df_bs.head())
            st.write(f"Shape: {df_bs.shape}")
        
        if df_cf is not None:
            st.subheader("Cash Flow Preview")
            st.write(df_cf.head())
            st.write(f"Shape: {df_cf.shape}")
        
        # ====================================================================
        # TABS
        # ====================================================================
        
        if df_pl is not None:
            st.divider()
            
            tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
                "Dashboard", "Market Data", "Price Forecast", "Volatility", 
                "Value at Risk", "Expected Shortfall", "Financial Ratios", 
                "Scenario Analysis", "Insights", "Help"
            ])
            
            # TAB 1: DASHBOARD
            with tab1:
                st.header("Executive Summary")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Revenue", "₹50,000 Cr", "+5.2%")
                with col2:
                    st.metric("Net Profit", "₹8,000 Cr", "+3.1%")
                with col3:
                    st.metric("ROE", "15.2%", "+0.5%")
                with col4:
                    st.metric("Profit Margin", "16.0%", "-0.2%")
                
                st.divider()
                
                st.subheader("Financial Data Preview")
                st.write(df_pl.head())
            
            # TAB 2: MARKET DATA
            with tab2:
                st.header("Market Data & Technical Analysis")
                
                try:
                    itc_data = yf.download('ITCL.NS', period='5y', progress=False)
                    
                    st.subheader("ITC Stock Price (5 Years)")
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=itc_data.index,
                        y=itc_data['Close'],
                        mode='lines',
                        name='ITC Price',
                        line=dict(color='#003366', width=2)
                    ))
                    fig.update_layout(
                        title="ITC Stock Price History",
                        xaxis_title="Date",
                        yaxis_title="Price (INR)",
                        hovermode='x unified',
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.metric("Current Price", f"₹{itc_data['Close'].iloc[-1]:.2f}")
                except:
                    st.warning("Unable to fetch stock data")
            
            # TAB 3: PRICE FORECAST
            with tab3:
                st.header("Price Forecast (ARIMA Model)")
                st.info("Price forecast visualization would appear here")
            
            # TAB 4: VOLATILITY
            with tab4:
                st.header("Volatility Analysis (GARCH)")
                st.info("Volatility analysis would appear here")
            
            # TAB 5: VALUE AT RISK
            with tab5:
                st.header("Value at Risk (VAR) Analysis")
                st.info("VAR analysis would appear here")
            
            # TAB 6: EXPECTED SHORTFALL
            with tab6:
                st.header("Expected Shortfall (CVaR) Analysis")
                st.info("CVaR analysis would appear here")
            
            # TAB 7: FINANCIAL RATIOS
            with tab7:
                st.header("Financial Ratios Analysis")
                
                st.subheader("Key Financial Metrics")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Profit Margin", "16.0%")
                with col2:
                    st.metric("ROA", "8.5%")
                with col3:
                    st.metric("ROE", "15.2%")
            
            # TAB 8: SCENARIO ANALYSIS
            with tab8:
                st.header("Scenario Analysis")
                
                scenarios = {
                    "Best Case": {"revenue": "+15%", "margin": "+2%"},
                    "Base Case": {"revenue": "+5%", "margin": "+0.5%"},
                    "Worst Case": {"revenue": "-5%", "margin": "-1%"}
                }
                
                for scenario, values in scenarios.items():
                    st.subheader(scenario)
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"Revenue Growth: {values['revenue']}")
                    with col2:
                        st.write(f"Margin Impact: {values['margin']}")
            
            # TAB 9: INSIGHTS
            with tab9:
                st.header("Investment Insights")
                st.write("Analysis and recommendations would appear here")
            
            # TAB 10: HELP
            with tab10:
                st.header("Help & Glossary")
                
                with st.expander("What is ARIMA?"):
                    st.write("ARIMA is a statistical model for time series forecasting.")
                
                with st.expander("What is GARCH?"):
                    st.write("GARCH models time-varying volatility.")
                
                with st.expander("What is VAR?"):
                    st.write("Value at Risk is the maximum expected loss at a given confidence level.")
        else:
            st.error("Could not load any financial data sheets")
            st.info("Please check your Excel file has the correct sheet names")
    
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.info("Please make sure your Excel file is valid and has the required sheets")
