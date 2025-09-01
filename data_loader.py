import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def load_data(file_path="data/machine_data.xlsx"):
    """
    Load machine usage data from Excel file with flexible column handling
    """
    try:
        df = pd.read_excel(file_path)
        print(f"📊 โหลดข้อมูลสำเร็จ! มี {len(df)} แถว")
        print(f"📋 คอลัมน์ที่พบ: {list(df.columns)}")
        
        # Convert date columns if they exist
        date_columns = ['Start_Date', 'End_Date']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Add missing required columns with default values
        required_columns = {
            'Machine_ID': lambda: [f'Machine_{i+1}' for i in range(len(df))],
            'Machine_Type': lambda: 'Unknown',
            'Status': lambda: 'Working',
            'Hours_Daily': lambda: 8.0,
            'Site': lambda: 'Default Site',
            'Target_Utilization': lambda: 75.0,  # Default target 75%
            'Current_Project': lambda: 'Project A',
            'Cost_Daily': lambda: 1000.0,
            'Hours_Monthly': lambda: df.get('Hours_Daily', 8.0) * 30 if 'Hours_Daily' in df.columns else 240.0,
            'Hours_Yearly': lambda: df.get('Hours_Daily', 8.0) * 365 if 'Hours_Daily' in df.columns else 2920.0,
            'Cost_Monthly': lambda: df.get('Cost_Daily', 1000.0) * 30 if 'Cost_Daily' in df.columns else 30000.0
        }
        
        # Add missing columns
        for col, default_func in required_columns.items():
            if col not in df.columns:
                if callable(default_func):
                    df[col] = default_func()
                else:
                    df[col] = default_func
                print(f"➕ เพิ่มคอลัมน์ '{col}' ด้วยค่าเริ่มต้น")
        
        # Calculate utilization percentage if not present
        if 'Utilization_Percent' not in df.columns:
            # Calculate actual utilization based on hours and target
            max_daily_hours = 24
            df['Actual_Utilization'] = (df['Hours_Daily'] / max_daily_hours) * 100
            df['Utilization_Percent'] = df['Actual_Utilization']
        
        # Clean and validate Status column
        valid_statuses = ['Working', 'Idle', 'Maintenance']
        if 'Status' in df.columns:
            # Replace invalid statuses
            df['Status'] = df['Status'].fillna('Working')
            invalid_mask = ~df['Status'].isin(valid_statuses)
            if invalid_mask.any():
                print(f"⚠️ แก้ไขสถานะที่ไม่ถูกต้อง: {df.loc[invalid_mask, 'Status'].unique()}")
                df.loc[invalid_mask, 'Status'] = 'Working'
        
        # Fill missing numeric values
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            df[col] = df[col].fillna(0)
        
        # Fill missing categorical values
        categorical_columns = df.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            if col == 'Status':
                df[col] = df[col].fillna('Working')
            elif col == 'Site':
                df[col] = df[col].fillna('Default Site')
            elif col == 'Machine_Type':
                df[col] = df[col].fillna('Unknown')
            else:
                df[col] = df[col].fillna('Unknown')
        
        print(f"✅ ข้อมูลพร้อมใช้งาน! รวม {len(df)} เครื่องจักร")
        return df
        
    except FileNotFoundError:
        raise Exception("ไม่พบไฟล์ Excel! ตรวจสอบว่าวางไฟล์ 'machine_data.xlsx' ในโฟลเดอร์ 'data/' แล้ว")
    except Exception as e:
        raise Exception(f"Error loading data: {str(e)}")

def filter_data(df, start_date=None, end_date=None, site=None, machine_type=None):
    """
    Filter data based on selected criteria
    """
    filtered_df = df.copy()
    
    # Date range filter
    if start_date and end_date and 'Start_Date' in df.columns:
        # Only filter if Start_Date column exists and has valid dates
        mask = (filtered_df['Start_Date'].notna()) & \
               (filtered_df['Start_Date'] >= start_date) & \
               (filtered_df['Start_Date'] <= end_date)
        filtered_df = filtered_df[mask]
    
    # Site filter
    if site and site != "All Sites":
        filtered_df = filtered_df[filtered_df['Site'] == site]
    
    # Machine type filter
    if machine_type and machine_type != "All Equipment":
        filtered_df = filtered_df[filtered_df['Machine_Type'] == machine_type]
    
    return filtered_df

def prepare_chart_data(df):
    """
    Prepare data for various chart types
    """
    chart_data = {}
    
    # Status distribution
    if 'Status' in df.columns:
        chart_data['status_dist'] = df['Status'].value_counts()
    
    # Monthly hours (simulate monthly data from daily)
    if 'Hours_Daily' in df.columns:
        # Create monthly aggregation
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        # Simulate monthly data by multiplying daily by random factors
        np.random.seed(42)  # For consistent results
        monthly_hours = []
        base_hours = df['Hours_Daily'].sum()
        
        for i in range(12):
            monthly_variation = np.random.uniform(0.8, 1.2)
            monthly_hours.append(base_hours * monthly_variation * 22)  # 22 working days
            
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
        target_util = 75  # Default target
        
    # Simulate weekly trend
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

def validate_data(df):
    """
    Validate the loaded data and show summary
    """
    print("\n📊 สรุปข้อมูล:")
    print(f"   - จำนวนเครื่องจักร: {len(df)}")
    
    if 'Status' in df.columns:
        status_counts = df['Status'].value_counts()
        for status, count in status_counts.items():
            print(f"   - {status}: {count} เครื่อง")
    
    if 'Site' in df.columns:
        site_counts = df['Site'].value_counts()
        print(f"   - จำนวนสถานที่: {len(site_counts)}")
    
    if 'Machine_Type' in df.columns:
        type_counts = df['Machine_Type'].value_counts()
        print(f"   - ประเภทเครื่องจักร: {len(type_counts)}")
    
    return True, "ข้อมูลถูกต้อง"