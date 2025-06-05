import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sqlalchemy import create_engine
from sklearn.linear_model import LinearRegression
import numpy as np

# Set page configuration for wide layout
st.set_page_config(layout="wide", page_title="Dashboard Analisis Penjualan Adidas")

# Custom CSS to mimic the design
st.markdown("""
    <style>
    /* Background gradient */
    .stApp {
        background: linear-gradient(90deg, #6b48ff, #00d4ff);
        color: white;
    }
    /* Title styling */
    .title {
        font-size: 2.5em;
        font-weight: bold;
        color: white;
        text-align: left;
        margin-bottom: 20px;
    }
    /* Metric box styling */
    .metric-box {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-size: 1.2em;
    }
    /* Sidebar styling */
    .css-1d391kg {
        background-color: rgba(255, 255, 255, 0.2);
    }
    /* Metric value */
    .metric-value {
        font-size: 1.8em;
        font-weight: bold;
    }
    /* Metric label */
    .metric-label {
        font-size: 0.9em;
        color: rgba(255, 255, 255, 0.8);
    }
    </style>
""", unsafe_allow_html=True)

# Database connection
engine = create_engine('postgresql+psycopg2://postgres:nadia1624@localhost:5432/DW_Adidas')

# Load data
@st.cache_data
def load_data():
    query = """
    SELECT 
        fs.sales_id, dr.retailer_name, dd.year, dd.month, dd.quarter, dd.day, dd.weekday, 
        dl.region, dl.state, dl.city, dp.product_category, dp.price_per_unit, 
        dg.gender_type, dsm.sales_method, fs.units_sold, fs.total_sales, fs.operating_profit, fs.operating_margin
    FROM fact_sales fs
    JOIN dim_retailer dr ON fs.retailer_id = dr.retailer_id
    JOIN dim_date dd ON fs.date_id = dd.date_id
    JOIN dim_location dl ON fs.location_id = dl.location_id
    JOIN dim_product dp ON fs.product_id = dp.product_id
    JOIN dim_gender dg ON fs.gender_id = dg.gender_id
    JOIN dim_sales_method dsm ON fs.sales_method_id = dsm.sales_method_id
    """
    df = pd.read_sql(query, engine)
    return df

df = load_data()

# Sidebar for navigation
st.sidebar.title("Dashboard Navigation")
pages = {
    "Dashboard Eksekutif": ["Tren Penjualan dan Profit", "Distribusi Penjualan Regional"],
    "Dashboard Analisis Pengecer": ["Top 10 Pengecer", "Scatter Plot Pengecer"],
    "Dashboard Segmentasi Produk": ["Performa Kategori Produk", "Distribusi Gender per Kategori"],
    "Dashboard Analisis Geografis": ["Peta Penjualan Interaktif", "Treemap Hierarki Penjualan"],
    "Dashboard Analisis Temporal": ["Tren Penjualan Multi-Periode", "Decomposition Plot"],
    "Dashboard Profitabilitas & Harga": ["Hubungan Harga dan Volume", "Heatmap Profitabilitas"],
    "Dashboard Analisis Gender": ["Preferensi Produk per Gender", "Tren Pembelian Gender"],
    "Dashboard Metode Penjualan": ["Perbandingan Metode Penjualan", "Tren Metode Penjualan"],
    "Dashboard Performa Tahunan": ["Penjualan dan Profit Tahunan", "Pencapaian Target"],
    "Dashboard Analisis Unit Terjual": ["Unit Terjual per Kategori", "Tren Unit Terjual"]
}
selection = st.sidebar.selectbox("Pilih Dashboard", list(pages.keys()))
chart_selection = st.sidebar.selectbox("Pilih Grafik", pages[selection])

# Title
st.markdown('<div class="title">Dashboard Analisis Penjualan Adidas</div>', unsafe_allow_html=True)

# Key Metrics (similar to "Ringkasan Metrik" in your design)
total_sales = df['total_sales'].sum() / 1e6  # In millions
total_profit = df['operating_profit'].sum() / 1e6  # In millions
avg_margin = df['operating_margin'].mean() * 100  # In percentage
avg_price = df['price_per_unit'].mean()  # Average price per unit

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div class="metric-box"><div class="metric-value">Rp {total_sales:,.1f} M</div><div class="metric-label">Total Penjualan</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-box"><div class="metric-value">Rp {total_profit:,.1f} M</div><div class="metric-label">Total Keuntungan</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-box"><div class="metric-value">{avg_margin:,.1f}%</div><div class="metric-label">Margin Rata-rata</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-box"><div class="metric-value">Rp {avg_price:,.1f}</div><div class="metric-label">Harga Rata-rata</div></div>', unsafe_allow_html=True)

# Prediction function
def predict_sales(df, period='month'):
    df_pred = df.groupby(period).agg({'total_sales': 'sum'}).reset_index()
    X = np.array(range(len(df_pred))).reshape(-1, 1)
    y = df_pred['total_sales'].values.reshape(-1, 1)
    model = LinearRegression()
    model.fit(X, y)
    future_periods = 12
    future_X = np.array(range(len(df_pred), len(df_pred) + future_periods)).reshape(-1, 1)
    predictions = model.predict(future_X)
    return pd.DataFrame({'period': range(len(df_pred), len(df_pred) + future_periods), 'predicted_sales': predictions.flatten()})

# Layout for charts (2x2 grid like in your design)
col_left, col_right = st.columns(2)

# Dashboard Eksekutif
if selection == "Dashboard Eksekutif":
    with col_left:
        if chart_selection == "Tren Penjualan dan Profit":
            monthly_data = df.groupby('month').agg({'total_sales': 'sum', 'operating_profit': 'sum'}).reset_index()
            fig, ax1 = plt.subplots(figsize=(6, 4))
            ax1.plot(monthly_data['month'], monthly_data['total_sales'], 'b-', label='Total Sales')
            ax1.set_xlabel('Month')
            ax1.set_ylabel('Total Sales', color='b')
            ax2 = ax1.twinx()
            ax2.plot(monthly_data['month'], monthly_data['operating_profit'], 'r-', label='Operating Profit')
            ax2.set_ylabel('Operating Profit', color='r')
            plt.title('Tren Penjualan dan Profit')
            st.pyplot(fig)
            pred_data = predict_sales(df, 'month')
            st.write("Prediksi Penjualan Bulan Depan:", pred_data['predicted_sales'].iloc[0])

    with col_right:
        if chart_selection == "Distribusi Penjualan Regional":
            regional_sales = df.groupby('region').agg({'total_sales': 'sum'}).reset_index()
            fig = px.choropleth(regional_sales, locations='region', locationmode='USA-states', color='total_sales',
                                color_continuous_scale='Viridis', title='Distribusi Penjualan Regional')
            st.plotly_chart(fig, use_container_width=True)

# Dashboard Analisis Pengecer
if selection == "Dashboard Analisis Pengecer":
    with col_left:
        if chart_selection == "Top 10 Pengecer":
            top_retailers = df.groupby('retailer_name').agg({'total_sales': 'sum', 'operating_margin': 'mean'}).nlargest(10, 'total_sales')
            fig = px.bar(top_retailers, x='total_sales', y=top_retailers.index, orientation='h',
                         color='operating_margin', color_continuous_scale='RdYlGn',
                         title='Top 10 Pengecer')
            st.plotly_chart(fig, use_container_width=True)

    with col_right:
        if chart_selection == "Scatter Plot Pengecer":
            retailer_perf = df.groupby('retailer_name').agg({'total_sales': 'sum', 'operating_margin': 'mean'}).reset_index()
            fig = px.scatter(retailer_perf, x='total_sales', y='operating_margin', color='retailer_name',
                             title='Scatter Plot Pengecer')
            st.plotly_chart(fig, use_container_width=True)

# Dashboard Segmentasi Produk
if selection == "Dashboard Segmentasi Produk":
    with col_left:
        if chart_selection == "Performa Kategori Produk":
            cat_perf = df.groupby('product_category').agg({'total_sales': 'sum', 'operating_profit': 'sum'}).reset_index()
            fig = px.bar(cat_perf, x='product_category', y=['total_sales', 'operating_profit'],
                         title='Performa Kategori Produk', barmode='group')
            st.plotly_chart(fig, use_container_width=True)

    with col_right:
        if chart_selection == "Distribusi Gender per Kategori":
            gender_dist = df.groupby(['product_category', 'gender_type']).agg({'total_sales': 'sum'}).reset_index()
            fig = px.bar(gender_dist, x='product_category', y='total_sales', color='gender_type',
                         title='Distribusi Gender per Kategori', barmode='stack')
            st.plotly_chart(fig, use_container_width=True)

# Dashboard Analisis Geografis
if selection == "Dashboard Analisis Geografis":
    with col_left:
        if chart_selection == "Peta Penjualan Interaktif":
            sales_map = df.groupby(['region', 'state', 'city']).agg({'total_sales': 'sum'}).reset_index()
            fig = px.scatter_mapbox(sales_map, lat=[0], lon=[0], hover_name='city', hover_data=['total_sales'],
                                    zoom=3, height=300, title='Peta Penjualan Interaktif')
            st.plotly_chart(fig, use_container_width=True)

    with col_right:
        if chart_selection == "Treemap Hierarki Penjualan":
            treemap_data = df.groupby(['region', 'state', 'city']).agg({'total_sales': 'sum', 'operating_margin': 'mean'}).reset_index()
            fig = px.treemap(treemap_data, path=['region', 'state', 'city'], values='total_sales',
                             color='operating_margin', color_continuous_scale='RdYlGn',
                             title='Treemap Hierarki Penjualan')
            st.plotly_chart(fig, use_container_width=True)

# Add similar blocks for other dashboards as needed...

# Run the app
if __name__ == "__main__":
    st.markdown('<div style="text-align: right; color: white;">Jan 2024 - Mei 2025</div>', unsafe_allow_html=True)