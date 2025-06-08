import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def plot_sales_profit_trend(monthly_data, prediction_result):
    st.markdown('<div class="chart-container"><div class="chart-title">Monthly Sales and Profit</div>', unsafe_allow_html=True)
    monthly_data['total_sales_usd'] = monthly_data['total_sales'] / 1e6 
    monthly_data['operating_profit_usd'] = monthly_data['operating_profit'] / 1e6 
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=monthly_data['month'], y=monthly_data['total_sales_usd'], name='Total Sales', line=dict(color='#667eea')))
    fig.add_trace(go.Scatter(x=monthly_data['month'], y=monthly_data['operating_profit_usd'], name='Total Profit', line=dict(color='#764ba2'), yaxis='y2'))
    fig.update_layout(
        xaxis=dict(title='Month'),
        yaxis=dict(title='Total Sales ($)', tickformat='.2f', tickprefix='$ ', titlefont=dict(color='#667eea'), tickfont=dict(color='#667eea')),
        yaxis2=dict(title='Total Profit ($)', tickformat='.2f', tickprefix='$ ', titlefont=dict(color='#764ba2'), tickfont=dict(color='#764ba2'), overlaying='y', side='right'),
        height=350, legend=dict(x=0.5, xanchor='center', y=1.1, orientation='h')
    )
    st.plotly_chart(fig, use_container_width=True)
    
    if isinstance(prediction_result, dict):
        prediction_usd = prediction_result['prediction'] / 1e6 
        mae_usd = prediction_result['mae'] / 1e6 
        st.markdown(f"""
            <div class="prediction-box">
                📊 <strong>Next Month Prediction:</strong> ${prediction_usd:.1f}M<br>
                📈 <strong>Trend:</strong> {prediction_result['trend'].upper()}<br>
                📉 <strong>MAE:</strong> ${mae_usd:.1f}M
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def plot_multi_period_trend(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Multi-Period Sales Trend</div>', unsafe_allow_html=True)
    yearly_data = filtered_df.groupby('year').agg({'total_sales': 'sum'}).reset_index()
    yearly_data['total_sales_usd'] = yearly_data['total_sales'] / 1e6 
    fig = px.line(yearly_data, x='year', y='total_sales_usd', title='', color_discrete_sequence=['#667eea'])
    fig.update_layout(
        xaxis_title='Year', yaxis_title='Total Sales ($)', yaxis_tickformat='.2f', yaxis_tickprefix='$ ',
        height=350, showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def plot_annual_sales_profit(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Annual Sales and Profit</div>', unsafe_allow_html=True)
    annual_data = filtered_df.groupby('year').agg({'total_sales': 'sum', 'operating_profit': 'sum'}).reset_index()
    annual_data['total_sales_usd'] = annual_data['total_sales'] / 1e6 
    annual_data['operating_profit_usd'] = annual_data['operating_profit'] / 1e6 
    fig = px.area(annual_data, x='year', y=['total_sales_usd', 'operating_profit_usd'], title='',
                  color_discrete_map={'total_sales_usd': '#667eea', 'operating_profit_usd': '#764ba2'})
    fig.update_layout(
        xaxis_title='Year', yaxis_title='Amount ($)', yaxis_tickformat='.2f', yaxis_tickprefix='$ ',
        height=350, legend=dict(x=0.5, xanchor='center', y=1.1, orientation='h')
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def plot_units_trend(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Units Sold Trend</div>', unsafe_allow_html=True)
    units_trend = filtered_df.groupby(['month', 'product_category']).agg({'units_sold': 'sum'}).reset_index()
    fig = px.line(units_trend, x='month', y='units_sold', color='product_category', title='')
    fig.update_layout(
        xaxis_title='Month', yaxis_title='Units Sold', height=350,
        legend=dict(x=0.5, xanchor='center', y=1.1, orientation='h')
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def plot_top_retailers(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Top 10 Retailers</div>', unsafe_allow_html=True)
    top_retailers = filtered_df.groupby('retailer_name').agg({'total_sales': 'sum'}).nlargest(10, 'total_sales').reset_index()
    top_retailers['total_sales_usd'] = top_retailers['total_sales'] / 1e6 
    fig = px.bar(top_retailers, x='total_sales_usd', y='retailer_name', orientation='h', title='',
                 color='total_sales_usd', color_continuous_scale='Viridis')
    fig.update_layout(
        xaxis_title='Total Sales ($)', yaxis_title='Retailer', xaxis_tickformat='.2f', xaxis_tickprefix='$ ',
        height=350, showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def plot_retailer_performance(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Retailer Performance</div>', unsafe_allow_html=True)
    retailer_perf = filtered_df.groupby('retailer_name').agg({'total_sales': 'sum', 'operating_margin': 'mean'}).reset_index()
    retailer_perf['total_sales_usd'] = retailer_perf['total_sales'] / 1e6 
    fig = px.scatter(retailer_perf, x='total_sales_usd', y='operating_margin', color='retailer_name', title='')
    fig.update_layout(
        xaxis_title='Total Sales ($)', yaxis_title='Operating Margin (%)', xaxis_tickformat='.2f', xaxis_tickprefix='$ ',
        height=350, showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def plot_product_category_performance(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Product Category Performance</div>', unsafe_allow_html=True)
    cat_perf = filtered_df.groupby('product_category').agg({'total_sales': 'sum', 'operating_profit': 'sum'}).reset_index()
    cat_perf['total_sales_usd'] = cat_perf['total_sales'] / 1e6 
    cat_perf['operating_profit_usd'] = cat_perf['operating_profit'] / 1e6 
    fig = px.bar(cat_perf, x='product_category', y=['total_sales_usd', 'operating_profit_usd'], barmode='group', title='')
    fig.update_layout(
        xaxis_title='Product Category', yaxis_title='Amount ($)', yaxis_tickformat='.2f', yaxis_tickprefix='$ ',
        height=350, legend=dict(x=0.5, xanchor='center', y=1.1, orientation='h')
    )
    st.plotly_chart(fig, use_container_width=True)
    
    best_category = cat_perf.nlargest(1, 'total_sales_usd').iloc[0]
    st.markdown(f"""
        <div class="alert-success">
            🏅 Best Category: {best_category['product_category']} 
            (${best_category['total_sales_usd']:.1f}M)
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def plot_gender_distribution(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Gender Distribution by Category</div>', unsafe_allow_html=True)
    gender_dist = filtered_df.groupby(['product_category', 'gender_type']).agg({'total_sales': 'sum'}).reset_index()
    gender_dist['total_sales_usd'] = gender_dist['total_sales'] / 1e6 
    fig = px.bar(gender_dist, x='product_category', y='total_sales_usd', color='gender_type', barmode='stack', title='')
    fig.update_layout(
        xaxis_title='Product Category', yaxis_title='Total Sales ($)', yaxis_tickformat='.2f', yaxis_tickprefix='$ ',
        height=350, legend=dict(x=0.5, xanchor='center', y=1.1, orientation='h')
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def plot_gender_preferences(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Product Preferences by Gender</div>', unsafe_allow_html=True)
    gender_pref = filtered_df.groupby(['gender_type', 'product_category']).agg({'total_sales': 'sum'}).unstack().fillna(0)
    gender_pref = gender_pref['total_sales'].reset_index()
    gender_pref.iloc[:, 1:] = gender_pref.iloc[:, 1:] / 1e6 
    fig = go.Figure()
    for gender in gender_pref['gender_type']:
        fig.add_trace(go.Scatterpolar(
            r=gender_pref[gender_pref['gender_type'] == gender].iloc[0, 1:].values,
            theta=gender_pref.columns[1:],
            fill='toself',
            name=gender
        ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, tickformat='.2f', tickprefix='$ ')),
        height=350, showlegend=True
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def plot_gender_trend(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Gender Purchase Trend</div>', unsafe_allow_html=True)
    gender_trend = filtered_df.groupby(['month', 'gender_type']).agg({'total_sales': 'sum'}).reset_index()
    gender_trend['total_sales_usd'] = gender_trend['total_sales'] / 1e6 
    fig = px.line(gender_trend, x='month', y='total_sales_usd', color='gender_type', title='')
    fig.update_layout(
        xaxis_title='Month', yaxis_title='Total Sales ($)', yaxis_tickformat='.2f', yaxis_tickprefix='$ ',
        height=350, legend=dict(x=0.5, xanchor='center', y=1.1, orientation='h')
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def plot_units_per_category(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Units Sold by Category</div>', unsafe_allow_html=True)
    units_cat = filtered_df.groupby('product_category').agg({'units_sold': 'sum'}).reset_index()
    fig = px.bar(units_cat, x='product_category', y='units_sold', title='', color='product_category')
    fig.update_layout(
        xaxis_title='Product Category', yaxis_title='Units Sold', height=350,
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    
    top_category = units_cat.nlargest(1, 'units_sold').iloc[0]
    st.markdown(f"""
        <div class="alert-success">
            🏆 Top Category: {top_category['product_category']} 
            ({top_category['units_sold']} units)
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def plot_margin_per_category(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Operating Margin by Category</div>', unsafe_allow_html=True)
    margin_cat = filtered_df.groupby('product_category').agg({'operating_margin': 'mean'}).reset_index()
    fig = px.bar(margin_cat, x='product_category', y='operating_margin', title='',
                 color='operating_margin', color_continuous_scale='Viridis')
    fig.update_layout(
        xaxis_title='Product Category', yaxis_title='Operating Margin (%)', height=350,
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    
    top_margin = margin_cat.nlargest(1, 'operating_margin').iloc[0]
    st.markdown(f"""
        <div class="alert-success">
            💰 Highest Margin: {top_margin['product_category']} 
            ({top_margin['operating_margin']:.1f}%)
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def plot_regional_sales(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Sales by Region</div>', unsafe_allow_html=True)
    regional_sales = filtered_df.groupby('region').agg({'total_sales': 'sum'}).reset_index()
    regional_sales['total_sales_usd'] = regional_sales['total_sales'] / 1e6 
    fig = px.bar(regional_sales, x='region', y='total_sales_usd', title='',
                 color='total_sales_usd', color_continuous_scale='Viridis')
    fig.update_layout(
        xaxis_title='Region', yaxis_title='Total Sales ($)', yaxis_tickformat='.2f', yaxis_tickprefix='$ ',
        height=350, showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def plot_sales_map(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Sales Map</div>', unsafe_allow_html=True)
    city_sales = filtered_df.groupby('city').agg({'total_sales': 'sum'}).reset_index()
    city_sales['total_sales_usd'] = city_sales['total_sales'] / 1e6 
    
    city_coords = {
        'Philadelphia': (39.9526, -75.1652), 'Providence': (41.8236, -71.4222),
        'New York': (40.7128, -74.0060), 'Wilmington': (39.7392, -75.5397),
        'Manchester': (42.9956, -71.4548), 'Hartford': (41.7658, -72.6734),
        'Charleston': (32.7765, -79.9311), 'Baltimore': (39.2904, -76.6122),
        'Boston': (42.3601, -71.0589), 'Portland': (43.6615, -70.2553),
        'Burlington': (44.4759, -73.2121), 'Newark': (40.7357, -74.1724),
        'Albany': (42.6526, -73.7562), 'Columbus': (39.9612, -82.9988),
        'Detroit': (42.3314, -83.0458), 'Fargo': (46.8772, -96.7898),
        'Sioux Falls': (43.5343, -96.7311), 'St. Louis': (38.6270, -90.1994),
        'Des Moines': (41.5868, -93.6250), 'Indianapolis': (39.7684, -86.1581),
        'Milwaukee': (43.0389, -87.9065), 'Chicago': (41.8781, -87.6298),
        'Minneapolis': (44.9778, -93.2650), 'Omaha': (41.2524, -95.9980),
        'Wichita': (37.6872, -97.3301), 'Richmond': (37.5407, -77.4360),
        'Atlanta': (33.7490, -84.3880), 'Orlando': (28.5383, -81.3792),
        'Miami': (25.7617, -80.1918), 'Louisville': (38.2527, -85.7585),
        'Charlotte': (35.2271, -80.8431), 'Salt Lake City': (40.7608, -111.8910),
        'Anchorage': (61.2181, -149.9003), 'Cheyenne': (41.1399, -104.8202),
        'Los Angeles': (34.0522, -118.2437), 'Seattle': (47.6062, -122.3321),
        'Dallas': (32.7767, -96.7970), 'Knoxville': (35.9606, -83.9207),
        'Birmingham': (33.5186, -86.8104), 'Jackson': (32.2988, -90.1848),
        'Billings': (45.7833, -108.5007), 'New Orleans': (29.9511, -90.0715),
        'Houston': (29.7604, -95.3698), 'Oklahoma City': (35.4676, -97.5164),
        'Little Rock': (34.7465, -92.2896), 'San Francisco': (37.7749, -122.4194),
        'Boise': (43.6150, -116.2023), 'Honolulu': (21.3069, -157.8583),
        'Albuquerque': (35.0845, -106.6504), 'Phoenix': (33.4484, -112.0740),
        'Denver': (39.7392, -104.9903), 'Las Vegas': (36.1699, -115.1398)
    }
    
    city_sales['lat'] = city_sales['city'].map(lambda x: city_coords.get(x, (0, 0))[0])
    city_sales['lon'] = city_sales['city'].map(lambda x: city_coords.get(x, (0, 0))[1])
    fig = px.scatter_geo(city_sales, lat='lat', lon='lon', size='total_sales_usd', color='total_sales_usd',
                         hover_name='city', hover_data=['total_sales_usd'],
                         title='', color_continuous_scale='Viridis')
    fig.update_layout(
        geo=dict(scope='usa', projection_type='albers usa'),
        height=350, showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    
    top_city = city_sales.nlargest(1, 'total_sales_usd').iloc[0]
    st.markdown(f"""
        <div class="alert-success">
            🌆 Top City: {top_city['city']} 
            (${top_city['total_sales_usd']:.1f}M)
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def plot_sales_method_distribution(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Sales by Method</div>', unsafe_allow_html=True)
    sales_method = filtered_df.groupby('sales_method').agg({'total_sales': 'sum'}).reset_index()
    sales_method['total_sales_usd'] = sales_method['total_sales'] / 1e6 
    fig = px.pie(sales_method, names='sales_method', values='total_sales_usd', title='',
                 color_discrete_sequence=['#667eea', '#764ba2', '#ff9a9e'])
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)
    
    dominant_method = sales_method.nlargest(1, 'total_sales_usd').iloc[0]
    st.markdown(f"""
        <div class="alert-success">
            🎯 Dominant Method: {dominant_method['sales_method']} 
            (${dominant_method['total_sales_usd']:.1f}M)
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def plot_sales_method_trend(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Sales Method Trend</div>', unsafe_allow_html=True)
    method_trend = filtered_df.groupby(['month', 'sales_method']).agg({'total_sales': 'sum'}).reset_index()
    method_trend['total_sales_usd'] = method_trend['total_sales'] / 1e6 
    fig = px.line(method_trend, x='month', y='total_sales_usd', color='sales_method', title='',
                  color_discrete_sequence=['#667eea', '#764ba2', '#ff9a9e'])
    fig.update_layout(
        xaxis_title='Month', yaxis_title='Total Sales ($)', yaxis_tickformat='.2f', yaxis_tickprefix='$ ',
        height=350, legend=dict(x=0.5, xanchor='center', y=1.1, orientation='h')
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)