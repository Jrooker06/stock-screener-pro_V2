
import streamlit as st
import pandas as pd
import yfinance as yf
import filters_sidebar_grouped_dynamic as filters_sidebar

st.set_page_config(page_title="Wolf Screener", layout="wide")

# Logo and header
wolf_url = "https://i.imgur.com/yOAdO7R.png'"
st.sidebar.image(wolf_url, width=180)
st.markdown(
    f"""
    <div style='display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;'>
        <img src='{wolf_url}' width='40'/>
        <h2 style='margin: 0; color: #c5a46d;'>Wolf Screener</h2>
    </div>
    """,
    unsafe_allow_html=True
)

tickers = ["AAPL", "MSFT", "GOOG", "NVDA"]

@st.cache_data(ttl=3600)
def load_data():
    rows = []
    for t in tickers:
        try:
            info = yf.Ticker(t).info
            rows.append({
                "Symbol": t,
                "Price": info.get("regularMarketPrice", 0),
                "P/E Ratio": info.get("trailingPE", 0),
                "Market Cap": round(info.get("marketCap", 0) / 1e9, 2),
                "EPS Growth": f"{info.get('earningsQuarterlyGrowth', 0) * 100:.0f}%",
                "Sector": info.get("sector", "N/A")
            })
        except:
            continue
    return pd.DataFrame(rows)

df = load_data()

filters_sidebar.show_sidebar_filters(df)

st.markdown("### Stock Overview")
selected_cols = st.multiselect("Select columns to show", list(df.columns), default=list(df.columns))
st.dataframe(df[selected_cols], use_container_width=True)
