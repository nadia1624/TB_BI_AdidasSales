import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

def generate_sales_prediction(monthly_data, algorithm='random_forest'):
    if len(monthly_data) < 3:
        return "Data tidak cukup untuk prediksi", None, None
    
    X = np.array(range(len(monthly_data))).reshape(-1, 1)
    y = monthly_data['total_sales'].values
    
    train_size = int(0.8 * len(X))
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]
    
    if algorithm == 'linear':
        model = LinearRegression()
    else:
        model = RandomForestRegressor(n_estimators=100, random_state=42)
    
    model.fit(X_train, y_train)
    y_pred_test = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred_test)
    
    next_month_pred = model.predict([[len(monthly_data)]])[0]
    
    lr_model = LinearRegression().fit(X, y)
    slope = lr_model.coef_[0]
    trend = "meningkat" if slope > 0 else "menurun" if slope < 0 else "stabil"
    trend_color = "success" if slope > 0 else "danger" if slope < 0 else "warning"
    
    return {
        'prediction': next_month_pred,
        'trend': trend,
        'trend_color': trend_color,
        'mae': mae
    }, model, lr_model

def generate_performance_alert(current_value, historical_avg, metric_name):
    if current_value > historical_avg * 1.1:
        return f"🟢 {metric_name} saat ini {((current_value/historical_avg - 1) * 100):.1f}% di atas rata-rata historis"
    elif current_value < historical_avg * 0.9:
        return f"🔴 {metric_name} saat ini {((1 - current_value/historical_avg) * 100):.1f}% di bawah rata-rata historis"
    else:
        return f"🟡 {metric_name} dalam rentang normal"

def generate_retailer_alert(retailer_data):
    alerts = []
    top_performer = retailer_data.nlargest(1, 'total_sales').iloc[0]
    worst_performer = retailer_data.nsmallest(1, 'total_sales').iloc[0]
    alerts.append(f"🏆 Top Performer: {top_performer['retailer_name']} dengan penjualan $ {top_performer['total_sales']/1e6:.1f}M")
    alerts.append(f"⚠️ Perlu Perhatian: {worst_performer['retailer_name']} dengan penjualan ${worst_performer['total_sales']/1e6:.1f}M")
    return alerts

def generate_prediction_alert(prediction_result):
    alerts = []
    if isinstance(prediction_result, dict):
        prediction_usd = prediction_result['prediction'] / 1e6
        mae_usd = prediction_result['mae'] / 1e6
        trend = prediction_result['trend'].upper()
        
        alerts.append(f"📊 Next Month Prediction: ${prediction_usd:.1f}M")
        alerts.append(f"📈 Trend: {trend}")
        alerts.append(f"📉 MAE: ${mae_usd:.1f}M")
    
    return alerts

def generate_category_alert(category_data):
    alerts = []
    top_category = category_data.nlargest(1, 'total_sales_usd').iloc[0]
    worst_category = category_data.nsmallest(1, 'total_sales_usd').iloc[0]
    
    alerts.append(f"🏅 Best Category: {top_category['product_category']} (${top_category['total_sales_usd']:.1f}M)")
    alerts.append(f"⚠️ Needs Attention: {worst_category['product_category']} (${worst_category['total_sales_usd']:.1f}M)")
    
    return alerts

def generate_units_category_alert(units_category_data):
    alerts = []
    top_category = units_category_data.nlargest(1, 'units_sold').iloc[0]
    worst_category = units_category_data.nsmallest(1, 'units_sold').iloc[0]
    
    alerts.append(f"🏆 Top Category: {top_category['product_category']} ({top_category['units_sold']} units)")
    
    return alerts

def generate_margin_category_alert(margin_category_data):
    alerts = []
    top_margin = margin_category_data.nlargest(1, 'operating_margin').iloc[0]
    worst_margin = margin_category_data.nsmallest(1, 'operating_margin').iloc[0]
    
    alerts.append(f"💰 Highest Margin: {top_margin['product_category']} ({top_margin['operating_margin']:.1f}%)")
    alerts.append(f"⚠️ Lowest Margin: {worst_margin['product_category']} ({worst_margin['operating_margin']:.1f}%)")
    
    return alerts

def generate_city_alert(city_data):
    alerts = []
    top_city = city_data.nlargest(1, 'total_sales_usd').iloc[0]
    worst_city = city_data.nsmallest(1, 'total_sales_usd').iloc[0]
    
    alerts.append(f"🌆 Top City: {top_city['city']} (${top_city['total_sales_usd']:.1f}M)")
    alerts.append(f"⚠️ Needs Focus: {worst_city['city']} (${worst_city['total_sales_usd']:.1f}M)")
    
    return alerts

def generate_sales_method_alert(sales_method_data):
    alerts = []
    top_method = sales_method_data.nlargest(1, 'total_sales_usd').iloc[0]
    worst_method = sales_method_data.nsmallest(1, 'total_sales_usd').iloc[0]
    
    alerts.append(f"🎯 Dominant Method: {top_method['sales_method']} (${top_method['total_sales_usd']:.1f}M)")
    alerts.append(f"⚠️ Underperforming: {worst_method['sales_method']} (${worst_method['total_sales_usd']:.1f}M)")
    
    return alerts


def generate_gender_preference_alert(gender_pref, categories):
    alerts = []
    if len(gender_pref) > 0:
        # Find top category for each gender
        for gender in gender_pref['gender_type'].unique():
            gender_data = gender_pref[gender_pref['gender_type'] == gender]
            if len(gender_data) > 0:
                top_category = gender_data[categories].iloc[0].idxmax()
                top_value = gender_data[categories].iloc[0].max()
                alerts.append(f"🎯 Top Preference {gender}: {top_category} (${top_value:.1f}M)")
    
    return alerts

def generate_geographic_insights(regional_data):
    insights = []
    total_sales = regional_data['total_sales'].sum()
    for _, row in regional_data.iterrows():
        percentage = (row['total_sales'] / total_sales) * 100
        if percentage > 30:
            insights.append(f"🎯 {row['region']}: Wilayah dominan ({percentage:.1f}% dari total penjualan)")
        elif percentage < 10:
            insights.append(f"📈 {row['region']}: Potensi ekspansi ({percentage:.1f}% dari total penjualan)")
    return insights