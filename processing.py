import pandas as pd

def filter_data(df, start_date, end_date):
    return df[(df['invoice_date'] >= start_date) & (df['invoice_date'] <= end_date)]

def calculate_kpis(filtered_df, full_df):
    total_sales = filtered_df['total_sales'].sum() / 1e6  # In millions
    total_profit = filtered_df['operating_profit'].sum() / 1e6  # In millions
    total_units = filtered_df['units_sold'].sum() / 1e6  # In millions
    avg_price = filtered_df['price_per_unit'].mean()
    
    historical_avg_sales = full_df['total_sales'].sum() / len(full_df['month'].unique()) / 1e6
    historical_avg_profit = full_df['operating_profit'].sum() / len(full_df['month'].unique()) / 1e6
    
    return {
        'total_sales': total_sales,
        'total_profit': total_profit,
        'total_units': total_units,
        'avg_price': avg_price,
        'historical_avg_sales': historical_avg_sales,
        'historical_avg_profit': historical_avg_profit
    }