import pandas as pd
from datetime import datetime, timedelta

def calculate_kpis(df):
    """Calculate key performance indicators"""
    kpis = {}
    
    kpis['total_machines'] = len(df)
    kpis['maintenance_count'] = len(df[df['Status'] == 'Maintenance'])
    
    available_statuses = ['Working', 'Idle']
    kpis['available_machines'] = len(df[df['Status'].isin(available_statuses)])
    
    if 'Utilization_Percent' in df.columns:
        kpis['avg_utilization'] = df['Utilization_Percent'].mean()
    elif 'Hours_Daily' in df.columns:
        kpis['avg_utilization'] = (df['Hours_Daily'].mean() / 24) * 100
    else:
        kpis['avg_utilization'] = 0
    
    return kpis

def get_date_range(date_option):
    """Convert date range option to actual dates"""
    today = datetime.now()
    
    if date_option == "Last 30 Days":
        start_date = today - timedelta(days=30)
    elif date_option == "Last 3 Months":
        start_date = today - timedelta(days=90)
    elif date_option == "Last 6 Months":
        start_date = today - timedelta(days=180)
    elif date_option == "This Year":
        start_date = datetime(today.year, 1, 1)
    else:  # All Time
        start_date = datetime(2000, 1, 1)
    
    return start_date, today

def format_number(number, format_type="default"):
    """Format numbers for display"""
    if pd.isna(number):
        return "0"
    
    if format_type == "currency":
        return f"${number:,.2f}"
    elif format_type == "percentage":
        return f"{number:.1f}%"
    else:
        return f"{number:,.0f}"
