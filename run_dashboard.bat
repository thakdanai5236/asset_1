@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting Machine Usage Dashboard...
echo Open your browser and go to: http://localhost:8501
echo.
echo Press Ctrl+C to stop the dashboard
echo.

streamlit run app.py
pause
