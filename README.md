# EquipTrack - Machine Usage Dashboard

A comprehensive interactive dashboard for monitoring and analyzing machine usage data.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Add Your Data
- Place your Excel file in the `data/` folder
- Name it `machine_data.xlsx`
- Ensure it has the required columns (see Data Structure below)

### 3. Run the Dashboard
```bash
streamlit run app.py
```

## 📊 Data Structure
Your Excel file should contain these columns:
- Machine_ID
- Machine_Type  
- Status (Working/Idle/Maintenance)
- Hours_Daily
- Hours_Monthly
- Hours_Yearly
- Current_Project
- Start_Date
- End_Date
- Cost_Daily
- Cost_Monthly
- Target_Utilization (%)
- Site

## 🎯 Features
- Interactive KPI cards
- Machine status distribution
- Working hours trends
- Utilization analysis
- Advanced filtering
- Data export capabilities

## 📁 Project Structure
```
machine-usage-dashboard/
├── app.py              # Main application
├── data_loader.py      # Data handling
├── charts.py          # Chart functions
├── utils.py           # Utility functions
├── requirements.txt   # Dependencies
├── data/             # Data files
├── assets/           # Static assets
└── config/           # Configuration files
```

## 🔧 Customization
You can customize the dashboard by:
- Modifying colors in the CSS section
- Adding new chart types in `charts.py`
- Extending filters in the sidebar
- Adding new KPIs in `utils.py`

## 📞 Support
For issues or questions, please check the documentation in the `docs/` folder.
