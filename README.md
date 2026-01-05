# 📊 ITC Ltd - Financial Analysis & Risk Forecasting Platform

## Professional Streamlit Web Application

A comprehensive financial analysis platform for ITC Limited featuring:
- **ARIMA Price Forecasting** - 6-month and 1-year stock price predictions
- **GARCH Volatility Modeling** - Forward-looking volatility projections
- **Value at Risk (VAR) & CVaR** - Risk quantification at multiple confidence levels
- **Financial Ratio Analysis** - Liquidity, Solvency, Profitability, Efficiency
- **Scenario Analysis** - Impact of cigarette demand on financial metrics
- **Interactive Dashboards** - Professional visualizations and real-time updates

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- 2GB+ RAM
- Internet connection (for Yahoo Finance data)

### Installation & Setup

**Step 1: Clone or Download Files**
```bash
# Create a project directory
mkdir itc-financial-app
cd itc-financial-app

# Copy all files (app.py, requirements.txt, and ITC__2_.xlsx)
# Ensure ITC__2_.xlsx is in the same directory or update the path in app.py
```

**Step 2: Create Virtual Environment (Optional but Recommended)**
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

**Step 4: Run the Application**
```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

---

## 📱 Application Features

### Tab 1: 📊 Dashboard
- Executive summary with key financial metrics
- Latest financial figures (Revenue, Net Profit, ROE, Margins)
- Financial health assessment cards
- Quick performance overview

### Tab 2: 📈 Market Data
- 10-year stock price history
- Current market metrics and technical indicators
- Price statistics and ranges
- Technical snapshot

### Tab 3: 🔮 Price Forecast (ARIMA)
- Auto-detected ARIMA parameters
- 6-month and 1-year price forecasts
- 95% confidence intervals
- Model diagnostics and fit statistics
- Upside potential analysis

### Tab 4: 📉 Volatility Analysis (GARCH)
- Historical volatility (30, 60, 90-day rolling)
- GARCH(1,1) forward volatility projections
- Volatility trend visualization
- Risk implications

### Tab 5: ⚠️ Value at Risk (VAR)
- Interactive VAR calculator
- VAR at 90%, 95%, 99% confidence levels
- Multiple time horizons (1-day, 5-day, 30-day)
- Risk profile visualization
- Loss distribution charts

### Tab 6: 🎯 Expected Shortfall (CVaR)
- Tail-end risk analysis
- CVaR at multiple confidence levels
- CVaR vs VAR comparison
- Worst-case scenario analysis

### Tab 7: 📑 Financial Ratios
- **Liquidity Ratios**: Current, Quick, Cash ratios
- **Solvency Ratios**: Debt/Equity, Interest Coverage, Debt/EBITDA
- **Profitability Ratios**: Net Margin, ROA, ROE, Dupont Analysis
- **Efficiency Ratios**: Asset Turnover, Inventory Turnover, Days metrics
- 3-year trends and peer comparisons

### Tab 8: 🎲 Scenario Analysis
- Best Case: +15% consumption, +8% pricing
- Average Case: +2% consumption, stable pricing
- Worst Case: -10% consumption, -4% pricing pressure
- 6-month and 1-year financial projections
- Ratio impact under scenarios

### Tab 9: 🔍 Integrated Insights
- Combined market, financial, and scenario views
- Investment recommendations
- Risk considerations
- Action items for investors

### Tab 10: ❓ Help & Glossary
- Model explanations (ARIMA, GARCH, VAR, CVaR)
- Comprehensive glossary
- Frequently asked questions
- Methodology notes

---

## 📊 Data Sources

### Screener.in Excel (ITC__2_.xlsx)
- **P&L Statement**: 10 years of revenue, expenses, profitability data
- **Balance Sheet**: Assets, liabilities, equity, cash positions
- **Cash Flow**: Operating, investing, and financing activities
- **Quarterly Data**: Latest 8 quarters for recent trends

Location: Place file in the same directory as app.py (or update path in app.py)

### Yahoo Finance (Real-time)
- **ITC Stock Data**: ITCL.NS ticker
- **Nifty50 Index**: ^NSEI for market returns
- **Daily Prices**: 5+ years of historical data
- **Company Metrics**: Market cap, dividend yield, PE ratio

---

## ⚙️ Configuration

### Modifying File Paths
If your Excel file is in a different location, edit app.py:

```python
# Line 150 (approx)
file_path = "/path/to/your/ITC__2_.xlsx"  # Change this path
```

### Customizing Scenarios
Edit scenario parameters in Tab 8 section (around line 650):

```python
scenario_data = {
    "BEST CASE: Consumption +15%": {
        "consumption": "+15%",
        "pricing": "+8%",
        # ... modify these values
    }
}
```

### Changing Color Scheme
Modify CSS in the <style> section (lines 30-150):

```css
--primary-color: #003366;      /* Dark blue */
--secondary-color: #004d80;    /* Medium blue */
--accent-color: #FFD700;       /* Gold */
```

---

## 🎨 Design Features

### Professional Styling
- **Color Scheme**: Professional blue (#003366) with gold accents
- **Typography**: Clear, readable fonts with proper hierarchy
- **Spacing**: Generous padding and margins for readability
- **Contrast**: High text contrast for visibility

### Responsive Design
- Works on desktop (optimal) and tablets
- Sidebar navigation for easy access
- Wide tabs for comprehensive information
- Adaptive layouts

### Data Visualization
- **Interactive Plotly Charts**: Hover for details, zoom, pan
- **Color-Coded Metrics**: Green (good), Yellow (warning), Red (danger)
- **Clean Tables**: Sorted, searchable data displays
- **Professional Cards**: Metric cards with clear labels

---

## 📈 How to Use

### First Time Users
1. Open the Dashboard tab to see overview
2. Check Market Data for historical context
3. Review Financial Ratios for company health
4. Look at Price Forecast for investment outlook
5. Analyze Risk (VAR/CVaR) for downside protection
6. Study Scenarios to understand sensitivities
7. Read Help tab for detailed explanations

### For Investment Analysis
1. Start with Integrated Insights tab
2. Review 6-month and 1-year targets
3. Check scenario upside/downside
4. Assess risk tolerance (VAR/CVaR)
5. Monitor key financial metrics

### For Risk Management
1. Use VAR tab to set position sizes
2. Monitor CVaR for tail-end risk
3. Track volatility trends (GARCH)
4. Review scenario impacts
5. Set stop-loss levels

---

## 🔄 Data Updates

### Manual Refresh
Press `R` in the Streamlit app or click "Rerun" to refresh all data.

### Automatic Updates
- **Yahoo Finance**: Fetches latest stock prices automatically
- **Screener.in**: Requires manual Excel file update (quarterly)

### Update Schedule
- Stock prices: Daily (when market is open)
- Financial ratios: Quarterly (after results announcement)
- Forecasts: Monthly (recalibrated)

---

## 🐛 Troubleshooting

### "Module not found" Error
```bash
# Ensure all packages are installed
pip install -r requirements.txt

# Or install individually
pip install streamlit pandas numpy plotly
```

### "File not found" Error
```
# Verify file paths in app.py
# Excel file should be in same directory
# Or use absolute path: C:\Users\YourName\Desktop\ITC__2_.xlsx
```

### "No data displayed" Error
- Check Yahoo Finance connectivity (might be blocked)
- Verify Excel file is in correct location
- Ensure column indices in app.py match your Excel file

### Slow Performance
- Increase caching duration in app.py
- Reduce time horizon for historical data
- Check internet connection for Yahoo Finance

---

## 📊 Model Details

### ARIMA Model
- **Auto-detection**: Automatically finds optimal (p,d,q) parameters
- **Data Used**: 5+ years of daily prices
- **Frequency**: Daily closing prices
- **Validation**: 80/20 train-test split with RMSE verification
- **Interpretation**: Red line = forecast, bands = confidence intervals

### GARCH(1,1) Model
- **Purpose**: Model time-varying volatility
- **Parameters**: Alpha, Beta, Omega calibrated to data
- **Forecast**: 12-month volatility projection
- **Uses**: Risk assessment, option pricing, portfolio management

### VAR Calculation
- **Methods**: Parametric (normal distribution), Historical simulation
- **Confidence Levels**: 90%, 95%, 99%
- **Time Horizons**: 1-day, 5-day, 30-day
- **Formula**: VaR = Portfolio Value × Z-score × Volatility

### CVaR Calculation
- **Definition**: Average loss beyond VAR threshold
- **Advantage**: Captures tail-end risk better than VAR
- **Conservative**: Higher values than VAR (more appropriate for risk-averse)

---

## 📋 File Structure

```
itc-financial-app/
├── app.py                    # Main application
├── requirements.txt          # Dependencies
├── README.md                 # This file
├── ITC__2_.xlsx             # Financial data (from Screener.in)
└── .streamlit/              # Streamlit config (auto-created)
    └── config.toml
```

---

## 🔒 Data Privacy

### Local Deployment
- All data stays on your machine
- No data uploaded to cloud
- Excel file never leaves your computer
- Yahoo Finance queries are read-only

### Cloud Deployment (if used)
- Consider using private Streamlit Cloud space
- Or deploy on private server (AWS, GCP, Azure)
- Ensure data compliance with your policies

---

## 🚀 Deployment Options

### Option 1: Local Desktop (Recommended)
```bash
streamlit run app.py
# Access at http://localhost:8501
```

### Option 2: Streamlit Cloud (Free)
```bash
# 1. Upload to GitHub
# 2. Go to https://share.streamlit.io
# 3. Deploy from GitHub repo
```

### Option 3: AWS (with cost)
```bash
# Use EC2 instance with Python 3.8+
# Install dependencies and run app.py
# Access via public IP:8501
```

### Option 4: Docker Containerization
```dockerfile
FROM python:3.8
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "app.py"]
```

---

## 📚 Learning Resources

### Understanding the Models
- **ARIMA**: Forecasting Time Series (by Brockwell & Davis)
- **GARCH**: Modeling Financial Time Series (widely used in finance)
- **VAR**: Risk Management framework used by all major banks
- **CVaR**: More advanced risk measure than VAR

### Financial Metrics
- **Liquidity Ratios**: Measure ability to pay short-term obligations
- **Solvency Ratios**: Measure long-term financial stability
- **Profitability Ratios**: Measure operational efficiency
- **Efficiency Ratios**: Measure asset utilization

---

## 👤 About the Author

**Prof. V. Ravichandran**
- 28+ Years in Corporate Finance & Banking
- 10+ Years in Academic Excellence
- Specialist in Financial Risk Management
- Expert in Quantitative Finance
- Developer of "The Mountain Path - World of Finance" platform

---

## 📞 Support & Feedback

For issues, questions, or suggestions:
1. Check the Help tab in the app
2. Review the FAQ section
3. Check troubleshooting guide above
4. Verify data file paths and formats

---

## 📄 License & Disclaimer

**Disclaimer:**
This application is for educational and analytical purposes only. It is not investment advice. 
Historical performance does not guarantee future results. Always consult with qualified financial 
advisors before making investment decisions. The developer and authors are not responsible for 
any losses incurred based on this analysis.

---

## 🎯 Version History

**Version 1.0** (January 2025)
- Initial release
- 10 interactive tabs
- ARIMA, GARCH, VAR, CVaR models
- Financial ratio analysis
- Scenario analysis
- Professional styling

---

## ✨ Key Highlights

✅ **Professional Design** - Beautiful, professional interface
✅ **Comprehensive Analysis** - Market + Financial + Scenarios
✅ **Interactive Charts** - Plotly visualizations
✅ **Real-time Data** - Yahoo Finance integration
✅ **Easy to Use** - Intuitive navigation
✅ **Responsive** - Works on desktop and tablets
✅ **Well-Documented** - Complete help and glossary
✅ **Extensible** - Easy to modify and enhance

---

## 🎓 Educational Value

Perfect for:
- MBA Finance students
- CFA aspirants
- Financial risk managers
- Investment analysts
- Finance professionals
- Anyone interested in quantitative finance

---

## 📞 Quick Support

**Q: The app won't start**
A: Run `pip install -r requirements.txt` and try again

**Q: Charts aren't showing**
A: Try `streamlit run app.py --logger.level=debug` for diagnostics

**Q: Data looks wrong**
A: Verify ITC__2_.xlsx is in correct location with correct sheet names

**Q: Need custom analysis**
A: Edit the Python code directly (well-commented for easy modification)

---

## 🎉 Congratulations!

You now have a professional-grade financial analysis platform. 
Enjoy analyzing ITC Ltd and building investment insights!

**Happy Analyzing!** 📊📈🚀
