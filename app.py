
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

@st.cache_data(ttl=3600)
def get_itc_stock_data():
    """Fetch ITC stock data with retry logic and rate limit handling"""
    import time
    
    tickers_to_try = ['ITC.NS', 'ITC.BO']
    
    for ticker in tickers_to_try:
        try:
            # Suppress yfinance warnings
            import warnings
            warnings.filterwarnings('ignore')
            
            itc_data = yf.download(
                ticker, 
                period='5y', 
                progress=False,
                threads=False,
                timeout=30
            )
            
            if itc_data is not None and len(itc_data) > 100:
                if 'Close' in itc_data.columns:
                    return itc_data
        except Exception as e:
            continue
        
        # Small delay between attempts to avoid rate limiting
        time.sleep(1)
    
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
            
            # Find metric rows (search in INDEX, not columns!)
            sales_row = None
            for idx in pl_df.index:
                idx_str = str(idx).lower().strip()
                if 'sales' in idx_str or 'revenue' in idx_str:
                    sales_row = idx
                    break
            
            profit_row = None
            for idx in pl_df.index:
                idx_str = str(idx).lower().strip()
                if 'net profit' in idx_str:
                    profit_row = idx
                    break
            
            # Get values from latest and previous columns
            if sales_row is not None:
                sales_latest = float(pl_df.loc[sales_row].iloc[latest_idx])
                sales_prev = float(pl_df.loc[sales_row].iloc[prev_idx])
                sales_growth = ((sales_latest - sales_prev) / sales_prev * 100) if sales_prev != 0 else 0
            else:
                sales_latest = sales_growth = 0
            
            if profit_row is not None:
                profit_latest = float(pl_df.loc[profit_row].iloc[latest_idx])
                profit_prev = float(pl_df.loc[profit_row].iloc[prev_idx])
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
                if bs_df is not None and profit_row is not None:
                    equity_row = None
                    for idx in bs_df.index:
                        if 'Equity' in str(idx):
                            equity_row = idx
                            break
                    
                    if equity_row is not None:
                        equity = float(bs_df.loc[equity_row].iloc[latest_idx])
                        roe = (profit_latest / equity * 100) if equity != 0 else 0
                        st.metric("ROE", f"{roe:.1f}%")
            
            st.divider()
            
            # Chart
            if sales_row is not None:
                st.subheader("Annual Revenue Trend")
                
                # Create clean dataframe for chart
                revenue_df = pd.DataFrame({
                    'Year': pl_df.columns.astype(str),
                    'Sales': pl_df.loc[sales_row].values
                })
                
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=revenue_df['Year'], 
                    y=revenue_df['Sales'], 
                    name='Revenue', 
                    marker_color='#003366'
                ))
                fig.update_layout(
                    title="Annual Sales", 
                    xaxis_title="Year", 
                    yaxis_title="Sales (Cr)", 
                    height=400,
                    template='plotly_white',
                    hovermode='x unified'
                )
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
            
            try:
                # Create a clean dataframe for plotting
                plot_df = pd.DataFrame({
                    'Date': pd.to_datetime(itc_data.index),
                    'Close': itc_data['Close'].values
                })
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=plot_df['Date'].astype(str), 
                    y=plot_df['Close'], 
                    mode='lines', 
                    name='ITC Price',
                    line=dict(color='#003366', width=2),
                    fill='tozeroy',
                    fillcolor='rgba(0, 51, 102, 0.1)'
                ))
                fig.update_layout(
                    title="ITC Stock Price History",
                    xaxis_title="Date",
                    yaxis_title="Price (INR)",
                    height=400,
                    template='plotly_white',
                    hovermode='x unified',
                    xaxis={'type': 'date'}
                )
                st.plotly_chart(fig)
                
                # Metrics
                current_price = float(itc_data['Close'].iloc[-1])
                high_52w = float(itc_data['Close'].tail(252).max())
                low_52w = float(itc_data['Close'].tail(252).min())
                avg_price = float(itc_data['Close'].tail(252).mean())
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Current Price", f"₹{current_price:.2f}")
                with col2:
                    st.metric("52-Week High", f"₹{high_52w:.2f}")
                with col3:
                    st.metric("52-Week Low", f"₹{low_52w:.2f}")
                with col4:
                    st.metric("52-Wk Avg", f"₹{avg_price:.2f}")
                
                # Additional metrics
                st.divider()
                col1, col2, col3 = st.columns(3)
                with col1:
                    price_change = current_price - float(itc_data['Close'].iloc[-252]) if len(itc_data) > 252 else 0
                    pct_change = (price_change / float(itc_data['Close'].iloc[-252]) * 100) if len(itc_data) > 252 else 0
                    st.metric("52-Week Change", f"₹{price_change:.2f}", f"{pct_change:+.2f}%")
                with col2:
                    today_change = current_price - float(itc_data['Close'].iloc[-2]) if len(itc_data) > 1 else 0
                    st.metric("Day Change", f"₹{today_change:.2f}")
                with col3:
                    volume_avg = float(itc_data['Volume'].tail(20).mean()) if 'Volume' in itc_data.columns else 0
                    st.metric("Avg Volume (20d)", f"{volume_avg:,.0f}")
            
            except Exception as e:
                st.error(f"Error displaying market data: {str(e)}")
        else:
            st.warning("📊 Stock price data not available from Yahoo Finance at this moment.")
            st.info("The app works perfectly with your financial data. Stock data will be available when Yahoo Finance is accessible.")
    
    # ========================================================================
    # TAB 3: PRICE FORECAST
    # ========================================================================
    with tab3:
        st.header("Price Forecast & Technical Analysis")
        
        if has_stock_data and len(itc_data) > 200:
            try:
                ma_20 = float(itc_data['Close'].tail(20).mean())
                ma_50 = float(itc_data['Close'].tail(50).mean())
                ma_200 = float(itc_data['Close'].tail(200).mean())
                current_price = float(itc_data['Close'].iloc[-1])
                
                # Metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("20-Day MA", f"₹{ma_20:.2f}")
                with col2:
                    st.metric("50-Day MA", f"₹{ma_50:.2f}")
                with col3:
                    st.metric("200-Day MA", f"₹{ma_200:.2f}")
                with col4:
                    st.metric("Current Price", f"₹{current_price:.2f}")
                
                st.divider()
                
                # Technical analysis
                st.subheader("Technical Signals")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    trend = "📈 Bullish" if ma_50 > ma_200 else "📉 Bearish"
                    st.write(f"**Golden Cross:** {trend} (50-MA vs 200-MA)")
                
                with col2:
                    price_trend = "📈 Above MA20" if current_price > ma_20 else "📉 Below MA20"
                    st.write(f"**Price Position:** {price_trend}")
                
                with col3:
                    ma_trend = "📈 Bullish" if ma_20 > ma_50 > ma_200 else "📉 Mixed/Bearish"
                    st.write(f"**MA Alignment:** {ma_trend}")
                
                # Moving averages chart
                st.subheader("Moving Averages Chart")
                
                # Create clean dataframe for plotting
                plot_df = pd.DataFrame({
                    'Date': pd.to_datetime(itc_data.index),
                    'Price': itc_data['Close'].values,
                    'MA20': itc_data['Close'].rolling(20).mean().values,
                    'MA50': itc_data['Close'].rolling(50).mean().values,
                    'MA200': itc_data['Close'].rolling(200).mean().values
                })
                
                # Convert dates to string for plotting
                plot_df['Date_str'] = plot_df['Date'].astype(str)
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=plot_df['Date_str'], 
                    y=plot_df['Price'], 
                    name='Price', 
                    line=dict(color='black', width=1.5)
                ))
                fig.add_trace(go.Scatter(
                    x=plot_df['Date_str'], 
                    y=plot_df['MA20'],
                    name='20-Day MA', 
                    line=dict(color='orange', width=2)
                ))
                fig.add_trace(go.Scatter(
                    x=plot_df['Date_str'], 
                    y=plot_df['MA50'],
                    name='50-Day MA', 
                    line=dict(color='blue', width=2)
                ))
                fig.add_trace(go.Scatter(
                    x=plot_df['Date_str'], 
                    y=plot_df['MA200'],
                    name='200-Day MA', 
                    line=dict(color='red', width=2)
                ))
                fig.update_layout(
                    title="Price with Moving Averages", 
                    xaxis_title="Date", 
                    yaxis_title="Price (INR)", 
                    height=400,
                    template='plotly_white',
                    hovermode='x unified'
                )
                st.plotly_chart(fig)
            
            except Exception as e:
                st.error(f"Error in forecast: {str(e)}")
        else:
            st.info("📊 Stock data required for technical analysis")
    
    # ========================================================================
    # TAB 4: VOLATILITY
    # ========================================================================
    with tab4:
        st.header("Volatility Analysis (Risk Measurement)")
        
        if has_stock_data and len(itc_data) > 30:
            try:
                returns = itc_data['Close'].pct_change().dropna()
                volatility_30d = returns.rolling(30).std() * np.sqrt(252)
                volatility_60d = returns.rolling(60).std() * np.sqrt(252)
                volatility_all = returns.std() * np.sqrt(252)
                
                # Key metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    current_vol = float(volatility_30d.iloc[-1])*100
                    st.metric("Current Vol (30d)", f"{current_vol:.2f}%")
                with col2:
                    avg_vol = float(volatility_30d.mean())*100
                    st.metric("Avg Vol (30d)", f"{avg_vol:.2f}%")
                with col3:
                    max_vol = float(volatility_30d.max())*100
                    st.metric("Peak Vol (30d)", f"{max_vol:.2f}%")
                with col4:
                    annual_vol = float(volatility_all)*100
                    st.metric("Annual Vol", f"{annual_vol:.2f}%")
                
                st.divider()
                
                # Volatility chart
                st.subheader("Rolling 30-Day Volatility Trend")
                
                # Create clean dataframe for volatility plotting
                vol_df = pd.DataFrame({
                    'Date': pd.to_datetime(volatility_30d.index),
                    'Volatility': volatility_30d.values * 100
                })
                
                # Convert dates to string for plotting
                vol_df['Date_str'] = vol_df['Date'].astype(str)
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=vol_df['Date_str'], 
                    y=vol_df['Volatility'], 
                    mode='lines',
                    name='30-Day Volatility',
                    line=dict(color='#FF6B6B', width=2),
                    fill='tozeroy',
                    fillcolor='rgba(255, 107, 107, 0.2)'
                ))
                fig.add_hline(y=avg_vol, line_dash="dash", line_color="blue", 
                             annotation_text=f"Average: {avg_vol:.2f}%")
                fig.update_layout(
                    title="Volatility Over Time (Annualized %)",
                    xaxis_title="Date",
                    yaxis_title="Volatility (%)",
                    height=400,
                    template='plotly_white',
                    hovermode='x unified'
                )
                st.plotly_chart(fig)
                
                # Volatility distribution
                st.subheader("Volatility Distribution")
                vol_clean = volatility_30d[volatility_30d.notna()].values * 100
                fig = px.histogram(
                    vol_clean,
                    nbins=40,
                    title="Distribution of 30-Day Volatility",
                    labels={'value': 'Volatility (%)', 'count': 'Frequency'},
                    color_discrete_sequence=['#003366']
                )
                st.plotly_chart(fig)
            
            except Exception as e:
                st.error(f"Error in volatility analysis: {str(e)}")
        else:
            st.info("📊 Stock data required for volatility analysis")
    
    # ========================================================================
    # TAB 5: VALUE AT RISK
    # ========================================================================
    with tab5:
        st.header("Value at Risk (VAR) Analysis")
        
        if has_stock_data and len(itc_data) > 30:
            try:
                returns = itc_data['Close'].pct_change().dropna()
                
                var_90 = float(returns.quantile(0.10))
                var_95 = float(returns.quantile(0.05))
                var_99 = float(returns.quantile(0.01))
                
                st.subheader("Daily Loss at Risk (Worst Case Scenario)")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("VAR (90%)", f"{var_90*100:.3f}%", 
                             help="90% chance loss won't exceed this")
                with col2:
                    st.metric("VAR (95%)", f"{var_95*100:.3f}%",
                             help="95% chance loss won't exceed this")
                with col3:
                    st.metric("VAR (99%)", f"{var_99*100:.3f}%",
                             help="99% chance loss won't exceed this")
                
                st.info(f"💡 **Interpretation:** There is a 95% probability that daily losses won't exceed {abs(var_95*100):.2f}%")
                
                st.divider()
                
                # Return distribution
                st.subheader("Daily Returns Distribution")
                returns_pct = returns.values * 100
                fig = px.histogram(
                    returns_pct, 
                    nbins=50,
                    title="Distribution of Daily Returns (%)",
                    labels={'value': 'Daily Return (%)', 'count': 'Frequency'},
                    color_discrete_sequence=['#003366']
                )
                fig.add_vline(x=var_95*100, line_dash="dash", line_color="red", 
                             annotation_text=f"95% VAR: {var_95*100:.2f}%")
                st.plotly_chart(fig)
                
                # Statistics
                st.subheader("Return Statistics")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    mean_ret = float(returns.mean())*100
                    st.metric("Mean Return", f"{mean_ret:.3f}%")
                with col2:
                    std_ret = float(returns.std())*100
                    st.metric("Std Dev", f"{std_ret:.3f}%")
                with col3:
                    skew_ret = float(returns.skew())
                    st.metric("Skewness", f"{skew_ret:.3f}")
                with col4:
                    kurt_ret = float(returns.kurtosis())
                    st.metric("Kurtosis", f"{kurt_ret:.3f}")
            
            except Exception as e:
                st.error(f"Error in VAR analysis: {str(e)}")
        else:
            st.info("📊 Stock data required for VAR analysis")
    
    # ========================================================================
    # TAB 6: EXPECTED SHORTFALL
    # ========================================================================
    with tab6:
        st.header("Expected Shortfall (CVaR) - Tail Risk Analysis")
        
        if has_stock_data and len(itc_data) > 30:
            try:
                returns = itc_data['Close'].pct_change().dropna()
                
                var_90 = float(returns.quantile(0.10))
                var_95 = float(returns.quantile(0.05))
                var_99 = float(returns.quantile(0.01))
                
                cvar_90 = float(returns[returns <= var_90].mean())
                cvar_95 = float(returns[returns <= var_95].mean())
                cvar_99 = float(returns[returns <= var_99].mean())
                
                st.subheader("Average Loss Beyond VAR (Tail Risk)")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("CVaR (90%)", f"{cvar_90*100:.3f}%",
                             help="Average loss when exceeding 90% VAR")
                with col2:
                    st.metric("CVaR (95%)", f"{cvar_95*100:.3f}%",
                             help="Average loss when exceeding 95% VAR")
                with col3:
                    st.metric("CVaR (99%)", f"{cvar_99*100:.3f}%",
                             help="Average loss when exceeding 99% VAR")
                
                st.info(f"💡 **Interpretation:** If the 95% VAR is breached, the average loss will be {abs(cvar_95*100):.2f}%")
                
                st.divider()
                
                # Comparison table
                st.subheader("VAR vs CVaR Comparison")
                comparison_data = {
                    'Confidence Level': ['90%', '95%', '99%'],
                    'VAR (%)': [f"{var_90*100:.3f}", f"{var_95*100:.3f}", f"{var_99*100:.3f}"],
                    'CVaR (%)': [f"{cvar_90*100:.3f}", f"{cvar_95*100:.3f}", f"{cvar_99*100:.3f}"],
                    'Difference': [f"{(cvar_90-var_90)*100:.3f}", 
                                  f"{(cvar_95-var_95)*100:.3f}",
                                  f"{(cvar_99-var_99)*100:.3f}"]
                }
                st.dataframe(pd.DataFrame(comparison_data), use_container_width=True)
                
                # Tail risk visualization
                st.subheader("Tail Risk Visualization")
                tail_returns = returns[returns <= var_95].dropna()
                tail_returns_pct = tail_returns.values * 100
                fig = px.histogram(
                    tail_returns_pct,
                    nbins=30,
                    title="Distribution of Returns Exceeding 95% VAR (Tail Risk)",
                    labels={'value': 'Daily Return (%)', 'count': 'Frequency'},
                    color_discrete_sequence=['#FF6B6B']
                )
                fig.add_vline(x=cvar_95*100, line_dash="dash", line_color="darkred",
                             annotation_text=f"Average: {cvar_95*100:.2f}%")
                st.plotly_chart(fig)
            
            except Exception as e:
                st.error(f"Error in CVaR analysis: {str(e)}")
        else:
            st.info("📊 Stock data required for CVaR analysis")
    
    # ========================================================================
    # TAB 7: FINANCIAL RATIOS
    # ========================================================================
    with tab7:
        st.header("Financial Ratios Analysis")
        
        try:
            latest_idx = -1
            
            # Find metric rows (search in INDEX)
            sales_row = None
            for idx in pl_df.index:
                if 'Sales' in str(idx) or 'Revenue' in str(idx):
                    sales_row = idx
                    break
            
            profit_row = None
            for idx in pl_df.index:
                if 'Net profit' in str(idx) or 'net profit' in str(idx):
                    profit_row = idx
                    break
            
            if sales_row is not None and profit_row is not None:
                sales = float(pl_df.loc[sales_row].iloc[latest_idx])
                profit = float(pl_df.loc[profit_row].iloc[latest_idx])
                
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
            # Find Sales row in index
            sales_row = None
            for idx in pl_df.index:
                if 'Sales' in str(idx) or 'Revenue' in str(idx):
                    sales_row = idx
                    break
            
            if sales_row is not None:
                base_sales = float(pl_df.loc[sales_row].iloc[-1])
                
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
