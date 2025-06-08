import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def plot_sales_profit_trend(monthly_data, prediction_result):
    st.markdown('<div class="chart-container"><div class="chart-title">Penjualan dan Profit Bulanan</div>', unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=monthly_data['month'], y=monthly_data['total_sales'], name='Total Penjualan', line=dict(color='#667eea')))
    fig.add_trace(go.Scatter(x=monthly_data['month'], y=monthly_data['operating_profit'], name='Total Keuntungan', line=dict(color='#764ba2'), yaxis='y2'))
    fig.update_layout(
        xaxis=dict(title='Bulan'),
        yaxis=dict(title='Total Penjualan (Rp)', tickformat='.0s', tickprefix='Rp ', titlefont=dict(color='#667eea'), tickfont=dict(color='#667eea')),
        yaxis2=dict(title='Total Keuntungan (Rp)', tickformat='.0s', tickprefix='Rp ', titlefont=dict(color='#764ba2'), tickfont=dict(color='#764ba2'), overlaying='y', side='right'),
        height=350, legend=dict(x=0.5, xanchor='center', y=1.1, orientation='h')
    )
    st.plotly_chart(fig, use_container_width=True)
    
    if isinstance(prediction_result, dict):
        st.markdown(f"""
            <div class="prediction-box">
                📊 <strong>Prediksi Bulan Depan:</strong> Rp {prediction_result['prediction']/1e6:.1f}M<br>
                📈 <strong>Tren:</strong> {prediction_result['trend'].upper()}<br>
                📉 <strong>MAE:</strong> Rp {prediction_result['mae']/1e6:.1f}M
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def plot_multi_period_trend(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Tren Penjualan Multi-Periode</div>', unsafe_allow_html=True)
    yearly_data = filtered_df.groupby('year').agg({'total_sales': 'sum'}).reset_index()
    fig = px.line(yearly_data, x='year', y='total_sales', title='', color_discrete_sequence=['#667eea'])
    fig.update_layout(
        xaxis_title='Tahun', yaxis_title='Total Penjualan (Rp)', yaxis_tickformat='.0s', yaxis_tickprefix='Rp ',
        height=350, showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def plot_annual_sales_profit(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Penjualan dan Profit Tahunan</div>', unsafe_allow_html=True)
    annual_data = filtered_df.groupby('year').agg({'total_sales': 'sum', 'operating_profit': 'sum'}).reset_index()
    fig = px.area(annual_data, x='year', y=['total_sales', 'operating_profit'], title='',
                  color_discrete_map={'total_sales': '#667eea', 'operating_profit': '#764ba2'})
    fig.update_layout(
        xaxis_title='Tahun', yaxis_title='Jumlah (Rp)', yaxis_tickformat='.0s', yaxis_tickprefix='Rp ',
        height=350, legend=dict(x=0.5, xanchor='center', y=1.1, orientation='h')
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def plot_units_trend(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Tren Unit Terjual</div>', unsafe_allow_html=True)
    units_trend = filtered_df.groupby(['month', 'product_category']).agg({'units_sold': 'sum'}).reset_index()
    fig = px.line(units_trend, x='month', y='units_sold', color='product_category', title='')
    fig.update_layout(
        xaxis_title='Bulan', yaxis_title='Unit Terjual', height=350,
        legend=dict(x=0.5, xanchor='center', y=1.1, orientation='h')
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def plot_top_retailers(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Top 10 Pengecer</div>', unsafe_allow_html=True)
    top_retailers = filtered_df.groupby('retailer_name').agg({'total_sales': 'sum'}).nlargest(10, 'total_sales').reset_index()
    fig = px.bar(top_retailers, x='total_sales', y='retailer_name', orientation='h', title='',
                 color='total_sales', color_continuous_scale='Viridis')
    fig.update_layout(
        xaxis_title='Total Penjualan (Rp)', yaxis_title='Pengecer', xaxis_tickformat='.0s', xaxis_tickprefix='Rp ',
        height=350, showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def plot_retailer_performance(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Performa Pengecer</div>', unsafe_allow_html=True)
    retailer_perf = filtered_df.groupby('retailer_name').agg({'total_sales': 'sum', 'operating_margin': 'mean'}).reset_index()
    fig = px.scatter(retailer_perf, x='total_sales', y='operating_margin', color='retailer_name', title='')
    fig.update_layout(
        xaxis_title='Total Penjualan (Rp)', yaxis_title='Operating Margin (%)', xaxis_tickformat='.0s', xaxis_tickprefix='Rp ',
        height=350, showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def plot_product_category_performance(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Performa Kategori Produk</div>', unsafe_allow_html=True)
    cat_perf = filtered_df.groupby('product_category').agg({'total_sales': 'sum', 'operating_profit': 'sum'}).reset_index()
    fig = px.bar(cat_perf, x='product_category', y=['total_sales', 'operating_profit'], barmode='group', title='')
    fig.update_layout(
        xaxis_title='Kategori Produk', yaxis_title='Jumlah (Rp)', yaxis_tickformat='.0s', yaxis_tickprefix='Rp ',
        height=350, legend=dict(x=0.5, xanchor='center', y=1.1, orientation='h')
    )
    st.plotly_chart(fig, use_container_width=True)
    
    best_category = cat_perf.nlargest(1, 'total_sales').iloc[0]
    st.markdown(f"""
        <div class="alert-success">
            🏅 Kategori Terbaik: {best_category['product_category']} 
            (Rp {best_category['total_sales']/1e6:.1f}M)
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def plot_gender_distribution(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Distribusi Gender per Kategori</div>', unsafe_allow_html=True)
    gender_dist = filtered_df.groupby(['product_category', 'gender_type']).agg({'total_sales': 'sum'}).reset_index()
    fig = px.bar(gender_dist, x='product_category', y='total_sales', color='gender_type', barmode='stack', title='')
    fig.update_layout(
        xaxis_title='Kategori Produk', yaxis_title='Total Penjualan (Rp)', yaxis_tickformat='.0s', yaxis_tickprefix='Rp ',
        height=350, legend=dict(x=0.5, xanchor='center', y=1.1, orientation='h')
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def plot_gender_preferences(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Preferensi Produk per Gender</div>', unsafe_allow_html=True)
    gender_pref = filtered_df.groupby(['gender_type', 'product_category']).agg({'total_sales': 'sum'}).unstack().fillna(0)
    gender_pref = gender_pref['total_sales'].reset_index()
    fig = go.Figure()
    for gender in gender_pref['gender_type']:
        fig.add_trace(go.Scatterpolar(
            r=gender_pref[gender_pref['gender_type'] == gender].iloc[0, 1:].values,
            theta=gender_pref.columns[1:],
            fill='toself',
            name=gender
        ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, tickformat='.0s', tickprefix='Rp ')),
        height=350, showlegend=True
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def plot_gender_trend(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Tren Pembelian Gender</div>', unsafe_allow_html=True)
    gender_trend = filtered_df.groupby(['month', 'gender_type']).agg({'total_sales': 'sum'}).reset_index()
    fig = px.line(gender_trend, x='month', y='total_sales', color='gender_type', title='')
    fig.update_layout(
        xaxis_title='Bulan', yaxis_title='Total Penjualan (Rp)', yaxis_tickformat='.0s', yaxis_tickprefix='Rp ',
        height=350, legend=dict(x=0.5, xanchor='center', y=1.1, orientation='h')
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def plot_units_per_category(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Unit Terjual per Kategori</div>', unsafe_allow_html=True)
    units_cat = filtered_df.groupby('product_category').agg({'units_sold': 'sum'}).reset_index()
    fig = px.bar(units_cat, x='product_category', y='units_sold', title='', color='product_category')
    fig.update_layout(
        xaxis_title='Kategori Produk', yaxis_title='Unit Terjual', height=350,
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    
    top_category = units_cat.nlargest(1, 'units_sold').iloc[0]
    st.markdown(f"""
        <div class="alert-success">
            🏆 Kategori Terlaris: {top_category['product_category']} 
            ({top_category['units_sold']} unit)
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def plot_margin_per_category(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Marjin Operasional per Kategori</div>', unsafe_allow_html=True)
    margin_cat = filtered_df.groupby('product_category').agg({'operating_margin': 'mean'}).reset_index()
    fig = px.bar(margin_cat, x='product_category', y='operating_margin', title='',
                 color='operating_margin', color_continuous_scale='Viridis')
    fig.update_layout(
        xaxis_title='Kategori Produk', yaxis_title='Marjin Operasional (%)', height=350,
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    
    top_margin = margin_cat.nlargest(1, 'operating_margin').iloc[0]
    st.markdown(f"""
        <div class="alert-success">
            💰 Marjin Tertinggi: {top_margin['product_category']} 
            ({top_margin['operating_margin']:.1f}%)
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def plot_regional_sales(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Penjualan per Wilayah</div>', unsafe_allow_html=True)
    regional_sales = filtered_df.groupby('region').agg({'total_sales': 'sum'}).reset_index()
    fig = px.bar(regional_sales, x='region', y='total_sales', title='',
                 color='total_sales', color_continuous_scale='Viridis')
    fig.update_layout(
        xaxis_title='Wilayah', yaxis_title='Total Penjualan (Rp)', yaxis_tickformat='.0s', yaxis_tickprefix='Rp ',
        height=350, showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def plot_sales_map(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Peta Penjualan</div>', unsafe_allow_html=True)
    city_sales = filtered_df.groupby('city').agg({'total_sales': 'sum'}).reset_index()
    city_coords = {
        'New York': (40.7128, -74.0060), 'Los Angeles': (34.0522, -118.2437),
        'Chicago': (41.8781, -87.6298), 'Houston': (29.7604, -95.3698),
        'Phoenix': (33.4484, -112.0740)
    }
    city_sales['lat'] = city_sales['city'].map(lambda x: city_coords.get(x, (0, 0))[0])
    city_sales['lon'] = city_sales['city'].map(lambda x: city_coords.get(x, (0, 0))[1])
    fig = px.scatter_geo(city_sales, lat='lat', lon='lon', size='total_sales', color='total_sales',
                         hover_name='city', hover_data=['total_sales'],
                         title='', color_continuous_scale='Viridis')
    fig.update_layout(
        geo=dict(scope='usa', projection_type='albers usa'),
        height=350, showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    
    top_city = city_sales.nlargest(1, 'total_sales').iloc[0]
    st.markdown(f"""
        <div class="alert-success">
            🌆 Kota Terlaris: {top_city['city']} 
            (Rp {top_city['total_sales']/1e6:.1f}M)
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def plot_sales_method_distribution(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Penjualan per Metode</div>', unsafe_allow_html=True)
    sales_method = filtered_df.groupby('sales_method').agg({'total_sales': 'sum'}).reset_index()
    fig = px.pie(sales_method, names='sales_method', values='total_sales', title='',
                 color_discrete_sequence=['#667eea', '#764ba2', '#ff9a9e'])
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)
    
    dominant_method = sales_method.nlargest(1, 'total_sales').iloc[0]
    st.markdown(f"""
        <div class="alert-success">
            🎯 Metode Dominan: {dominant_method['sales_method']} 
            ({dominant_method['total_sales']/1e6:.1f}M)
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def plot_sales_method_trend(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Tren Metode Penjualan</div>', unsafe_allow_html=True)
    method_trend = filtered_df.groupby(['month', 'sales_method']).agg({'total_sales': 'sum'}).reset_index()
    fig = px.line(method_trend, x='month', y='total_sales', color='sales_method', title='',
                  color_discrete_sequence=['#667eea', '#764ba2', '#ff9a9e'])
    fig.update_layout(
        xaxis_title='Bulan', yaxis_title='Total Penjualan (Rp)', yaxis_tickformat='.0s', yaxis_tickprefix='Rp ',
        height=350, legend=dict(x=0.5, xanchor='center', y=1.1, orientation='h')
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)