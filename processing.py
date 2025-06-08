import pandas as pd

def filter_data(df, start_date, end_date):
    print("Filter range:", start_date, "to", end_date)
    print("Original df shape:", df.shape)
    filtered_df = df[(df['invoice_date'] >= start_date) & (df['invoice_date'] <= end_date)]
    print("Filtered df shape:", filtered_df.shape)
    return filtered_df

def calculate_kpis(filtered_df, full_df):
    print("price_per_unit sample:", filtered_df['price_per_unit'].head().to_list())
    print("price_per_unit mean (USD):", filtered_df['price_per_unit'].dropna().mean())
    
    total_sales = filtered_df['total_sales'].sum() / 1e6  # USD, in millions
    total_profit = filtered_df['operating_profit'].sum() / 1e6  # USD, in millions
    total_units = filtered_df['units_sold'].sum() / 1e6  # Millions
    
    avg_price = 0
    if 'price_per_unit' in filtered_df.columns and filtered_df['price_per_unit'].notnull().any():
        avg_price = filtered_df['price_per_unit'].dropna().mean()  # USD
    
    historical_avg_sales = full_df['total_sales'].sum() / len(full_df['month'].unique()) / 1e6  # USD, in millions
    historical_avg_profit = full_df['operating_profit'].sum() / len(full_df['month'].unique()) / 1e6  # USD, in millions
    
    return {
        'total_sales': total_sales,
        'total_profit': total_profit,
        'total_units': total_units,
        'avg_price': avg_price,
        'historical_avg_sales': historical_avg_sales,
        'historical_avg_profit': historical_avg_profit
    }