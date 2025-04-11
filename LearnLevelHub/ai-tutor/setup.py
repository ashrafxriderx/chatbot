#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path
import shutil

def main():
    print("===== AI Tutor Setup =====")
    print("This script will set up everything needed to run the AI Tutor application.")
    
    # Check Python version
    if sys.version_info < (3, 9):
        print("Error: Python 3.9 or newer is required")
        print(f"You are using Python {sys.version_info.major}.{sys.version_info.minor}")
        sys.exit(1)
    
    print(f"Using Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Create virtual environment
    print("\nCreating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("Virtual environment created successfully!")
    except subprocess.CalledProcessError:
        print("Error: Failed to create virtual environment")
        sys.exit(1)
    
    # Determine executable paths
    if os.name == "nt":  # Windows
        python_exe = os.path.join("venv", "Scripts", "python.exe")
        pip_exe = os.path.join("venv", "Scripts", "pip.exe")
    else:  # macOS/Linux
        python_exe = os.path.join("venv", "bin", "python")
        pip_exe = os.path.join("venv", "bin", "pip")
    
    # Install requirements
    print("\nInstalling requirements...")
    try:
        subprocess.run([pip_exe, "install", "--upgrade", "pip"], check=True)
        subprocess.run([pip_exe, "install", "-r", "requirements.txt"], check=True)
        print("Requirements installed successfully!")
    except subprocess.CalledProcessError:
        print("Error: Failed to install requirements")
        sys.exit(1)
    
    # Set up API key
    print("\nSetting up API key...")
    if os.path.exists(".env"):
        print("Found existing .env file. Keeping it as is.")
    else:
        if os.path.exists(".env.example"):
            print("Creating .env file from template...")
            shutil.copy(".env.example", ".env")
            
        print("\nYou need a Google AI API key to use this application.")
        print("Get one from: https://makersuite.google.com/")
        api_key = input("\nEnter your Google AI API key (press Enter to skip for now): ")
        
        if api_key:
            with open(".env", "w") as f:
                f.write(f"GOOGLE_API_KEY={api_key}")
            print("API key saved to .env file")
        else:
            print("No API key provided. You'll need to add it to the .env file before using the app.")
    
    # Print success message and next steps
    print("\n===== Setup Complete! =====")
    print("\nTo run the application:")
    if os.name == "nt":  # Windows
        print("1. Activate the environment: venv\\Scripts\\activate")
    else:  # macOS/Linux
        print("1. Activate the environment: source venv/bin/activate")
    print("2. Run the app: streamlit run app.py")
    print("\nEnjoy your AI Tutor!")

if __name__ == "__main__":
    main()