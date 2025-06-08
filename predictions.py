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
    alerts.append(f"🏆 Top Performer: {top_performer['retailer_name']} dengan penjualan Rp {top_performer['total_sales']/1e6:.1f}M")
    alerts.append(f"⚠️ Perlu Perhatian: {worst_performer['retailer_name']} dengan penjualan Rp {worst_performer['total_sales']/1e6:.1f}M")
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