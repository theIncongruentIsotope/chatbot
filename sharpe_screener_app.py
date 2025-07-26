import streamlit as st
import pandas as pd
import json
import subprocess
import datetime
import os
import altair as alt
import time

DATA_DIR = 'sharpe_outputs'
DEFAULT_FILE = os.path.join(DATA_DIR, 'sharpe_filtered.json')

@st.cache_data(ttl=3600)
def load_data(file_path):
    with open(file_path, 'r') as f:
        return pd.read_json(f)

def refresh_data():
    start = time.time()
    with st.spinner('Fetching latest data... this may take 3–5 minutes.'):
        subprocess.run(['python', 'full_sharpe_script.py'])
        duration = round(time.time() - start, 2)
        st.success(f'Data refreshed in {duration} seconds!')
        return load_data(DEFAULT_FILE), duration

def main():
    st.set_page_config(page_title='Sharpe Ratio Screener', layout='wide')
    st.title('📈 Sharpe Ratio Screener — Top 1000 US Stocks')

    # Sidebar filters
    st.sidebar.header('🔍 Filters')
    min_sharpe = st.sidebar.slider('Minimum Sharpe Ratio', 0.0, 3.0, 1.5, 0.1)
    beta_range = st.sidebar.slider('Beta Range', 0.0, 3.0, (0.5, 1.5), 0.1)

    # Load or refresh data
    load_duration = None
    if not os.path.exists(DEFAULT_FILE):
        st.warning('No precomputed data found. Please refresh.')
        if st.button('🔄 Refresh Data'):
            df, load_duration = refresh_data()
    else:
        df = load_data(DEFAULT_FILE)

    if st.sidebar.button('🔁 Refresh Live Data'):
        df, load_duration = refresh_data()

    # Fill in missing sector data
    df['Sector'] = df['Sector'].fillna('Unknown')
    all_sectors = df['Sector'].unique().tolist()
    selected_sectors = st.sidebar.multiselect('Sectors', all_sectors, default=all_sectors)

    # Filter data
    df_filtered = df[(df['Sharpe Ratio'] >= min_sharpe) &
                     (df['Beta'] >= beta_range[0]) &
                     (df['Beta'] <= beta_range[1]) &
                     (df['Sector'].isin(selected_sectors))]

    st.markdown(f"### 📊 {len(df_filtered)} Securities with Sharpe > {min_sharpe} and Beta in {beta_range}")
    if load_duration:
        st.caption(f"Last refresh took {load_duration} seconds")

    st.dataframe(df_filtered, use_container_width=True)

    # Charts
    st.markdown("### 🎯 Sharpe vs Beta Scatter Plot")
    scatter_chart = alt.Chart(df_filtered).mark_circle(size=60).encode(
        x=alt.X('Beta', scale=alt.Scale(zero=False)),
        y=alt.Y('Sharpe Ratio', scale=alt.Scale(zero=False)),
        color='Sector',
        tooltip=['Ticker', 'Sharpe Ratio', 'Beta', 'Annual Return (%)']
    ).interactive().properties(height=400)
    st.altair_chart(scatter_chart, use_container_width=True)

    st.markdown("### 📈 Sharpe Ratio Distribution")
    hist_chart = alt.Chart(df_filtered).mark_bar().encode(
        x=alt.X('Sharpe Ratio', bin=True),
        y='count()',
        tooltip=['count()']
    ).properties(height=300)
    st.altair_chart(hist_chart, use_container_width=True)

    st.markdown("### 📌 Sector Breakdown")
    sector_counts = df_filtered['Sector'].value_counts()
    st.bar_chart(sector_counts)

    # Download buttons
    st.markdown("### 📥 Export Filtered Data")
    st.download_button(
        label="Download CSV",
        data=df_filtered.to_csv(index=False),
        file_name=f'sharpe_filtered_{datetime.date.today()}.csv',
        mime='text/csv')

    st.download_button(
        label="Download JSON",
        data=df_filtered.to_json(orient='records', indent=2),
        file_name=f'sharpe_filtered_{datetime.date.today()}.json',
        mime='application/json')

if __name__ == '__main__':
    main()

