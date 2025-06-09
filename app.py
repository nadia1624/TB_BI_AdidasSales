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
st.set_page_config(
    layout="wide", 
    page_title="Adidas Sales Analysis Dashboard",
    page_icon="👟",
    initial_sidebar_state="expanded"
)

# Initialize session state for theme
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

def get_theme_styles():
    """Return CSS styles for dark mode with Adidas dashboard color palette"""
    if st.session_state.dark_mode:
        return """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            
            .stApp {
                background: linear-gradient(135deg, #2d1b69 0%, #1a0f3d 50%, #0f0629 100%);
                color: white;
            }
            
            .main {
                padding: 0rem 1rem;
            }
            
            .dashboard-header {
                background: linear-gradient(135deg, #7c4dff 0%, #6a1b9a 50%, #4a148c 100%);
                padding: 2.5rem;
                border-radius: 20px;
                margin-bottom: 2rem;
                box-shadow: 0 20px 40px rgba(124, 77, 255, 0.4);
                position: relative;
                overflow: hidden;
            }
            
            .dashboard-header::before {
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: linear-gradient(45deg, transparent, rgba(255,255,255,0.15), transparent);
                transform: rotate(45deg);
                animation: shine 3s infinite;
            }
            
            @keyframes shine {
                0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
                100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
            }
            
            .dashboard-title {
                color: white;
                font-family: 'Inter', sans-serif;
                font-size: 2.8rem;
                font-weight: 700;
                margin: 0;
                text-align: center;
                text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.5);
                position: relative;
                z-index: 1;
            }
            
            .dashboard-subtitle {
                color: rgba(255, 255, 255, 0.9);
                font-family: 'Inter', sans-serif;
                font-size: 1.1rem;
                font-weight: 400;
                text-align: center;
                margin-top: 0.5rem;
                position: relative;
                z-index: 1;
            }
            
            .section-container {
                background: rgba(124, 77, 255, 0.1);
                backdrop-filter: blur(15px);
                border: 1px solid rgba(124, 77, 255, 0.3);
                border-radius: 20px;
                padding: 2rem;
                margin-bottom: 2rem;
                box-shadow: 0 8px 32px rgba(124, 77, 255, 0.2);
            }
            
            .section-title {
                font-family: 'Inter', sans-serif;
                font-size: 1.8rem;
                font-weight: 600;
                color: white;
                margin-bottom: 1.5rem;
                padding-bottom: 0.5rem;
                border-bottom: 3px solid #7c4dff;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            
            .kpi-card {
                background: linear-gradient(135deg, rgba(124, 77, 255, 0.25) 0%, rgba(156, 39, 176, 0.25) 50%, rgba(74, 20, 140, 0.25) 100%);
                backdrop-filter: blur(15px);
                border: 2px solid rgba(124, 77, 255, 0.4);
                border-radius: 16px;
                padding: 1.5rem;
                text-align: center;
                box-shadow: 0 8px 32px rgba(124, 77, 255, 0.3);
                transition: all 0.3s ease;
                height: 160px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                position: relative;
                overflow: hidden;
            }
            
            .kpi-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
                transition: left 0.5s;
            }
            
            .kpi-card:hover::before {
                left: 100%;
            }
            
            .kpi-card:hover {
                transform: translateY(-8px) scale(1.02);
                box-shadow: 0 20px 40px rgba(124, 77, 255, 0.5);
                border-color: rgba(124, 77, 255, 0.8);
                background: linear-gradient(135deg, rgba(124, 77, 255, 0.35) 0%, rgba(156, 39, 176, 0.35) 50%, rgba(74, 20, 140, 0.35) 100%);
            }
            
            .kpi-value {
                font-family: 'Inter', sans-serif;
                font-size: 2.2rem;
                font-weight: 700;
                color: white;
                margin: 0.5rem 0;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            }
            
            .kpi-label {
                font-family: 'Inter', sans-serif;
                font-size: 0.9rem;
                font-weight: 500;
                color: rgba(255, 255, 255, 0.85);
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            .kpi-period {
                font-family: 'Inter', sans-serif;
                font-size: 0.8rem;
                color: rgba(255, 255, 255, 0.65);
                margin-top: 0.3rem;
            }
            
            .chart-container {
                background: rgba(124, 77, 255, 0.08);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(124, 77, 255, 0.25);
                border-radius: 15px;
                padding: 1.5rem;
                box-shadow: 0 4px 20px rgba(124, 77, 255, 0.15);
                margin-bottom: 1rem;
            }
            
            .alert {
                padding: 1rem 1.2rem;
                border-radius: 12px;
                margin: 0.5rem 0;
                font-family: 'Inter', sans-serif;
                font-size: 0.9rem;
                font-weight: 500;
                border-left: 4px solid;
                backdrop-filter: blur(10px);
                animation: slideIn 0.5s ease-out;
            }
            
            .alert-success {
                background: rgba(76, 175, 80, 0.25);
                color: #a5d6a7;
                border-left-color: #4caf50;
            }
            
            .alert-warning {
                background: rgba(255, 193, 7, 0.25);
                color: #fff176;
                border-left-color: #ffc107;
            }
            
            .alert-danger {
                background: rgba(244, 67, 54, 0.25);
                color: #ef9a9a;
                border-left-color: #f44336;
            }
            
            .alert-info {
                background: rgba(124, 77, 255, 0.25);
                color: #b39ddb;
                border-left-color: #7c4dff;
            }
            
            .insight-box {
                background: linear-gradient(135deg, rgba(124, 77, 255, 0.15) 0%, rgba(156, 39, 176, 0.15) 100%);
                backdrop-filter: blur(15px);
                border: 1px solid rgba(124, 77, 255, 0.3);
                border-radius: 16px;
                padding: 2rem;
                margin: 1rem 0;
                border-left: 4px solid #7c4dff;
                box-shadow: 0 4px 20px rgba(124, 77, 255, 0.15);
            }
            
            .insight-title {
                font-family: 'Inter', sans-serif;
                font-size: 1.3rem;
                font-weight: 600;
                color: white;
                margin-bottom: 1rem;
            }
            
            .insight-text {
                font-family: 'Inter', sans-serif;
                font-size: 0.95rem;
                line-height: 1.7;
                color: rgba(255, 255, 255, 0.9);
            }
            
            @keyframes slideIn {
                from { opacity: 0; transform: translateX(-20px); }
                to { opacity: 1; transform: translateX(0); }
            }
            .chart-title {
                color: white;
                font-weight: bold;
            }
        </style>
        """
    else:
        return """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            
            /* Light Mode Styles - Adidas Purple Theme */
            .stApp {
                background: linear-gradient(135deg, #f3f0ff 0%, #e8e0ff 50%, #ddd6fe 100%);
            }
            
            .main {
                padding: 0rem 1rem;
            }

            .chart-title {
                color: #4a148c;
                font-weight: bold;
            }
            
            .dashboard-header {
                background: linear-gradient(135deg, #7c4dff 0%, #6a1b9a 50%, #4a148c 100%);
                padding: 2.5rem;
                border-radius: 20px;
                margin-bottom: 2rem;
                box-shadow: 0 20px 40px rgba(124, 77, 255, 0.3);
                position: relative;
                overflow: hidden;
            }
            
            .dashboard-header::before {
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: linear-gradient(45deg, transparent, rgba(255,255,255,0.25), transparent);
                transform: rotate(45deg);
                animation: shine 3s infinite;
            }
            
            @keyframes shine {
                0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
                100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
            }
            
            .dashboard-title {
                color: white;
                font-family: 'Inter', sans-serif;
                font-size: 2.8rem;
                font-weight: 700;
                margin: 0;
                text-align: center;
                text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);
                position: relative;
                z-index: 1;
            }
            
            .dashboard-subtitle {
                color: rgba(255, 255, 255, 0.95);
                font-family: 'Inter', sans-serif;
                font-size: 1.1rem;
                font-weight: 400;
                text-align: center;
                margin-top: 0.5rem;
                position: relative;
                z-index: 1;
            }
            
            .theme-toggle {
                position: absolute;
                top: 1rem;
                right: 1rem;
                z-index: 10;
            }
            
            .section-container {
                background: white;
                border-radius: 20px;
                padding: 2rem;
                margin-bottom: 2rem;
                box-shadow: 0 10px 40px rgba(124, 77, 255, 0.15);
                border: 2px solid rgba(124, 77, 255, 0.1);
            }
            
            .section-title {
                font-family: 'Inter', sans-serif;
                font-size: 1.8rem;
                font-weight: 600;
                color: #4a148c;
                margin-bottom: 1.5rem;
                padding-bottom: 0.5rem;
                border-bottom: 3px solid #7c4dff;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            
            .kpi-card {
                background: linear-gradient(135deg, #f8f5ff 0%, #f0ebff 50%, #e8deff 100%);
                border: 2px solid rgba(124, 77, 255, 0.3);
                border-radius: 16px;
                padding: 1.5rem;
                text-align: center;
                box-shadow: 0 8px 25px rgba(124, 77, 255, 0.2);
                transition: all 0.3s ease;
                height: 160px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                position: relative;
                overflow: hidden;
            }
            
            .kpi-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(124, 77, 255, 0.15), transparent);
                transition: left 0.5s;
            }
            
            .kpi-card:hover::before {
                left: 100%;
            }
            
            .kpi-card:hover {
                transform: translateY(-8px) scale(1.02);
                box-shadow: 0 20px 40px rgba(124, 77, 255, 0.3);
                border-color: rgba(124, 77, 255, 0.6);
                background: linear-gradient(135deg, #f5f0ff 0%, #ede4ff 50%, #e5d8ff 100%);
            }
            
            .kpi-value {
                font-family: 'Inter', sans-serif;
                font-size: 2.2rem;
                font-weight: 700;
                color: #4a148c;
                margin: 0.5rem 0;
                text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
            }
            
            .kpi-label {
                font-family: 'Inter', sans-serif;
                font-size: 0.9rem;
                font-weight: 500;
                color: #7c4dff;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            .kpi-period {
                font-family: 'Inter', sans-serif;
                font-size: 0.8rem;
                color: #6a1b9a;
                margin-top: 0.3rem;
            }
            
            .chart-container {
                background: white;
                border-radius: 15px;
                padding: 1.5rem;
                box-shadow: 0 4px 20px rgba(124, 77, 255, 0.1);
                border: 1px solid rgba(124, 77, 255, 0.15);
                margin-bottom: 1rem;
            }
            
            .alert {
                padding: 1rem 1.2rem;
                border-radius: 12px;
                margin: 0.5rem 0;
                font-family: 'Inter', sans-serif;
                font-size: 0.9rem;
                font-weight: 500;
                border-left: 4px solid;
                animation: slideIn 0.5s ease-out;
            }
            
            .alert-success {
                background-color: #e8f5e8;
                color: #2e7d2e;
                border-left-color: #4caf50;
            }
            
            .alert-warning {
                background-color: #fffbf0;
                color: #b8860b;
                border-left-color: #ffc107;
            }
            
            .alert-danger {
                background-color: #ffeaea;
                color: #c62828;
                border-left-color: #f44336;
            }
            
            .alert-info {
                background-color: #f3f0ff;
                color: #4a148c;
                border-left-color: #7c4dff;
            }
            
            .insight-box {
                background: linear-gradient(135deg, #f8f5ff 0%, #f0ebff 100%);
                border-radius: 16px;
                padding: 2rem;
                margin: 1rem 0;
                border-left: 4px solid #7c4dff;
                box-shadow: 0 4px 20px rgba(124, 77, 255, 0.15);
                border: 1px solid rgba(124, 77, 255, 0.1);
            }
            
            .insight-title {
                font-family: 'Inter', sans-serif;
                font-size: 1.3rem;
                font-weight: 600;
                color: #4a148c;
                margin-bottom: 1rem;
            }
            
            .insight-text {
                font-family: 'Inter', sans-serif;
                font-size: 0.95rem;
                line-height: 1.7;
                color: #5e35b1;
            }
            
            @keyframes slideIn {
                from { opacity: 0; transform: translateX(-20px); }
                to { opacity: 1; transform: translateX(0); }
            }
        </style>
        """

def create_kpi_card(label, value, period, alert=None):
    """Helper function to create consistent KPI cards"""
    card_html = f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-period">{period}</div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
    
    if alert:
        alert_class = "alert-success" if "🟢" in alert else "alert-danger" if "🔴" in alert else "alert-warning"
        st.markdown(f'<div class="alert {alert_class}">{alert}</div>', unsafe_allow_html=True)

def main():
    # Apply theme styles
    st.markdown(get_theme_styles(), unsafe_allow_html=True)
    
    # Main Dashboard Header with theme toggle
    st.markdown(f"""
    <div class="dashboard-header">
        <div class="theme-toggle">
        </div>
        <h1 class="dashboard-title">👟 Dashboard Analisis Penjualan Adidas</h1>
        <div class="dashboard-subtitle">Real-time insights and analytics for strategic decision making</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Theme toggle functionality
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button(
            "🌙 Switch to Dark Mode" if not st.session_state.dark_mode else "☀️ Switch to Light Mode",
            key="theme_toggle",
            help="Toggle between light and dark mode"
        ):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    
    # Sidebar Configuration
    with st.sidebar:
        st.markdown("### 📊 Dashboard Controls")
        
        # Connect to database
        engine = connect_to_database()
        
        # Load data with progress indicator
        with st.spinner("Loading data..."):
            df = load_data(engine)
        
        if df.empty:
            st.error("❌ No data loaded. Check database or query.")
            return
        
        st.success(f"✅ Data loaded successfully")
        st.info(f"📈 {len(df):,} records | {len(df.columns)} columns")
        
        # Debug info (can be hidden in production)
        with st.expander("🔧 Debug Info"):
            st.write(f"Data source: {'Database' if engine else 'Sample'}")
            st.write(f"DataFrame shape: {df.shape}")
            st.write(f"Date range: {df['invoice_date'].min()} to {df['invoice_date'].max()}")
        
        st.markdown("---")
        
        # Period Filter
        st.markdown("### 📅 Time Period")
        period_options = {
            "📊 Jan 2020 - Dec 2021": (pd.to_datetime("2020-01-01"), pd.to_datetime("2021-12-31")),
            "📅 2021 Full Year": (pd.to_datetime("2021-01-01"), pd.to_datetime("2021-12-31")),
            "🗓️ Q1 2021": (pd.to_datetime("2021-01-01"), pd.to_datetime("2021-03-31")),
            "⏰ Last 6 Months": (df['invoice_date'].max() - pd.Timedelta(days=180), df['invoice_date'].max())
        }
        
        selected_period = st.selectbox(
            "Select Time Period", 
            list(period_options.keys()),
            key="period_filter"
        )
        
        start_date, end_date = period_options[selected_period]
        filtered_df = filter_data(df, start_date, end_date)
        
        st.info(f"📊 Filtered to {len(filtered_df):,} records")
    
    # Calculate KPIs
    kpis = calculate_kpis(filtered_df, df)

    current_year = filtered_df['year'].max()
    last_year = current_year - 1
    # Sum total sales and profit for current and last year from full data
    total_sales_current = df[df['year'] == current_year]['total_sales'].sum() / 1e6  # in millions
    total_sales_last = df[df['year'] == last_year]['total_sales'].sum() / 1e6  # in millions
    total_profit_current = df[df['year'] == current_year]['operating_profit'].sum() / 1e6
    total_profit_last = df[df['year'] == last_year]['operating_profit'].sum() / 1e6
    # Calculate growth percentages with safe zero-division check
    sales_growth = ((total_sales_current - total_sales_last) / total_sales_last * 100) if total_sales_last > 0 else 0
    profit_growth = ((total_profit_current - total_profit_last) / total_profit_last * 100) if total_profit_last > 0 else 0
    # Format growth strings for KPI cards
    sales_growth_text = f"▲ {sales_growth:.1f}% dibanding tahun lalu" if sales_growth >= 0 else f"▼ {abs(sales_growth):.1f}% dibanding tahun lalu"
    profit_growth_text = f"▲ {profit_growth:.1f}% dibanding tahun lalu" if profit_growth >= 0 else f"▼ {abs(profit_growth):.1f}% dibanding tahun lalu"

    # Hitung total unit terjual untuk tahun ini dan tahun lalu
    total_units_current = df[df['year'] == current_year]['units_sold'].sum() / 1e6  # dalam juta
    total_units_last = df[df['year'] == last_year]['units_sold'].sum() / 1e6  # dalam juta
    # Hitung pertumbuhan unit terjual
    units_growth = ((total_units_current - total_units_last) / total_units_last * 100) if total_units_last > 0 else 0
    units_growth_text = f"▲ {units_growth:.1f}% dibanding tahun lalu" if units_growth >= 0 else f"▼ {abs(units_growth):.1f}% dibanding tahun lalu"
    # Hitung harga rata-rata per unit untuk tahun ini dan tahun lalu
    avg_price_current = df[df['year'] == current_year]['price_per_unit'].mean()
    avg_price_last = df[df['year'] == last_year]['price_per_unit'].mean()
    # Hitung pertumbuhan harga rata-rata per unit
    price_growth = ((avg_price_current - avg_price_last) / avg_price_last * 100) if avg_price_last > 0 else 0
    price_growth_text = f"▲ {price_growth:.1f}% dibanding tahun lalu" if price_growth >= 0 else f"▼ {abs(price_growth):.1f}% dibanding tahun lalu"
    
    # Section 1: Ringkasan Metrik (Executive Summary)
    st.markdown("""
    <div class="section-container">
        <div class="section-title">
            📈 Ringkasan Metrik
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        sales_alert = generate_performance_alert(kpis['total_sales'], kpis['historical_avg_sales'], "Sales")
        create_kpi_card(
            "Total Penjualan",
            f"$ {kpis['total_sales']:,.1f} M",
            sales_growth_text,
            sales_alert
        )
    with col2:
        profit_alert = generate_performance_alert(kpis['total_profit'], kpis['historical_avg_profit'], "Profit")
        create_kpi_card(
            "Total Keuntungan",
            f"$ {kpis['total_profit']:,.1f} M",
            profit_growth_text,
            profit_alert
        )
    
    with col3:
        create_kpi_card(
            "Unit Terjual",
            f"{kpis['total_units']:,.1f} Juta",
            units_growth_text  # Ganti dengan variabel pertumbuhan yang baru
        )
    with col4:
        create_kpi_card(
            "Harga Rata-rata per Unit",
            f"$ {kpis['avg_price']:,.0f}",
            price_growth_text  # Ganti dengan variabel pertumbuhan yang baru
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 2: Tren Penjualan (Sales Performance Trends)
    st.markdown("""
    <div class="section-container">
        <div class="section-title">
            📊 Tren Penjualan
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        monthly_data = filtered_df.groupby('month').agg({'total_sales': 'sum', 'operating_profit': 'sum'}).reset_index()
        prediction_result, _, _ = generate_sales_prediction(monthly_data, algorithm='random_forest')
        plot_sales_profit_trend(monthly_data, prediction_result)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        plot_multi_period_trend(filtered_df)
        st.markdown('</div>', unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    with col3:
        plot_annual_sales_profit(filtered_df)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        plot_units_trend(filtered_df)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 3: Wawasan Pengecer (Retailer Performance Analysis)
    st.markdown("""
    <div class="section-container">
        <div class="section-title">
            🏪 Wawasan Pengecer
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        plot_top_retailers(filtered_df)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Retailer alerts
        retailer_data = filtered_df.groupby('retailer_name').agg({'total_sales': 'sum'}).reset_index()
        retailer_alerts = generate_retailer_alert(retailer_data)
        for alert in retailer_alerts:
            alert_class = "alert-success" if "🏆" in alert else "alert-warning"
            st.markdown(f'<div class="alert {alert_class}">{alert}</div>', unsafe_allow_html=True)
    
    with col2:
        plot_retailer_performance(filtered_df)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 4: Analisis Produk & Gender (Product & Customer Insights)
    st.markdown("""
    <div class="section-container">
        <div class="section-title">
            👥 Analisis Produk & Gender
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        plot_product_category_performance(filtered_df)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        plot_gender_distribution(filtered_df)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        plot_gender_preferences(filtered_df)
        st.markdown('</div>', unsafe_allow_html=True)
    
    col4, col5, col6 = st.columns(3)
    with col4:
        plot_gender_trend(filtered_df)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col5:
        plot_units_per_category(filtered_df)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col6:
        plot_margin_per_category(filtered_df)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 5: Analisis Geografis (Geographic Market Analysis)
    st.markdown("""
    <div class="section-container">
        <div class="section-title">
            🌍 Analisis Geografis
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        plot_regional_sales(filtered_df)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Geographic insights
        regional_sales = filtered_df.groupby('region').agg({'total_sales': 'sum'}).reset_index()
        geo_insights = generate_geographic_insights(regional_sales)
        for insight in geo_insights:
            alert_class = "alert-info" if "🎯" in insight else "alert-warning"
            st.markdown(f'<div class="alert {alert_class}">{insight}</div>', unsafe_allow_html=True)
    
    with col2:
        plot_sales_map(filtered_df)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 6: Analisis Saluran Penjualan (Sales Channel Performance)
    st.markdown("""
    <div class="section-container">
        <div class="section-title">
            🛒 Analisis Saluran Penjualan
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        plot_sales_method_distribution(filtered_df)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        plot_sales_method_trend(filtered_df)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 7: Wawasan Strategis & Rekomendasi (Strategic Insights & Recommendations)
    st.markdown("""
    <div class="section-container">
        <div class="section-title">
            💡 Wawasan Strategis & Rekomendasi
        </div>
        <div class="insight-box">
            <div class="insight-title">🎯 Wawasan Bisnis Utama</div>
            <div class="insight-text">
                <strong>📊 Analitik Prediktif:</strong> Model Random Forest menunjukkan akurasi superior (MAE lebih rendah) dibandingkan Linear Regression untuk forecasting penjualan, memungkinkan perencanaan bisnis yang lebih handal.<br><br>
                
                <strong>🏪 Optimisasi Pengecer:</strong> Fokuskan pengembangan kemitraan pada pengecer berkinerja rendah dengan margin profit rendah. Implementasikan program dukungan terarah untuk meningkatkan conversion rate penjualan mereka.<br><br>
                
                <strong>👥 Segmentasi Pelanggan:</strong> Manfaatkan pola pembelian berbasis gender untuk mengembangkan kampanye marketing yang dipersonalisasi dan rekomendasi produk yang resonan dengan segmen pelanggan spesifik.<br><br>
                
                <strong>🌍 Ekspansi Pasar:</strong> Identifikasi dan prioritaskan wilayah geografis dengan potensi yang belum dimanfaatkan. Kembangkan strategi market entry untuk region dengan volume penjualan rendah namun potensi pertumbuhan tinggi.<br><br>
                
                <strong>📈 Strategi Saluran:</strong> Optimisasi sales channel mix berdasarkan tren performa. Pertimbangkan peningkatan investasi pada saluran berkinerja tinggi sambil memperbaiki yang berkinerja rendah.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 2rem; color: #7f8c8d; font-size: 0.9rem;">
        <hr style="border: 1px solid #ecf0f1; margin: 2rem 0;">
        🏃‍♂️ Dashboard Analisis Penjualan Adidas • Dibuat dengan Streamlit • Terakhir diperbarui: Real-time
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()