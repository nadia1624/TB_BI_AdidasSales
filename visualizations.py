import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Define consistent color palettes and styling
def get_theme_colors():
    """Get theme colors based on dark mode setting"""
    if st.session_state.get('dark_mode', False):
        return {
            'bg_color': 'rgba(45, 27, 105, 0.8)',
            'text_color': 'white',
            'grid_color': 'rgba(255, 255, 255, 0.25)'
        }
    else:
        return {
            'bg_color': 'rgba(255, 255, 255, 0.9)',
            'text_color': '#4a148c',
            'grid_color': 'rgba(74, 20, 140, 0.25)'
        }

def get_purple_palette():
    """Get consistent purple color palette"""
    return [
        '#5b21b6', '#7c3aed', '#a78bfa', '#c4b5fd', '#8b5cf6',
        '#6d28d9', '#7e22ce', '#9333ea', '#a855f7', '#c084fc'
    ]

def apply_chart_layout(fig, title_x='', title_y='', height=400, showlegend=True):
    """Apply consistent layout styling to charts"""
    theme = get_theme_colors()
    
    fig.update_layout(
        xaxis_title=title_x,
        yaxis_title=title_y,
        height=height,
        showlegend=showlegend,
        margin=dict(l=80, r=40, t=60, b=40),
        paper_bgcolor=theme['bg_color'],
        plot_bgcolor=theme['bg_color'],
        font=dict(family='Inter, sans-serif', size=14, color=theme['text_color']),
        xaxis=dict(
            gridcolor=theme['grid_color'],
            title_font_color=theme['text_color'],  # Tambahkan ini
            tickfont_color=theme['text_color']     # Tambahkan ini
        ),
        yaxis=dict(
            gridcolor=theme['grid_color'],
            title_font_color=theme['text_color'],  # Tambahkan ini
            tickfont_color=theme['text_color']     # Tambahkan ini
        ),
        yaxis2=dict(
            gridcolor=theme['grid_color'],
            title_font_color=theme['text_color'],  # Tambahkan ini
            tickfont_color=theme['text_color']     # Tambahkan ini
        ),
        legend=dict(
            x=0.5, 
            xanchor='center', 
            y=1.1, 
            orientation='h',
            font_color=theme['text_color']  # Tambahkan ini
        ) if showlegend else {}
    )
    return fig

def plot_sales_profit_trend(monthly_data, prediction_result):
    st.markdown('<div class="chart-container"><div class="chart-title">Monthly Sales and Profit</div>', unsafe_allow_html=True)
    
    # Prepare data for plotting
    monthly_data['total_sales_usd'] = monthly_data['total_sales'] / 1e6
    monthly_data['operating_profit_usd'] = monthly_data['operating_profit'] / 1e6

    theme = get_theme_colors()

    purple_palette = get_purple_palette()
    fig = go.Figure()

    # Sales line with markers and hover info
    fig.add_trace(go.Scatter(
        x=monthly_data['month'],
        y=monthly_data['total_sales_usd'],
        mode='lines+markers',
        name='Total Sales',
        line=dict(color=purple_palette[0], width=3),
        marker=dict(size=8, symbol='circle'),
        hovertemplate='Month: %{x}<br>Total Sales: $%{y:.2f}M<extra></extra>'
    ))

    # Profit line with markers and hover info
    fig.add_trace(go.Scatter(
        x=monthly_data['month'],
        y=monthly_data['operating_profit_usd'],
        mode='lines+markers',
        name='Total Profit',
        line=dict(color=purple_palette[1], width=3),
        marker=dict(size=8, symbol='circle'),
        hovertemplate='Month: %{x}<br>Total Profit: $%{y:.2f}M<extra></extra>',
        yaxis='y2'
    ))

    # Apply consistent styling
    fig = apply_chart_layout(fig, 'Month', 'Total Sales (Million $)')
    fig.update_layout(
        xaxis=dict(
            # title='Month',
            tickvals=list(range(1, 13)),
            ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        ),
        yaxis=dict(tickformat='.2f', tickprefix='$ '),
        yaxis2=dict(tickformat='.2f', tickprefix='$ ', overlaying='y', side='right'),
        font=dict(family='Inter, sans-serif', size=14, color=theme['text_color']),
        hovermode='x unified'
    )
    

    st.plotly_chart(fig, use_container_width=True)

    # Display prediction results if available
    # if isinstance(prediction_result, dict):
    #     prediction_usd = prediction_result['prediction'] / 1e6
    #     mae_usd = prediction_result['mae'] / 1e6
    #     st.markdown(f"""
    #         <div class="prediction-box">
    #             📊 <strong>Next Month Prediction:</strong> ${prediction_usd:.1f}M<br>
    #             📈 <strong>Trend:</strong> {prediction_result['trend'].upper()}<br>
    #             📉 <strong>MAE:</strong> ${mae_usd:.1f}M
    #         </div>
    #     """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def plot_multi_period_trend(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Multi-Period Sales Trend</div>', unsafe_allow_html=True)
    
    # Group by year and sum total sales
    yearly_data = filtered_df.groupby('year').agg({'total_sales': 'sum'}).reset_index()
    yearly_data['total_sales_usd'] = yearly_data['total_sales'] / 1e6 

    # Filter to include only 2020 and 2021
    yearly_data = yearly_data[yearly_data['year'].isin([2020, 2021])]

    purple_palette = get_purple_palette()
    fig = go.Figure()

    # Sales line with markers and hover info
    fig.add_trace(go.Scatter(
        x=yearly_data['year'],
        y=yearly_data['total_sales_usd'],
        mode='lines+markers',
        name='Total Sales',
        line=dict(color=purple_palette[0], width=3),
        marker=dict(size=8, symbol='circle'),
        hovertemplate='Year: %{x}<br>Total Sales: $%{y:.2f}M<extra></extra>'
    ))

    # Apply consistent styling
    fig = apply_chart_layout(fig, 'Year', 'Total Sales (Million $)', showlegend=False)
    fig.update_layout(
        xaxis=dict(tickmode='linear'),
        yaxis=dict(tickformat='.2f', tickprefix='$ '),
        hovermode='x unified'
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


def plot_annual_sales_profit(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Annual Sales and Profit</div>', unsafe_allow_html=True)
    
    # Group by year and sum total sales and operating profit
    annual_data = filtered_df.groupby('year').agg({'total_sales': 'sum', 'operating_profit': 'sum'}).reset_index()
    annual_data['total_sales_usd'] = annual_data['total_sales'] / 1e6 
    annual_data['operating_profit_usd'] = annual_data['operating_profit'] / 1e6 

    purple_palette = get_purple_palette()
    fig = go.Figure()

    # Add total sales area
    fig.add_trace(go.Scatter(
        x=annual_data['year'],
        y=annual_data['total_sales_usd'],
        mode='lines+markers',
        name='Total Sales',
        line=dict(color=purple_palette[0], width=3),
        marker=dict(size=8, symbol='circle'),
        hovertemplate='Year: %{x}<br>Total Sales: $%{y:.2f}M<extra></extra>',
        fill='tozeroy'
    ))

    # Add operating profit area
    fig.add_trace(go.Scatter(
        x=annual_data['year'],
        y=annual_data['operating_profit_usd'],
        mode='lines+markers',
        name='Operating Profit',
        line=dict(color=purple_palette[1], width=3),
        marker=dict(size=8, symbol='circle'),
        hovertemplate='Year: %{x}<br>Operating Profit: $%{y:.2f}M<extra></extra>',
        fill='tonexty'
    ))

    # Apply consistent styling
    fig = apply_chart_layout(fig, 'Year', 'Amount ($)')
    fig.update_layout(
        xaxis=dict(tickmode='linear'),
        yaxis_title='Amount ($)',
        yaxis_tickformat='.2f',
        yaxis_tickprefix='$ ',
        hovermode='x unified'
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


def plot_units_trend(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Units Sold Trend</div>', unsafe_allow_html=True)
    
    # Group by month and product category to sum units sold
    units_trend = filtered_df.groupby(['month', 'product_category']).agg({'units_sold': 'sum'}).reset_index()

    purple_palette = get_purple_palette()
    fig = go.Figure()

    # Add a line for each product category
    for i, category in enumerate(units_trend['product_category'].unique()):
        category_data = units_trend[units_trend['product_category'] == category]
        fig.add_trace(go.Scatter(
            x=category_data['month'],
            y=category_data['units_sold'],
            mode='lines+markers',
            name=category,
            line=dict(width=3, color=purple_palette[i % len(purple_palette)]),
            marker=dict(size=8, symbol='circle'),
            hovertemplate='Month: %{x}<br>Units Sold: %{y}<extra></extra>'
        ))

    # Apply consistent styling
    fig = apply_chart_layout(fig, 'Month', 'Units Sold')
    fig.update_layout(
        xaxis=dict(
            # title='Month',
            tickvals=list(range(1, 13)),
            ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        ),
        hovermode='x unified'
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def plot_top_retailers(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Top 10 Retailers</div>', unsafe_allow_html=True)
    
    # Prepare data: top 10 retailers by total sales
    top_retailers = filtered_df.groupby('retailer_name').agg({'total_sales': 'sum'}).nlargest(10, 'total_sales').reset_index()
    top_retailers['total_sales_usd'] = top_retailers['total_sales'] / 1e6 
    
    # Define a purple palette with distinct shades for up to 10 bars
    purple_palette = get_purple_palette()
    
    # Assign colors to bars, cycling the palette if needed
    colors = [purple_palette[i % len(purple_palette)] for i in range(len(top_retailers))]
    
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=top_retailers['total_sales_usd'],
        y=top_retailers['retailer_name'],
        orientation='h',
        marker=dict(color=colors),
        hovertemplate='Retailer: %{y}<br>Total Sales: $%{x:.2f}M<extra></extra>',
    ))

    # Apply consistent styling
    fig = apply_chart_layout(fig, 'Total Sales ($)', 'Retailer', showlegend=False)
    fig.update_layout(
        xaxis_tickformat='.2f',
        xaxis_tickprefix='$ ',
        yaxis=dict(autorange="reversed")
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


def plot_retailer_performance(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Retailer Performance</div>', unsafe_allow_html=True)
    
    retailer_perf = filtered_df.groupby('retailer_name').agg({'total_sales': 'sum', 'operating_margin': 'mean'}).reset_index()
    retailer_perf['total_sales_usd'] = retailer_perf['total_sales'] / 1e6 
    
    purple_palette = get_purple_palette()
    theme = get_theme_colors()
    
    fig = go.Figure()
    
    # Menggunakan warna yang lebih muda untuk marker
    fig.add_trace(go.Scatter(
        x=retailer_perf['total_sales_usd'],
        y=retailer_perf['operating_margin'],
        mode='markers',
        marker=dict(
            size=12,  # Ukuran marker yang lebih besar untuk visibilitas
            color=purple_palette[2],  # Menggunakan warna yang lebih muda
            opacity=0.95,
            line=dict(width=1, color='rgba(0, 0, 0, 0.6)')  # Garis tepi untuk kontras
        ),
        text=retailer_perf['retailer_name'],
        hovertemplate='Retailer: %{text}<br>Total Sales: $%{x:.2f}M<br>Operating Margin: %{y:.2f}%<extra></extra>'
    ))
    
    # Terapkan styling yang konsisten
    fig = apply_chart_layout(fig, 'Total Sales ($)', 'Operating Margin (%)', showlegend=False)
    fig.update_layout(
        xaxis_tickformat='.2f',
        xaxis_tickprefix='$ ',
        # xaxis=dict(title='Total Sales ($)'),
        # yaxis=dict(title='Operating Margin (%)'),
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


def plot_product_category_performance(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Product Category Performance</div>', unsafe_allow_html=True)
    
    cat_perf = filtered_df.groupby('product_category').agg({'total_sales': 'sum', 'operating_profit': 'sum'}).reset_index()
    cat_perf['total_sales_usd'] = cat_perf['total_sales'] / 1e6 
    cat_perf['operating_profit_usd'] = cat_perf['operating_profit'] / 1e6 
    
    purple_palette = get_purple_palette()
    fig = go.Figure()
    
    # Add sales bars
    fig.add_trace(go.Bar(
        x=cat_perf['product_category'],
        y=cat_perf['total_sales_usd'],
        name='Total Sales',
        marker=dict(color=purple_palette[0]),
        hovertemplate='Category: %{x}<br>Total Sales: $%{y:.2f}M<extra></extra>'
    ))
    
    # Add profit bars
    fig.add_trace(go.Bar(
        x=cat_perf['product_category'],
        y=cat_perf['operating_profit_usd'],
        name='Operating Profit',
        marker=dict(color=purple_palette[1]),
        hovertemplate='Category: %{x}<br>Operating Profit: $%{y:.2f}M<extra></extra>'
    ))
    
    # Apply consistent styling
    fig = apply_chart_layout(fig, 'Product Category', 'Amount ($)', height=350)
    fig.update_layout(
        yaxis_tickformat='.2f',
        yaxis_tickprefix='$ ',
        height=400,
        barmode='group'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    best_category = cat_perf.nlargest(1, 'total_sales_usd').iloc[0]
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def plot_gender_distribution(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Gender Distribution by Category</div>', unsafe_allow_html=True)
    
    gender_dist = filtered_df.groupby(['product_category', 'gender_type']).agg({'total_sales': 'sum'}).reset_index()
    gender_dist['total_sales_usd'] = gender_dist['total_sales'] / 1e6 
    
    purple_palette = get_purple_palette()
    fig = go.Figure()
    
    for i, gender in enumerate(gender_dist['gender_type'].unique()):
        gender_data = gender_dist[gender_dist['gender_type'] == gender]
        fig.add_trace(go.Bar(
            x=gender_data['product_category'],
            y=gender_data['total_sales_usd'],
            name=gender,
            marker=dict(color=purple_palette[i]),
            hovertemplate=f'Category: %{{x}}<br>Gender: {gender}<br>Total Sales: $%{{y:.2f}}M<extra></extra>'
        ))
    
    # Apply consistent styling
    fig = apply_chart_layout(fig, 'Product Category', 'Total Sales ($)', height=350)
    fig.update_layout(
        yaxis_tickformat='.2f',
        yaxis_tickprefix='$ ',
        height=400,
        barmode='stack'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def plot_gender_preferences(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Product Preferences by Gender</div>', unsafe_allow_html=True)
    
    # Alternative approach - create pivot table directly
    try:
        # Method 1: Using pivot_table
        gender_pref = filtered_df.pivot_table(
            index='gender_type',
            columns='product_category',
            values='total_sales',
            aggfunc='sum',
            fill_value=0
        ).reset_index()
        
        # Convert to millions for better readability
        numeric_columns = [col for col in gender_pref.columns if col != 'gender_type']
        for col in numeric_columns:
            gender_pref[col] = gender_pref[col] / 1e6
            
    except Exception as e:
        # Method 2: Manual groupby and reshape if pivot fails
        try:
            temp_df = filtered_df.groupby(['gender_type', 'product_category']).agg({'total_sales': 'sum'}).reset_index()
            gender_pref = temp_df.pivot(index='gender_type', columns='product_category', values='total_sales').fillna(0).reset_index()
            
            # Convert to millions
            numeric_columns = [col for col in gender_pref.columns if col != 'gender_type']
            for col in numeric_columns:
                gender_pref[col] = gender_pref[col] / 1e6
                
        except Exception as e2:
            st.warning(f"Unable to create gender preferences chart - data processing error: {str(e2)}")
            st.markdown('</div>', unsafe_allow_html=True)
            return
    
    # Get styling
    purple_palette = get_purple_palette()
    theme = get_theme_colors()
    
    # Get categories (theta values) - exclude gender_type column
    categories = [col for col in gender_pref.columns if col != 'gender_type']
    
    # Create figure with improved styling
    fig = go.Figure()
    
    # Add trace for each gender
    for i, gender in enumerate(gender_pref['gender_type'].unique()):
        gender_data = gender_pref[gender_pref['gender_type'] == gender]
        
        if len(gender_data) > 0:
            # Get values for this gender
            values = gender_data[categories].iloc[0].values
            
            # Convert hex color to RGB for fillcolor
            hex_color = purple_palette[i % len(purple_palette)]
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=gender,
                line=dict(
                    color=hex_color,
                    width=3
                ),
                fillcolor=f'rgba({r}, {g}, {b}, 0.25)',
                marker=dict(
                    size=8,
                    color=hex_color,
                    symbol='circle'
                ),
                hovertemplate='<b>%{fullData.name}</b><br>' +
                             'Category: %{theta}<br>' +
                             'Sales: $%{r:.2f}M<br>' +
                             '<extra></extra>'
            ))
    
    # Calculate max value for better axis scaling
    max_value = gender_pref[categories].max().max()
    axis_max = max_value * 1.1  # Add 10% padding
    
    # Update layout with improved styling
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                tickformat='.1f',
                tickprefix='$',
                ticksuffix='M',
                range=[0, axis_max],
                showline=True,
                linewidth=1,
                linecolor=theme['grid_color'],
                gridcolor=theme['grid_color'],
                gridwidth=1,
                tickfont=dict(size=11, color=theme['text_color'])
            ),
            angularaxis=dict(
                tickfont=dict(size=12, color=theme['text_color']),
                linecolor=theme['grid_color'],
                gridcolor=theme['grid_color']
            ),
            bgcolor=theme['bg_color']
        ),
        height=400,
        showlegend=True,
        paper_bgcolor=theme['bg_color'],
        font=dict(family='Inter, sans-serif', size=14, color=theme['text_color']),
        legend=dict(
            x=0.5, 
            xanchor='center', 
            y=-0.1, 
            orientation='h',
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(0,0,0,0)'
        ),
        margin=dict(l=60, r=60, t=60, b=80)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # # Add summary insights
    # if len(gender_pref) > 0:
    #     # Find top category for each gender
    #     insights = []
    #     for gender in gender_pref['gender_type'].unique():
    #         gender_data = gender_pref[gender_pref['gender_type'] == gender]
    #         if len(gender_data) > 0:
    #             top_category = gender_data[categories].iloc[0].idxmax()
    #             top_value = gender_data[categories].iloc[0].max()
    #             insights.append(f"<strong>{gender}:</strong> {top_category} (${top_value:.1f}M)")
        
    #     if insights:
    #         st.markdown(f"""
    #             <div class="alert-success">
    #                 🎯 <strong>Top Preferences:</strong><br>
    #                 {' • '.join(insights)}
    #             </div>
    #         """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
def plot_gender_trend(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Gender Purchase Trend</div>', unsafe_allow_html=True)
    
    gender_trend = filtered_df.groupby(['month', 'gender_type']).agg({'total_sales': 'sum'}).reset_index()
    gender_trend['total_sales_usd'] = gender_trend['total_sales'] / 1e6 
    
    purple_palette = get_purple_palette()
    fig = go.Figure()
    
    for i, gender in enumerate(gender_trend['gender_type'].unique()):
        gender_data = gender_trend[gender_trend['gender_type'] == gender]
        fig.add_trace(go.Scatter(
            x=gender_data['month'],
            y=gender_data['total_sales_usd'],
            mode='lines+markers',
            name=gender,
            line=dict(color=purple_palette[i], width=3),
            marker=dict(size=8, symbol='circle'),
            # Adjust hovertemplate to show uniform info, gender shown as trace name
            hovertemplate='Month: %{x}<br>Total Sales: $%{y:.2f}M<extra></extra>'
        ))
    
    # Apply consistent styling
    fig = apply_chart_layout(fig, 'Month', 'Total Sales ($)', height=350)
    fig.update_layout(
        xaxis=dict(
            # title='Month',
            tickvals=list(range(1, 13)),
            ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        ),
        yaxis_tickformat='.2f',
        yaxis_tickprefix='$ ',
        height=400,
        hovermode='x unified'  # critical for unified vertical hover line
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)



def plot_units_per_category(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Units Sold by Category</div>', unsafe_allow_html=True)
    
    units_cat = filtered_df.groupby('product_category').agg({'units_sold': 'sum'}).reset_index()
    
    purple_palette = get_purple_palette()
    colors = [purple_palette[i % len(purple_palette)] for i in range(len(units_cat))]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=units_cat['product_category'],
        y=units_cat['units_sold'],
        marker=dict(color=colors),
        hovertemplate='Category: %{x}<br>Units Sold: %{y}<extra></extra>'
    ))
    
    # Apply consistent styling
    fig = apply_chart_layout(fig, 'Product Category', 'Units Sold', height=350, showlegend=False)
    fig.update_layout(
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # top_category = units_cat.nlargest(1, 'units_sold').iloc[0]
    # st.markdown(f"""
    #     <div class="alert-success">
    #         🏆 Top Category: {top_category['product_category']} 
    #         ({top_category['units_sold']} units)
    #     </div>
    # """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def plot_margin_per_category(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Operating Margin by Category</div>', unsafe_allow_html=True)
    
    margin_cat = filtered_df.groupby('product_category').agg({'operating_margin': 'mean'}).reset_index()
    
    purple_palette = get_purple_palette()
    # Create gradient colors based on margin values
    colors = []
    for i, margin in enumerate(margin_cat['operating_margin']):
        intensity = (margin - margin_cat['operating_margin'].min()) / (margin_cat['operating_margin'].max() - margin_cat['operating_margin'].min())
        colors.append(purple_palette[min(int(intensity * len(purple_palette)), len(purple_palette)-1)])
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=margin_cat['product_category'],
        y=margin_cat['operating_margin'],
        marker=dict(color=colors),
        hovertemplate='Category: %{x}<br>Operating Margin: %{y:.2f}%<extra></extra>'
    ))
    
    # Apply consistent styling
    fig = apply_chart_layout(fig, 'Product Category', 'Operating Margin (%)', height=350, showlegend=False)
    fig.update_layout(
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # top_margin = margin_cat.nlargest(1, 'operating_margin').iloc[0]
    # st.markdown(f"""
    #     <div class="alert-success">
    #         💰 Highest Margin: {top_margin['product_category']} 
    #         ({top_margin['operating_margin']:.1f}%)
    #     </div>
    # """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def plot_regional_sales(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Sales by Region</div>', unsafe_allow_html=True)
    
    regional_sales = filtered_df.groupby('region').agg({'total_sales': 'sum'}).reset_index()
    regional_sales['total_sales_usd'] = regional_sales['total_sales'] / 1e6 
    
    purple_palette = get_purple_palette()
    # Create gradient colors based on sales values
    colors = []
    for i, sales in enumerate(regional_sales['total_sales_usd']):
        intensity = (sales - regional_sales['total_sales_usd'].min()) / (regional_sales['total_sales_usd'].max() - regional_sales['total_sales_usd'].min())
        colors.append(purple_palette[min(int(intensity * len(purple_palette)), len(purple_palette)-1)])
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=regional_sales['region'],
        y=regional_sales['total_sales_usd'],
        marker=dict(color=colors),
        hovertemplate='Region: %{x}<br>Total Sales: $%{y:.2f}M<extra></extra>'
    ))
    
    # Apply consistent styling
    fig = apply_chart_layout(fig, 'Region', 'Total Sales ($)', height=350, showlegend=False)
    fig.update_layout(
        yaxis_tickformat='.2f',
        height=400,
        yaxis_tickprefix='$ '
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
    
    # Get consistent styling
    purple_palette = get_purple_palette()
    theme = get_theme_colors()
    
    # Create custom purple color scale to match other visualizations
    purple_colorscale = [
        [0.0, purple_palette[3]],    # Lightest purple for lowest values
        [0.25, purple_palette[2]],   # Light purple
        [0.5, purple_palette[1]],    # Medium purple
        [0.75, purple_palette[0]],   # Dark purple
        [1.0, purple_palette[4]]     # Darkest purple for highest values
    ]
    
    # Create the map visualization with consistent purple theme
    fig = px.scatter_geo(
        city_sales, 
        lat='lat', 
        lon='lon', 
        size='total_sales_usd', 
        color='total_sales_usd',
        hover_name='city', 
        hover_data={'total_sales_usd': ':$.2f'},
        title='', 
        color_continuous_scale=purple_colorscale
    )
    
    # Update traces for better styling with smaller markers
    fig.update_traces(
        marker=dict(
            sizemode='diameter',
            sizeref=2. * max(city_sales['total_sales_usd']) / (12.**2),  # Reduced from 40 to 20
            sizemin=2,  # Reduced minimum size from 4 to 2
            line=dict(width=1, color='white')
        ),
        hovertemplate='<b>%{hovertext}</b><br>Total Sales: $%{marker.color:.2f}M<extra></extra>'
    )
    
    # Apply consistent layout styling
    fig.update_layout(
        geo=dict(
            scope='usa', 
            projection_type='albers usa',
            bgcolor=theme['bg_color'],
            showland=True,
            landcolor='rgba(243, 243, 243, 0.8)',
            coastlinecolor='rgba(204, 204, 204, 0.8)',
            showlakes=True,
            lakecolor='rgba(255, 255, 255, 0.8)'
        ),
        height=400,  # Consistent with other charts
        showlegend=False,
        paper_bgcolor=theme['bg_color'],
        font=dict(family='Inter, sans-serif', size=14, color=theme['text_color']),
        margin=dict(l=40, r=40, t=60, b=40),
        coloraxis_colorbar=dict(
            title="Sales ($M)",
            titlefont=dict(color=theme['text_color']),
            tickfont=dict(color=theme['text_color']),
            tickformat='.1f',
            tickprefix='$',
            ticksuffix='M'
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # top_city = city_sales.nlargest(1, 'total_sales_usd').iloc[0]
    # st.markdown(f"""
    #     <div class="alert-success">
    #         🌆 Top City: {top_city['city']} 
    #         (${top_city['total_sales_usd']:.1f}M)
    #     </div>
    # """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def plot_sales_method_distribution(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Sales by Method</div>', unsafe_allow_html=True)
    
    sales_method = filtered_df.groupby('sales_method').agg({'total_sales': 'sum'}).reset_index()
    sales_method['total_sales_usd'] = sales_method['total_sales'] / 1e6 
    
    purple_palette = get_purple_palette()
    theme = get_theme_colors()
    
    # Membuat pie chart dengan warna konsisten dari palet ungu
    fig = go.Figure(data=[go.Pie(
        labels=sales_method['sales_method'],
        values=sales_method['total_sales_usd'],
        marker=dict(colors=purple_palette[:len(sales_method)]),
        hoverinfo='label+percent+value',
        textinfo='percent',
        textfont=dict(family='Inter, sans-serif', size=14, color=theme['text_color']),
        hole=0.4
    )])
    
    fig.update_layout(
        height=350,
        paper_bgcolor=theme['bg_color'],
        font=dict(family='Inter, sans-serif', size=14, color=theme['text_color']),
        margin=dict(l=40, r=40, t=60, b=40),
        showlegend=True,
        legend=dict(x=0.5, xanchor='center', y=1.1, orientation='h')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # dominant_method = sales_method.nlargest(1, 'total_sales_usd').iloc[0]
    # st.markdown(f"""
    #     <div class="alert-success">
    #         🎯 Dominant Method: {dominant_method['sales_method']} 
    #         (${dominant_method['total_sales_usd']:.1f}M)
    #     </div>
    # """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def plot_sales_method_trend(filtered_df):
    st.markdown('<div class="chart-container"><div class="chart-title">Sales Method Trend</div>', unsafe_allow_html=True)
    
    # Prepare data
    method_trend = filtered_df.groupby(['month', 'sales_method']).agg({'total_sales': 'sum'}).reset_index()
    method_trend['total_sales_usd'] = method_trend['total_sales'] / 1e6 
    
    purple_palette = get_purple_palette()
    theme = get_theme_colors()
    
    fig = go.Figure()
    sales_methods = method_trend['sales_method'].unique()
    
    # Add one line for each sales method
    for i, method in enumerate(sales_methods):
        data = method_trend[method_trend['sales_method'] == method]
        fig.add_trace(go.Scatter(
            x=data['month'],
            y=data['total_sales_usd'],
            mode='lines+markers',
            name=method,
            line=dict(color=purple_palette[i % len(purple_palette)], width=3),
            marker=dict(size=8, symbol='circle'),
            hovertemplate=f'Month: %{{x}}<br>Method: {method}<br>Total Sales: $%{{y:.2f}}M<extra></extra>'
        ))
    
    # Apply consistent styling
    fig = apply_chart_layout(fig, 'Month', 'Total Sales (Million $)')
    fig.update_layout(
        xaxis=dict(
            tickvals=list(range(1, 13)),
            ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        ),
        yaxis=dict(tickformat='.2f', tickprefix='$ '),
        height=350,
        margin=dict(l=80, r=40, t=60, b=40),
        paper_bgcolor=theme['bg_color'],
        plot_bgcolor=theme['bg_color'],
        font=dict(family='Inter, sans-serif', size=14, color=theme['text_color']),
        legend=dict(x=0.5, xanchor='center', y=1.1, orientation='h'),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display method performance summary
    total_sales_by_method = method_trend.groupby('sales_method')['total_sales_usd'].sum().reset_index()
    best_method = total_sales_by_method.loc[total_sales_by_method['total_sales_usd'].idxmax()]
    total_methods = len(sales_methods)
    avg_sales = total_sales_by_method['total_sales_usd'].mean()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
