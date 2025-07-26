# 📈 Sharpe Ratio Screener

A high-performance Streamlit dashboard for screening the top 1000 U.S. stocks by market cap based on their Sharpe Ratio, beta, and sector exposure.

## 🔧 Features

- ✅ Computes **Sharpe Ratios**, **Beta**, **Annual Return**, and **Volatility**
- ✅ Filters by:
  - Sharpe Ratio (e.g., > 1.5)
  - Beta Range (e.g., 0.5–1.5)
  - Sector (multiselect)
- ✅ On-demand **data refresh** with performance timer
- ✅ Interactive visualizations:
  - Scatter plot: **Sharpe Ratio vs Beta**
  - Histogram: **Sharpe distribution**
  - Bar chart: **Sector breakdown**
- ✅ Export filtered results to **CSV** or **JSON**
- ✅ Caching for fast reloads

---

## 📁 Folder Structure
/
├── sharpe_screener_app.py # Streamlit UI
├── full_sharpe_script.py # Backend computation for Sharpe & Beta
├── requirements.txt # Package list
├── README.md
└── sharpe_outputs/
└── sharpe_filtered.json # Cached results from last full refresh


---

## 📦 Install Requirements

```bash
pip install -r requirements.txt

🚀 Run Locally

streamlit run sharpe_screener_app.py
