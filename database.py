import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import streamlit as st

def connect_to_database():
    try:
        engine = create_engine('postgresql+psycopg2://postgres:nadia1624@localhost:5432/DW_Adidas')
        st.success("✅ Connected to DW_Adidas database!")
        return engine
    except Exception as e:
        st.error(f"❌ Database connection failed: {str(e)}")
        st.warning("🔧 Using sample data...")
        return None

@st.cache_data
def load_data(_engine=None):
    if _engine:
        query = """
        SELECT 
            fs.sales_id, dr.retailer_name, dd.year, dd.month, dd.quarter, dd.day, dd.weekday, 
            dl.region, dl.state, dl.city, dp.product_category, 
            COALESCE(dp.price_per_unit, 100) as price_per_unit, 
            dg.gender_type, dsm.sales_method, fs.units_sold, fs.total_sales, fs.operating_profit, fs.operating_margin,
            dd.invoice_date
        FROM fact_sales fs
        JOIN dim_retailer dr ON fs.retailer_id = dr.retailer_id
        JOIN dim_date dd ON fs.date_id = dd.date_id
        JOIN dim_location dl ON fs.location_id = dl.location_id
        JOIN dim_product dp ON fs.product_id = dp.product_id
        JOIN dim_gender dg ON fs.gender_id = dg.gender_id
        JOIN dim_sales_method dsm ON fs.sales_method_id = dsm.sales_method_id
        """
        try:
            df = pd.read_sql(query, _engine)
            df['invoice_date'] = pd.to_datetime(df['invoice_date'])
            df['price_per_unit'] = pd.to_numeric(df['price_per_unit'], errors='coerce').fillna(100)  # USD default
            return df
        except Exception as e:
            st.error(f"Failed to load data: {str(e)}")
    
    # Sample data in USD
    np.random.seed(42)
    dates = pd.date_range('2020-01-01', '2021-12-31', freq='D')
    sample_size = 1000
    df = pd.DataFrame({
        'sales_id': range(sample_size),
        'retailer_name': np.random.choice(['West Gear', 'Foot Locker', 'Sports Direct', 'Kohl\'s', 'Amazon'], sample_size),
        'year': np.random.choice([2020, 2021], sample_size),
        'month': np.random.randint(1, 13, sample_size),
        'quarter': np.random.choice(['Q1', 'Q2', 'Q3', 'Q4'], sample_size),
        'day': np.random.randint(1, 32, sample_size),
        'weekday': np.random.choice(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], sample_size),
        'region': np.random.choice(['West', 'Northeast', 'Southeast', 'South', 'Midwest'], sample_size),
        'state': np.random.choice(['California', 'New York', 'Texas', 'Florida', 'Illinois'], sample_size),
        'city': np.random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'], sample_size),
        'product_category': np.random.choice(['Men\'s Street Footwear', 'Women\'s Apparel', 'Men\'s Athletic Footwear'], sample_size),
        'price_per_unit': np.random.uniform(50, 200, sample_size),  # USD
        'gender_type': np.random.choice(['Men', 'Women'], sample_size),
        'sales_method': np.random.choice(['In-store', 'Online', 'Outlet'], sample_size),
        'units_sold': np.random.randint(1, 100, sample_size),
        'total_sales': np.random.uniform(1000, 50000, sample_size),  # USD
        'operating_profit': np.random.uniform(200, 15000, sample_size),  # USD
        'operating_margin': np.random.uniform(10, 50, sample_size),
        'invoice_date': np.random.choice(dates, sample_size)
    })
    df['invoice_date'] = pd.to_datetime(df['invoice_date'])
    return df