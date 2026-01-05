
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="ITC Financial Analysis", layout="wide")

# ============================================================================
# FILE UPLOADER
# ============================================================================

with st.sidebar:
    st.header("Data Upload")
    
    uploaded_file = st.file_uploader(
        "Upload Excel File from Screener.in",
        type=['xlsx', 'xls']
    )
    
    if uploaded_file is not None:
        st.success("File uploaded successfully!")
    else:
        st.info("Upload your Excel file to get started")

# ============================================================================
# DATA LOADING
# ============================================================================

@st.cache_data
def load_and_parse_screener(file):
    """Load and parse Screener.in Excel format"""
    if file is None:
        return None, None, None
    
    try:
        df = pd.read_excel(file, sheet_name='Data Sheet')
        
        pl_idx = None
        bs_idx = None
        cf_idx = None
        
        for i, row in df.iterrows():
            if row.iloc[0] == 'PROFIT & LOSS':
                pl_idx = i
            elif row.iloc[0] == 'BALANCE SHEET':
                bs_idx = i
            elif row.iloc[0] == 'CASH FLOW:':
                cf_idx = i
        
        # Extract P&L
        pl_annual = None
        if pl_idx is not None:
            date_row = pl_idx + 1
            dates = df.iloc[date_row, 1:11]
            dates = [d for d in dates if pd.notna(d)]
            
            if len(dates) > 0:
                pl_data = {}
                end_idx = bs_idx if bs_idx else len(df)
                
                for row_idx in range(date_row + 1, min(date_row + 20, end_idx)):
                    metric_name = df.iloc[row_idx, 0]
                    if metric_name and pd.notna(metric_name) and metric_name not in ['NaN', 'Quarters']:
                        try:
                            values = df.iloc[row_idx, 1:len(dates)+1].values
                            pl_data[metric_name] = values
                        except:
                            pass
                
                if len(pl_data) > 0:
                    pl_annual = pd.DataFrame(pl_data, index=dates).T
        
        # Extract Balance Sheet
        bs_annual = None
        if bs_idx is not None:
            date_row = bs_idx + 1
            dates = df.iloc[date_row, 1:11]
            dates = [d for d in dates if pd.notna(d)]
            
            if len(dates) > 0:
                bs_data = {}
                end_idx = cf_idx if cf_idx else len(df)
                
                for row_idx in range(date_row + 1, min(date_row + 20, end_idx)):
                    metric_name = df.iloc[row_idx, 0]
                    if metric_name and pd.notna(metric_name):
                        try:
                            values = df.iloc[row_idx, 1:len(dates)+1].values
                            bs_data[metric_name] = values
                        except:
                            pass
                
                if len(bs_data) > 0:
                    bs_annual = pd.DataFrame(bs_data, index=dates).T
        
        # Extract Cash Flow
        cf_annual = None
        if cf_idx is not None:
            date_row = cf_idx + 1
            dates = df.iloc[date_row, 1:11]
            dates = [d for d in dates if pd.notna(d)]
            
            if len(dates) > 0:
                cf_data = {}
                
                for row_idx in range(date_row + 1, min(date_row + 10, len(df))):
                    metric_name = df.iloc[row_idx, 0]
                    if metric_name and pd.notna(metric_name):
                        try:
                            values = df.iloc[row_idx, 1:len(dates)+1].values
                            cf_data[metric_name] = values
                        except:
                            pass
                
                if len(cf_data) > 0:
                    cf_annual = pd.DataFrame(cf_data, index=dates).T
        
        return pl_annual, bs_annual, cf_annual
    except:
        return None, None, None

@st.cache_data
def get_itc_stock_data():
    """Try to fetch ITC stock data"""
    try:
        itc_data = yf.download('ITC.NS', period='5y', progress=False, threads=False)
        if itc_data is not None and len(itc_data) > 50 and 'Close' in itc_data.columns:
            return itc_data
        return None
    except:
        return None

# ============================================================================
# MAIN APP
# ============================================================================

st.title("ITC Financial Analysis Platform")

if uploaded_file is None:
    st.write("Welcome! Please upload your Screener.in Excel file in the sidebar to begin.")
else:
    # Load financial data
    pl_df, bs_df, cf_df = load_and_parse_screener(uploaded_file)
    
    if pl_df is None or len(pl_df) == 0:
        st.error("Could not parse P&L data from Excel file")
        st.stop()
    
    st.success("Financial data loaded successfully!")
    
    # Try to load stock data
    itc_data = get_itc_stock_data()
    has_stock_data = itc_data is not None and len(itc_data) > 0
    
    # ========================================================================
    # TABS
    # ========================================================================
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
        "Dashboard", "Market Data", "Price Forecast", "Volatility", 
        "Value at Risk", "Expected Shortfall", "Financial Ratios", 
        "Scenario Analysis", "Insights", "Help"
    ])
    
    # ========================================================================
    # TAB 1: DASHBOARD
    # ========================================================================
    with tab1:
        st.header("Executive Summary")
        
        try:
            latest_idx = -1
            prev_idx = -2 if len(pl_df) > 1 else -1
            
            # Find columns - check exact names from your data
            sales_col = None
            for col in pl_df.columns:
                col_str = str(col).lower().strip()
                if 'sales' in col_str or 'revenue' in col_str:
                    sales_col = col
                    break
            
            profit_col = None
            for col in pl_df.columns:
                col_str = str(col).lower().strip()
                if 'net profit' in col_str:
                    profit_col = col
                    break
            
            # Get values
            if sales_col:
                sales_latest = float(pl_df[sales_col].iloc[latest_idx])
                sales_prev = float(pl_df[sales_col].iloc[prev_idx])
                sales_growth = ((sales_latest - sales_prev) / sales_prev * 100) if sales_prev != 0 else 0
            else:
                sales_latest = sales_growth = 0
            
            if profit_col:
                profit_latest = float(pl_df[profit_col].iloc[latest_idx])
                profit_prev = float(pl_df[profit_col].iloc[prev_idx])
                profit_growth = ((profit_latest - profit_prev) / profit_prev * 100) if profit_prev != 0 else 0
            else:
                profit_latest = profit_growth = 0
            
            # Display metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Revenue", f"₹{sales_latest:,.0f} Cr", f"{sales_growth:+.1f}%")
            with col2:
                st.metric("Net Profit", f"₹{profit_latest:,.0f} Cr", f"{profit_growth:+.1f}%")
            with col3:
                margin = (profit_latest / sales_latest * 100) if sales_latest != 0 else 0
                st.metric("Profit Margin", f"{margin:.1f}%")
            with col4:
                if bs_df is not None:
                    equity_col = next((col for col in bs_df.columns if 'Equity' in str(col)), None)
                    if equity_col:
                        equity = float(bs_df[equity_col].iloc[latest_idx])
                        roe = (profit_latest / equity * 100) if equity != 0 else 0
                        st.metric("ROE", f"{roe:.1f}%")
            
            st.divider()
            
            # Chart
            if sales_col:
                st.subheader("Annual Revenue Trend")
                fig = go.Figure()
                fig.add_trace(go.Bar(x=pl_df.index, y=pl_df[sales_col], name='Revenue', marker_color='#003366'))
                fig.update_layout(title="Annual Sales", xaxis_title="Year", yaxis_title="Sales (Cr)", height=400)
                st.plotly_chart(fig)
            
            st.subheader("Financial Data")
            st.dataframe(pl_df.tail(5))
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    # ========================================================================
    # TAB 2: MARKET DATA
    # ========================================================================
    with tab2:
        st.header("Market Data & Technical Analysis")
        
        if has_stock_data:
            st.subheader("ITC Stock Price (5 Years)")
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=itc_data.index, y=itc_data['Close'], mode='lines', 
                                    name='ITC Price', line=dict(color='#003366', width=2)))
            fig.update_layout(title="ITC Stock Price", xaxis_title="Date", yaxis_title="Price (INR)", height=400)
            st.plotly_chart(fig)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Current Price", f"₹{float(itc_data['Close'].iloc[-1]):.2f}")
            with col2:
                st.metric("52-Week High", f"₹{float(itc_data['Close'].tail(252).max()):.2f}")
            with col3:
                st.metric("52-Week Low", f"₹{float(itc_data['Close'].tail(252).min()):.2f}")
        else:
            st.warning("Stock price data not available. Please upload financial data from Screener.in.")
    
    # ========================================================================
    # TAB 3: PRICE FORECAST
    # ========================================================================
    with tab3:
        st.header("Price Forecast Analysis")
        
        if has_stock_data and len(itc_data) > 200:
            ma_50 = float(itc_data['Close'].tail(50).mean())
            ma_200 = float(itc_data['Close'].tail(200).mean())
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("50-Day MA", f"₹{ma_50:.2f}")
            with col2:
                st.metric("200-Day MA", f"₹{ma_200:.2f}")
            
            st.write(f"**Trend:** {'Bullish (50-MA > 200-MA)' if ma_50 > ma_200 else 'Bearish (50-MA < 200-MA)'}")
        else:
            st.info("Stock data required for forecasting")
    
    # ========================================================================
    # TAB 4: VOLATILITY
    # ========================================================================
    with tab4:
        st.header("Volatility Analysis")
        
        if has_stock_data and len(itc_data) > 30:
            returns = itc_data['Close'].pct_change().dropna()
            volatility = returns.rolling(30).std() * np.sqrt(252)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=volatility.index, y=volatility.values, mode='lines', 
                                    name='Volatility', line=dict(color='orange')))
            fig.update_layout(title="30-Day Rolling Volatility", xaxis_title="Date", 
                            yaxis_title="Volatility", height=400)
            st.plotly_chart(fig)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Current Vol", f"{float(volatility.iloc[-1])*100:.2f}%")
            with col2:
                st.metric("Avg Vol", f"{float(volatility.mean())*100:.2f}%")
            with col3:
                st.metric("Max Vol", f"{float(volatility.max())*100:.2f}%")
        else:
            st.info("Stock data required for volatility analysis")
    
    # ========================================================================
    # TAB 5: VALUE AT RISK
    # ========================================================================
    with tab5:
        st.header("Value at Risk (VAR)")
        
        if has_stock_data and len(itc_data) > 30:
            returns = itc_data['Close'].pct_change().dropna()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("VAR 90%", f"{float(returns.quantile(0.10))*100:.2f}%")
            with col2:
                st.metric("VAR 95%", f"{float(returns.quantile(0.05))*100:.2f}%")
            with col3:
                st.metric("VAR 99%", f"{float(returns.quantile(0.01))*100:.2f}%")
            
            st.subheader("Return Distribution")
            fig = px.histogram(x=returns, nbins=50, title="Daily Returns Distribution")
            st.plotly_chart(fig)
        else:
            st.info("Stock data required for VAR analysis")
    
    # ========================================================================
    # TAB 6: EXPECTED SHORTFALL
    # ========================================================================
    with tab6:
        st.header("Expected Shortfall (CVaR)")
        
        if has_stock_data and len(itc_data) > 30:
            returns = itc_data['Close'].pct_change().dropna()
            var_95 = float(returns.quantile(0.05))
            cvar_95 = float(returns[returns <= var_95].mean())
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("VAR 95%", f"{var_95*100:.2f}%")
            with col2:
                st.metric("CVaR 95%", f"{cvar_95*100:.2f}%")
        else:
            st.info("Stock data required for CVaR analysis")
    
    # ========================================================================
    # TAB 7: FINANCIAL RATIOS
    # ========================================================================
    with tab7:
        st.header("Financial Ratios Analysis")
        
        try:
            latest_idx = -1
            
            sales_col = None
            for col in pl_df.columns:
                if 'Sales' in str(col) or 'Revenue' in str(col):
                    sales_col = col
                    break
            
            profit_col = None
            for col in pl_df.columns:
                if 'Net profit' in str(col) or 'Net Profit' in str(col):
                    profit_col = col
                    break
            
            if sales_col and profit_col:
                sales = float(pl_df[sales_col].iloc[latest_idx])
                profit = float(pl_df[profit_col].iloc[latest_idx])
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    margin = (profit / sales * 100) if sales != 0 else 0
                    st.metric("Profit Margin", f"{margin:.2f}%")
                with col2:
                    st.metric("Sales (Cr)", f"₹{sales:,.0f}")
                with col3:
                    if bs_df is not None:
                        equity_col = next((col for col in bs_df.columns if 'Equity' in str(col)), None)
                        if equity_col:
                            equity = float(bs_df[equity_col].iloc[latest_idx])
                            roe = (profit / equity * 100) if equity != 0 else 0
                            st.metric("ROE", f"{roe:.2f}%")
        except:
            st.info("Calculating ratios...")
    
    # ========================================================================
    # TAB 8: SCENARIO ANALYSIS
    # ========================================================================
    with tab8:
        st.header("Scenario Analysis")
        
        try:
            sales_col = None
            for col in pl_df.columns:
                if 'Sales' in str(col) or 'Revenue' in str(col):
                    sales_col = col
                    break
            
            if sales_col:
                base_sales = float(pl_df[sales_col].iloc[-1])
                
                scenarios = {"Best Case (+15%)": 0.15, "Base Case (+5%)": 0.05, "Worst Case (-5%)": -0.05}
                
                for scenario, growth in scenarios.items():
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric(scenario, f"₹{base_sales * (1 + growth):,.0f} Cr")
                    with col2:
                        st.metric("Growth Rate", f"{growth*100:+.0f}%")
                    st.divider()
        except:
            st.info("Scenario analysis...")
    
    # ========================================================================
    # TAB 9: INSIGHTS
    # ========================================================================
    with tab9:
        st.header("Investment Insights")
        
        st.write("""
        ### Financial Performance Summary
        
        Based on comprehensive analysis of ITC Ltd's financials from your Excel file.
        
        **Key Metrics:** Revenue, Profitability, ROE, Financial Health
        
        Review all tabs for detailed analysis.
        """)
    
    # ========================================================================
    # TAB 10: HELP
    # ========================================================================
    with tab10:
        st.header("Help & Glossary")
        
        with st.expander("About Financial Ratios"):
            st.write("Metrics for analyzing financial performance and health")
        
        with st.expander("About VAR & CVaR"):
            st.write("Risk metrics for measuring potential losses")
        
        with st.expander("About Volatility"):
            st.write("Measure of price fluctuations and market risk")
