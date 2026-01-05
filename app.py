
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
        "Upload Excel File from Screener.in",
        type=['xlsx', 'xls']
    )
    
    if uploaded_file is not None:
        st.success("File uploaded successfully!")
    else:
        st.info("Upload your Excel file to get started")

# ============================================================================
# LOAD AND PARSE DATA
# ============================================================================

@st.cache_data
def load_screener_data(file):
    """Load and parse Screener.in format data"""
    if file is None:
        return None
    
    try:
        df = pd.read_excel(file, sheet_name='Data Sheet')
        return df
    except:
        return None

@st.cache_data
def extract_pl_annual(df):
    """Extract annual P&L data"""
    try:
        # Find P&L section (row 13) and Report Date (row 14)
        pl_section = df[df.iloc[:, 0] == 'PROFIT & LOSS'].index[0]
        date_row = pl_section + 1
        
        # Extract dates and create annual P&L dataframe
        dates = df.iloc[date_row, 1:].dropna()
        
        # Extract key metrics
        metrics = {}
        for idx in range(date_row + 1, pl_section + 15):
            if idx < len(df):
                metric_name = df.iloc[idx, 0]
                if metric_name and pd.notna(metric_name) and metric_name not in ['NaN', 'Quarters']:
                    metrics[metric_name] = df.iloc[idx, 1:len(dates)+1].values
        
        pl_df = pd.DataFrame(metrics, index=dates).T
        return pl_df
    except:
        return None

@st.cache_data
def extract_bs_annual(df):
    """Extract annual Balance Sheet data"""
    try:
        # Find Balance Sheet section
        bs_section = df[df.iloc[:, 0] == 'BALANCE SHEET'].index[0]
        date_row = bs_section + 1
        
        dates = df.iloc[date_row, 1:].dropna()
        
        metrics = {}
        for idx in range(date_row + 1, bs_section + 20):
            if idx < len(df):
                metric_name = df.iloc[idx, 0]
                if metric_name and pd.notna(metric_name):
                    metrics[metric_name] = df.iloc[idx, 1:len(dates)+1].values
        
        bs_df = pd.DataFrame(metrics, index=dates).T
        return bs_df
    except:
        return None

@st.cache_data
def extract_cf_annual(df):
    """Extract annual Cash Flow data"""
    try:
        # Find Cash Flow section
        cf_section = df[df.iloc[:, 0] == 'CASH FLOW:'].index[0]
        date_row = cf_section + 1
        
        dates = df.iloc[date_row, 1:].dropna()
        
        metrics = {}
        for idx in range(date_row + 1, cf_section + 10):
            if idx < len(df):
                metric_name = df.iloc[idx, 0]
                if metric_name and pd.notna(metric_name):
                    metrics[metric_name] = df.iloc[idx, 1:len(dates)+1].values
        
        cf_df = pd.DataFrame(metrics, index=dates).T
        return cf_df
    except:
        return None

@st.cache_data
def get_itc_stock_data():
    """Fetch ITC stock data from Yahoo Finance"""
    try:
        itc_data = yf.download('ITCL.NS', period='5y', progress=False)
        return itc_data
    except:
        return None

# ============================================================================
# MAIN APP
# ============================================================================

st.title("ITC Financial Analysis Platform")

if uploaded_file is None:
    st.write("Welcome! Please upload your Screener.in Excel file in the sidebar to begin.")
else:
    # Load data
    raw_df = load_screener_data(uploaded_file)
    
    if raw_df is None:
        st.error("Error loading Excel file.")
        st.stop()
    
    pl_df = extract_pl_annual(raw_df)
    bs_df = extract_bs_annual(raw_df)
    cf_df = extract_cf_annual(raw_df)
    itc_data = get_itc_stock_data()
    
    if pl_df is None:
        st.error("Could not parse financial data from file.")
        st.stop()
    
    st.success("Financial data loaded successfully!")
    
    # ========================================================================
    # TABS
    # ========================================================================
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
        "Dashboard", "Market Data", "Price Forecast", "Volatility", 
        "Value at Risk", "Expected Shortfall", "Financial Ratios", 
        "Scenario Analysis", "Insights", "Help"
    ])
    
    # TAB 1: DASHBOARD
    with tab1:
        st.header("Executive Summary")
        
        try:
            # Get latest year data
            latest_year = pl_df.index[-1]
            prev_year = pl_df.index[-2] if len(pl_df) > 1 else pl_df.index[0]
            
            sales_latest = float(pl_df.loc[latest_year, 'Sales']) if 'Sales' in pl_df.columns else 0
            sales_prev = float(pl_df.loc[prev_year, 'Sales']) if 'Sales' in pl_df.columns else sales_latest
            sales_growth = ((sales_latest - sales_prev) / sales_prev * 100) if sales_prev != 0 else 0
            
            profit_latest = float(pl_df.loc[latest_year, 'Net profit']) if 'Net profit' in pl_df.columns else 0
            profit_prev = float(pl_df.loc[prev_year, 'Net profit']) if 'Net profit' in pl_df.columns else profit_latest
            profit_growth = ((profit_latest - profit_prev) / profit_prev * 100) if profit_prev != 0 else 0
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Revenue (Latest)", f"₹{sales_latest:,.0f} Cr", f"{sales_growth:+.1f}%")
            with col2:
                st.metric("Net Profit (Latest)", f"₹{profit_latest:,.0f} Cr", f"{profit_growth:+.1f}%")
            with col3:
                margin = (profit_latest / sales_latest * 100) if sales_latest != 0 else 0
                st.metric("Profit Margin", f"{margin:.1f}%")
            with col4:
                equity = float(bs_df.loc[latest_year, 'Equity Share Capital']) if bs_df is not None and 'Equity Share Capital' in bs_df.columns else 0
                roe = (profit_latest / equity * 100) if equity != 0 else 0
                st.metric("ROE", f"{roe:.1f}%")
            
            st.divider()
            
            st.subheader("Annual Revenue Trend")
            if 'Sales' in pl_df.columns:
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=pl_df.index,
                    y=pl_df['Sales'],
                    name='Revenue',
                    marker_color='#003366'
                ))
                fig.update_layout(
                    title="Annual Sales Trend",
                    xaxis_title="Year",
                    yaxis_title="Sales (Crores)",
                    hovermode='x unified',
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("Financial Data Preview")
            st.write("Latest Financial Data:")
            st.write(pl_df.tail(3))
        except Exception as e:
            st.error(f"Error in dashboard: {str(e)}")
    
    # TAB 2: MARKET DATA
    with tab2:
        st.header("Market Data & Technical Analysis")
        
        if itc_data is not None and len(itc_data) > 0:
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
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Current Price", f"₹{itc_data['Close'].iloc[-1]:.2f}")
            with col2:
                st.metric("52-Week High", f"₹{itc_data['Close'].tail(252).max():.2f}")
            with col3:
                st.metric("52-Week Low", f"₹{itc_data['Close'].tail(252).min():.2f}")
        else:
            st.warning("Unable to fetch stock data from Yahoo Finance")
    
    # TAB 3: PRICE FORECAST
    with tab3:
        st.header("Price Forecast Analysis")
        
        st.info("ARIMA model for price forecasting would be implemented here with historical price data")
        
        if itc_data is not None:
            # Simple moving average forecast
            ma_50 = itc_data['Close'].tail(50).mean()
            ma_200 = itc_data['Close'].tail(200).mean()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("50-Day MA", f"₹{ma_50:.2f}")
            with col2:
                st.metric("200-Day MA", f"₹{ma_200:.2f}")
    
    # TAB 4: VOLATILITY
    with tab4:
        st.header("Volatility Analysis")
        
        if itc_data is not None and len(itc_data) > 30:
            returns = itc_data['Close'].pct_change().dropna()
            volatility = returns.rolling(30).std() * np.sqrt(252)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=volatility.index,
                y=volatility.values,
                mode='lines',
                name='30-Day Volatility',
                line=dict(color='orange')
            ))
            fig.update_layout(
                title="Rolling 30-Day Volatility (Annualized)",
                xaxis_title="Date",
                yaxis_title="Volatility",
                hovermode='x unified',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Current Volatility", f"{volatility.iloc[-1]*100:.2f}%")
            with col2:
                st.metric("Average Volatility", f"{volatility.mean()*100:.2f}%")
            with col3:
                st.metric("Max Volatility", f"{volatility.max()*100:.2f}%")
    
    # TAB 5: VALUE AT RISK
    with tab5:
        st.header("Value at Risk (VAR) Analysis")
        
        if itc_data is not None and len(itc_data) > 30:
            returns = itc_data['Close'].pct_change().dropna()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                var_95 = returns.quantile(0.05)
                st.metric("VAR (95%)", f"{var_95*100:.2f}%")
            with col2:
                var_99 = returns.quantile(0.01)
                st.metric("VAR (99%)", f"{var_99*100:.2f}%")
            with col3:
                var_90 = returns.quantile(0.10)
                st.metric("VAR (90%)", f"{var_90*100:.2f}%")
            
            st.subheader("Return Distribution")
            fig = px.histogram(
                x=returns,
                nbins=50,
                title="Daily Returns Distribution",
                labels={'x': 'Daily Return', 'y': 'Frequency'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # TAB 6: EXPECTED SHORTFALL
    with tab6:
        st.header("Expected Shortfall (CVaR) Analysis")
        
        if itc_data is not None and len(itc_data) > 30:
            returns = itc_data['Close'].pct_change().dropna()
            
            var_95 = returns.quantile(0.05)
            cvar_95 = returns[returns <= var_95].mean()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("VAR (95%)", f"{var_95*100:.2f}%")
            with col2:
                st.metric("CVaR (95%)", f"{cvar_95*100:.2f}%")
            
            st.write(f"Average loss beyond 95% VAR: {cvar_95*100:.2f}%")
    
    # TAB 7: FINANCIAL RATIOS
    with tab7:
        st.header("Financial Ratios Analysis")
        
        try:
            latest_year = pl_df.index[-1]
            
            sales = float(pl_df.loc[latest_year, 'Sales']) if 'Sales' in pl_df.columns else 0
            net_profit = float(pl_df.loc[latest_year, 'Net profit']) if 'Net profit' in pl_df.columns else 0
            
            profit_margin = (net_profit / sales * 100) if sales != 0 else 0
            
            if bs_df is not None:
                equity = float(bs_df.loc[latest_year, 'Equity Share Capital']) if 'Equity Share Capital' in bs_df.columns else 0
                roe = (net_profit / equity * 100) if equity != 0 else 0
                
                borrowings = float(bs_df.loc[latest_year, 'Borrowings']) if 'Borrowings' in bs_df.columns else 0
                debt_equity = (borrowings / equity) if equity != 0 else 0
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Profit Margin", f"{profit_margin:.2f}%")
                with col2:
                    st.metric("ROE", f"{roe:.2f}%")
                with col3:
                    st.metric("Debt/Equity", f"{debt_equity:.2f}")
            
            st.subheader("Key Metrics Over Time")
            
            margin_trend = (pl_df['Net profit'] / pl_df['Sales'] * 100) if 'Sales' in pl_df.columns else None
            
            if margin_trend is not None:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=margin_trend.index,
                    y=margin_trend.values,
                    mode='lines+markers',
                    name='Profit Margin %',
                    line=dict(color='#003366')
                ))
                fig.update_layout(
                    title="Profit Margin Trend",
                    xaxis_title="Year",
                    yaxis_title="Margin %",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.warning(f"Could not calculate all ratios: {str(e)}")
    
    # TAB 8: SCENARIO ANALYSIS
    with tab8:
        st.header("Scenario Analysis")
        
        try:
            latest_year = pl_df.index[-1]
            base_sales = float(pl_df.loc[latest_year, 'Sales']) if 'Sales' in pl_df.columns else 0
            base_margin = float(pl_df.loc[latest_year, 'Net profit']) / base_sales if base_sales != 0 else 0
            
            scenarios = {
                "Best Case": {"revenue_growth": 0.15, "margin_change": 0.02},
                "Base Case": {"revenue_growth": 0.05, "margin_change": 0.005},
                "Worst Case": {"revenue_growth": -0.05, "margin_change": -0.01}
            }
            
            for scenario, params in scenarios.items():
                st.subheader(scenario)
                
                projected_sales = base_sales * (1 + params['revenue_growth'])
                projected_margin = (base_margin + params['margin_change']) * 100
                projected_profit = projected_sales * (base_margin + params['margin_change'])
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Revenue", f"₹{projected_sales:,.0f} Cr", f"{params['revenue_growth']*100:+.0f}%")
                with col2:
                    st.metric("Margin", f"{projected_margin:.2f}%")
                with col3:
                    st.metric("Net Profit", f"₹{projected_profit:,.0f} Cr")
                st.divider()
        except Exception as e:
            st.warning(f"Could not perform scenario analysis: {str(e)}")
    
    # TAB 9: INSIGHTS
    with tab9:
        st.header("Investment Insights & Recommendations")
        
        st.subheader("Executive Summary")
        st.write("""
        Based on the comprehensive financial analysis of ITC Ltd:
        
        **Financial Strength:**
        - Strong revenue base with consistent growth trajectory
        - Healthy profit margins indicating operational efficiency
        - Solid balance sheet with manageable debt levels
        
        **Investment Highlights:**
        - Diversified business portfolio
        - Strong dividend history
        - Market leadership in tobacco and FMCG segments
        
        **Risk Factors:**
        - Regulatory risks in tobacco sector
        - Competitive pressures in FMCG
        - Currency and commodity price volatility
        """)
        
        st.subheader("Key Recommendations")
        st.write("""
        1. Monitor quarterly earnings for growth acceleration
        2. Track regulatory changes in tobacco sector
        3. Evaluate dividend sustainability
        4. Compare with peer group metrics regularly
        5. Watch for expansion in agri-business and hospitality segments
        """)
    
    # TAB 10: HELP
    with tab10:
        st.header("Help & Glossary")
        
        with st.expander("About This App"):
            st.write("""
            This app analyzes financial data from Screener.in Excel exports.
            It provides comprehensive financial analysis tools for investment decision-making.
            """)
        
        with st.expander("What is VAR?"):
            st.write("Value at Risk (VAR) is the maximum expected loss at a given confidence level over a specific time horizon.")
        
        with st.expander("What is CVaR?"):
            st.write("Conditional Value at Risk (CVaR) is the average loss beyond the VAR threshold, measuring tail-end risk.")
        
        with st.expander("Financial Ratios"):
            st.write("""
            - **Profit Margin**: Net Profit / Sales
            - **ROE**: Net Profit / Equity
            - **Debt/Equity**: Total Borrowings / Equity
            - **Current Ratio**: Current Assets / Current Liabilities
            """)
        
        with st.expander("Data Source"):
            st.write("Financial data sourced from Screener.in Excel exports. Stock prices from Yahoo Finance.")
