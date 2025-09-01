import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import pandas as pd
from data_loader import prepare_chart_data

def create_kpi_cards(title, value, icon, color):
    """Create KPI cards"""
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
        <div class="metric-value" style="color: {color};">{value}</div>
        <div class="metric-label">{title}</div>
    </div>
    """, unsafe_allow_html=True)

def create_donut_chart(df):
    """Create machine status distribution donut chart"""
    status_counts = df['Status'].value_counts()
    
    colors = {
        'Working': '#10b981',
        'Idle': '#3b82f6',
        'Maintenance': '#ef4444'
    }
    
    color_sequence = [colors.get(status, '#6b7280') for status in status_counts.index]
    
    fig = go.Figure(data=[go.Pie(
        labels=status_counts.index,
        values=status_counts.values,
        hole=0.4,
        marker=dict(colors=color_sequence, line=dict(color='#1f2937', width=2))
    )])
    
    fig.update_layout(
        title={'text': 'Machine Status Distribution', 'x': 0.5, 'font': {'color': 'white'}},
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=300
    )
    
    return fig

def create_bar_chart(df):
    """Create working hours bar chart"""
    chart_data = prepare_chart_data(df)
    monthly_data = chart_data['monthly_hours']
    
    fig = go.Figure(data=[
        go.Bar(
            x=monthly_data['Month'],
            y=monthly_data['Hours'],
            marker=dict(color='#3b82f6'),
            name='Working Hours'
        )
    ])
    
    fig.update_layout(
        title={'text': 'Working Hours per Month', 'x': 0.5, 'font': {'color': 'white'}},
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=300
    )
    
    return fig

def create_utilization_summary(df):
    """Create utilization summary card"""
    if 'Utilization_Percent' in df.columns:
        avg_util = df['Utilization_Percent'].mean()
    else:
        avg_util = (df['Hours_Daily'].mean() / 24) * 100
    
    target = df['Target_Utilization'].mean() if 'Target_Utilization' in df.columns else 75
    
    status_color = "#10b981" if avg_util >= target else "#f59e0b"
    status_text = "Above Target" if avg_util >= target else "Below Target"
    
    st.markdown(f"""
    <div class="chart-container">
        <h3 style="color: white; margin-bottom: 1rem;">Utilization Summary</h3>
        <div style="text-align: center;">
            <div style="font-size: 3rem; font-weight: bold; color: {status_color};">
                {avg_util:.1f}%
            </div>
            <div style="color: #9ca3af;">{status_text}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_trend_chart(df):
    """Create utilization trend chart"""
    chart_data = prepare_chart_data(df)
    trend_data = chart_data['trend_data']
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=trend_data['Week'],
        y=trend_data['Current'],
        mode='lines+markers',
        name='Current Project',
        line=dict(color='#3b82f6', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=trend_data['Week'],
        y=trend_data['Baseline'],
        mode='lines+markers',
        name='Previous Baseline',
        line=dict(color='#10b981', width=3, dash='dash')
    ))
    
    fig.update_layout(
        title={'text': 'Utilization Trend Comparison', 'x': 0.5, 'font': {'color': 'white'}},
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=300
    )
    
    return fig
