#!/usr/bin/env python3
"""
Quick run script for Machine Usage Dashboard
สคริปต์สำหรับรันแอปพลิเคชันอย่างรวดเร็ว
"""

import subprocess
import sys
import os

def install_requirements():
    """ติดตั้ง dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False
    return True

def run_dashboard():
    """รัน dashboard"""
    print("🚀 Starting Machine Usage Dashboard...")
    print("🌐 Open your browser and go to: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the dashboard")
    print("")
    
    try:
        subprocess.run(["streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped!")
    except FileNotFoundError:
        print("❌ Streamlit not found. Please install it first:")
        print("   pip install streamlit")

def main():
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found!")
        return
        
    if not os.path.exists("app.py"):
        print("❌ app.py not found!")
        return
    
    # Install dependencies
    if install_requirements():
        # Run dashboard
        run_dashboard()

if __name__ == "__main__":
    main()
