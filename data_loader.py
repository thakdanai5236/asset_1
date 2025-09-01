import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def load_data(file_path="data/machine_data.xlsx"):
    """Load machine usage data from Excel file"""
    try:
        df = pd.read_excel(file_path)
        
        # Convert date columns
        if 'Start_Date' in df.columns:
            df['Start_Date'] = pd.to_datetime(df['Start_Date'])
        if 'End_Date' in df.columns:
            df['End_Date'] = pd.to_datetime(df['End_Date'])
            
        # Calculate utilization percentage
        if 'Utilization_Percent' not in df.columns and 'Target_Utilization' in df.columns:
            max_daily_hours = 24
            df['Actual_Utilization'] = (df['Hours_Daily'] / max_daily_hours) * 100
            df['Utilization_Percent'] = df['Actual_Utilization']
        
        # Fill missing values
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        df[numeric_columns] = df[numeric_columns].fillna(0)
        
        categorical_columns = df.select_dtypes(include=['object']).columns
        df[categorical_columns] = df[categorical_columns].fillna('Unknown')
        
        return df
        
    except Exception as e:
        raise Exception(f"Error loading data: {str(e)}")

def filter_data(df, start_date=None, end_date=None, site=None, machine_type=None):
    """Filter data based on selected criteria"""
    filtered_df = df.copy()
    
    # Date range filter
    if start_date and end_date and 'Start_Date' in df.columns:
        filtered_df = filtered_df[
            (filtered_df['Start_Date'] >= start_date) & 
            (filtered_df['Start_Date'] <= end_date)
        ]
    
    # Site filter
    if site and site != "All Sites":
        filtered_df = filtered_df[filtered_df['Site'] == site]
    
    # Machine type filter
    if machine_type and machine_type != "All Equipment":
        filtered_df = filtered_df[filtered_df['Machine_Type'] == machine_type]
    
    return filtered_df

def prepare_chart_data(df):
    """Prepare data for various chart types"""
    chart_data = {}
    
    # Status distribution
    if 'Status' in df.columns:
        chart_data['status_dist'] = df['Status'].value_counts()
    
    # Monthly hours simulation
    if 'Hours_Daily' in df.columns:
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        np.random.seed(42)
        monthly_hours = []
        for i in range(12):
            base_hours = df['Hours_Daily'].sum()
            monthly_variation = np.random.uniform(0.8, 1.2)
            monthly_hours.append(base_hours * monthly_variation * 30)
            
        chart_data['monthly_hours'] = pd.DataFrame({
            'Month': months,
            'Hours': monthly_hours
        })
    
    # Utilization trend data
    weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4']
    
    if 'Utilization_Percent' in df.columns:
        current_util = df['Utilization_Percent'].mean()
    else:
        current_util = (df['Hours_Daily'].mean() / 24) * 100
        
    if 'Target_Utilization' in df.columns:
        target_util = df['Target_Utilization'].mean()
    else:
        target_util = 75
        
    np.random.seed(42)
    current_trend = []
    target_trend = []
    
    for i in range(4):
        current_var = current_util + np.random.uniform(-5, 5)
        target_var = target_util + np.random.uniform(-2, 2)
        current_trend.append(max(0, min(100, current_var)))
        target_trend.append(max(0, min(100, target_var)))
        
    chart_data['trend_data'] = pd.DataFrame({
        'Week': weeks,
        'Current': current_trend,
        'Baseline': target_trend
    })
    
    return chart_data
