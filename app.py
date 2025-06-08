import streamlit as st
import pandas as pd
from database import connect_to_database, load_data
from processing import filter_data, calculate_kpis
from predictions import generate_sales_prediction, generate_performance_alert, generate_retailer_alert, generate_geographic_insights
from visualizations import (
    plot_sales_profit_trend, plot_multi_period_trend, plot_annual_sales_profit,
    plot_units_trend, plot_top_retailers, plot_retailer_performance,
    plot_product_category_performance, plot_gender_distribution, plot_gender_preferences,
    plot_gender_trend, plot_units_per_category, plot_margin_per_category,
    plot_regional_sales, plot_sales_map, plot_sales_method_distribution, plot_sales_method_trend
)

# Set page configuration
st.set_page_config(layout="wide", page_title="Dashboard Analisis Penjualan Adidas")

# Load CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    # Connect to database
    engine = connect_to_database()
    
    # Load data
    df = load_data(engine)
    if df.empty:
        st.warning("Tidak ada data yang dimuat. Periksa database atau query.")
        return
    
    # Filter periode
    period_options = {
        "Jan 2020 - Des 2021": (pd.to_datetime("2020-01-01"), pd.to_datetime("2021-12-31")),
        "2021 Full Year": (pd.to_datetime("2021-01-01"), pd.to_datetime("2021-12-31")),
        "Q1 2021": (pd.to_datetime("2021-01-01"), pd.to_datetime("2021-03-31")),
        "Last 6 Months": (df['invoice_date'].max() - pd.Timedelta(days=180), df['invoice_date'].max())
    }
    selected_period = st.selectbox("Pilih Periode", list(period_options.keys()), key="period_filter")
    start_date, end_date = period_options[selected_period]
    filtered_df = filter_data(df, start_date, end_date)
    
    # Header
    st.markdown(f"""
        <div class="header">
            <h1>Dashboard Analisis Penjualan Adidas</h1>
            <div class="controls">
                <select class="filter-dropdown">
                    <option>{selected_period}</option>
                </select>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Section 1: Summary Metrics
    st.markdown('<div class="section"><div class="section-title">Ringkasan Metrik</div><div class="kpi-grid">', unsafe_allow_html=True)
    kpis = calculate_kpis(filtered_df, df)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Total Penjualan</div>
                <div class="kpi-value">Rp {kpis['total_sales']:,.1f} M</div>
                <div class="kpi-label">Periode: {selected_period}</div>
            </div>
        """, unsafe_allow_html=True)
        sales_alert = generate_performance_alert(kpis['total_sales'], kpis['historical_avg_sales'], "Penjualan")
        alert_class = "alert-success" if "🟢" in sales_alert else "alert-danger" if "🔴" in sales_alert else "alert-warning"
        st.markdown(f'<div class="{alert_class}">{sales_alert}</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Total Keuntungan</div>
                <div class="kpi-value">Rp {kpis['total_profit']:,.1f} M</div>
                <div class="kpi-label">Periode: {selected_period}</div>
            </div>
        """, unsafe_allow_html=True)
        profit_alert = generate_performance_alert(kpis['total_profit'], kpis['historical_avg_profit'], "Keuntungan")
        alert_class = "alert-success" if "🟢" in profit_alert else "alert-danger" if "🔴" in profit_alert else "alert-warning"
        st.markdown(f'<div class="{alert_class}">{profit_alert}</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Unit Terjual</div>
                <div class="kpi-value">{kpis['total_units']:,.2f} Juta</div>
                <div class="kpi-label">Periode: {selected_period}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Harga Rata-rata</div>
                <div class="kpi-value">Rp {kpis['avg_price']:,.0f}</div>
                <div class="kpi-label">Periode: {selected_period}</div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # Section 2: Sales Trends
    st.markdown('<div class="section"><div class="section-title">Tren Penjualan</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        monthly_data = filtered_df.groupby('month').agg({'total_sales': 'sum', 'operating_profit': 'sum'}).reset_index()
        prediction_result, _, _ = generate_sales_prediction(monthly_data, algorithm='random_forest')
        plot_sales_profit_trend(monthly_data, prediction_result)
    
    with col2:
        plot_multi_period_trend(filtered_df)
    
    col3, col4 = st.columns(2)
    with col3:
        plot_annual_sales_profit(filtered_df)
    with col4:
        plot_units_trend(filtered_df)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 3: Retailer Insights
    st.markdown('<div class="section"><div class="section-title">Wawasan Pengecer</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        plot_top_retailers(filtered_df)
        retailer_data = filtered_df.groupby('retailer_name').agg({'total_sales': 'sum'}).reset_index()
        retailer_alerts = generate_retailer_alert(retailer_data)
        for alert in retailer_alerts:
            alert_class = "alert-success" if "🏆" in alert else "alert-warning"
            st.markdown(f'<div class="{alert_class}">{alert}</div>', unsafe_allow_html=True)
    
    with col2:
        plot_retailer_performance(filtered_df)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 4: Product & Gender Analysis
    st.markdown('<div class="section"><div class="section-title">Analisis Produk & Gender</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        plot_product_category_performance(filtered_df)
    with col2:
        plot_gender_distribution(filtered_df)
    with col3:
        plot_gender_preferences(filtered_df)
    
    col4, col5, col6 = st.columns(3)
    with col4:
        plot_gender_trend(filtered_df)
    with col5:
        plot_units_per_category(filtered_df)
    with col6:
        plot_margin_per_category(filtered_df)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 5: Geographic Insights
    st.markdown('<div class="section"><div class="section-title">Wawasan Geografis</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        plot_regional_sales(filtered_df)
        regional_sales = filtered_df.groupby('region').agg({'total_sales': 'sum'}).reset_index()
        geo_insights = generate_geographic_insights(regional_sales)
        for insight in geo_insights:
            alert_class = "alert-success" if "🎯" in insight else "alert-warning"
            st.markdown(f'<div class="{alert_class}">{insight}</div>', unsafe_allow_html=True)
    
    with col2:
        plot_sales_map(filtered_df)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 6: Sales Method Insights
    st.markdown('<div class="section"><div class="section-title">Wawasan Metode Penjualan</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        plot_sales_method_distribution(filtered_df)
    with col2:
        plot_sales_method_trend(filtered_df)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Narrative Analysis
    st.markdown('<div class="section"><div class="section-title">Wawasan Pasar</div>', unsafe_allow_html=True)
    st.markdown("""
        **Observasi Utama:**
        1. **Tren Penjualan**: Prediksi menggunakan Random Forest menunjukkan akurasi lebih baik (MAE lebih rendah) dibandingkan Linear Regression.
        2. **Wawasan Pengecer**: Fokus pada pengecer dengan marjin rendah untuk strategi peningkatan.
        3. **Analisis Produk & Gender**: Sesuaikan pemasaran berdasarkan preferensi gender.
        4. **Wawasan Geografis**: Ekspansi ke wilayah dengan penjualan rendah untuk pertumbuhan.
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()