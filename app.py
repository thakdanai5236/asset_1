import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from data_loader import load_data, filter_data
from charts import create_kpi_cards, create_donut_chart, create_bar_chart, create_utilization_summary, create_trend_chart
from utils import calculate_kpis, get_date_range

# Configure page
st.set_page_config(
    page_title="EquipTrack - Machine Usage Dashboard",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #4b5563;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .chart-container {
        background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #4b5563;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏭 EquipTrack - Machine Usage Dashboard</h1>
        <p>Monitor and analyze equipment performance</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    try:
        df = load_data()
        
        # Sidebar filters
        st.sidebar.header("📊 Dashboard Filters")
        
        # Date range filter
        date_options = ["Last 30 Days", "Last 3 Months", "Last 6 Months", "This Year", "All Time"]
        selected_date_range = st.sidebar.selectbox("📅 Date Range", date_options, index=0)
        
        # Site filter
        sites = ["All Sites"] + sorted(df['Site'].unique().tolist())
        selected_site = st.sidebar.selectbox("🏢 Site", sites, index=0)
        
        # Machine type filter
        machine_types = ["All Equipment"] + sorted(df['Machine_Type'].unique().tolist())
        selected_machine_type = st.sidebar.selectbox("⚙️ Machine Type", machine_types, index=0)
        
        # Apply filters
        start_date, end_date = get_date_range(selected_date_range)
        filtered_df = filter_data(df, start_date, end_date, selected_site, selected_machine_type)
        
        if filtered_df.empty:
            st.warning("⚠️ No data available for the selected filters.")
            return
            
        # Calculate KPIs
        kpis = calculate_kpis(filtered_df)
        
        # KPI Cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            create_kpi_cards("Total Machines", kpis['total_machines'], "📱", "#3b82f6")
        
        with col2:
            create_kpi_cards("Under Maintenance", kpis['maintenance_count'], "🔧", "#ef4444")
            
        with col3:
            create_kpi_cards("Available Machines", kpis['available_machines'], "✅", "#10b981")
            
        with col4:
            create_kpi_cards("Average Utilization", f"{kpis['avg_utilization']:.1f}%", "📊", "#f59e0b")
        
        # Charts Section
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(create_donut_chart(filtered_df), use_container_width=True)
            
        with col2:
            st.plotly_chart(create_bar_chart(filtered_df), use_container_width=True)
        
        # Bottom Section
        col1, col2 = st.columns([1, 2])
        
        with col1:
            create_utilization_summary(filtered_df)
            
        with col2:
            st.plotly_chart(create_trend_chart(filtered_df), use_container_width=True)
        
        # Data Table
        st.subheader("📋 Equipment Data")
        
        display_columns = [
            'Machine_ID', 'Machine_Type', 'Status', 'Site', 
            'Hours_Daily', 'Current_Project', 'Target_Utilization'
        ]
        
        display_df = filtered_df[display_columns].copy()
        display_df = display_df.round(2)
        
        st.dataframe(display_df, use_container_width=True, height=300)
        
        # Summary statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📊 Total Records", len(filtered_df))
            
        with col2:
            st.metric("💰 Total Daily Cost", f"${filtered_df['Cost_Daily'].sum():,.2f}")
            
        with col3:
            st.metric("⏱️ Total Daily Hours", f"{filtered_df['Hours_Daily'].sum():.1f}")
    
    except FileNotFoundError:
        st.error("❌ Excel file not found. Please ensure 'machine_data.xlsx' is in the data/ directory.")
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")

if __name__ == "__main__":
    main()
