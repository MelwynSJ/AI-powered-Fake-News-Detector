#!/usr/bin/env python3
"""
Quick Setup Script for Fake News Detection System

This script helps automate the setup and running process.
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully!")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ {description} failed!")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return False
    return True

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7+ required. Current version:", sys.version)
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install required packages."""
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("💡 Try: python -m pip install --upgrade pip")
        print("💡 Or use: pip install --user -r requirements.txt")
        return False
    return True

def download_nltk_data():
    """Download NLTK data."""
    nltk_commands = [
        'python -c "import nltk; nltk.download(\'stopwords\', quiet=True)"',
        'python -c "import nltk; nltk.download(\'punkt\', quiet=True)"',
        'python -c "import nltk; nltk.download(\'wordnet\', quiet=True)"'
    ]
    
    print("\n🔧 Downloading NLTK data (optional but recommended)...")
    for cmd in nltk_commands:
        subprocess.run(cmd, shell=True, capture_output=True)
    print("✅ NLTK data download completed!")

def train_model():
    """Train the machine learning model."""
    return run_command("python train_model.py", "Training the ML model")

def test_prediction():
    """Test the prediction system."""
    print("\n🔧 Testing prediction system...")
    print("📝 You can test the system manually by running: python predict_live.py")
    return True

def launch_streamlit():
    """Launch the Streamlit web application."""
    print("\n🚀 Launching Streamlit web application...")
    print("📱 The web interface will open at: http://localhost:8501")
    print("💡 Press Ctrl+C to stop the application")
    
    try:
        subprocess.run("streamlit run app.py", shell=True)
    except KeyboardInterrupt:
        print("\n👋 Streamlit application stopped!")

def main():
    """Main setup function."""
    print("🔍 Fake News Detection System - Setup Script")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Show menu
    while True:
        print("\n📋 Setup Options:")
        print("1. 📦 Install dependencies")
        print("2. 🧠 Train model")
        print("3. 🚀 Launch web interface")
        print("4. 🔧 Complete setup (steps 1-2)")
        print("5. 📖 Show usage instructions")
        print("6. 🚪 Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            print("\n📦 Installing Dependencies...")
            if install_dependencies():
                download_nltk_data()
                print("✅ All dependencies installed successfully!")
            else:
                print("❌ Failed to install dependencies. Please check the error messages above.")
        
        elif choice == '2':
            print("\n🧠 Training Model...")
            if not os.path.exists('requirements.txt'):
                print("❌ requirements.txt not found. Make sure you're in the correct directory.")
                continue
            
            if train_model():
                print("✅ Model training completed successfully!")
                print("📁 Model files saved in: models/")
            else:
                print("❌ Model training failed. Make sure dependencies are installed.")
        
        elif choice == '3':
            print("\n🚀 Launching Web Interface...")
            if not os.path.exists('models/fake_news_model.joblib'):
                print("❌ Model not found. Please train the model first (option 2).")
                continue
            launch_streamlit()
        
        elif choice == '4':
            print("\n🔧 Complete Setup...")
            print("Step 1: Installing dependencies...")
            if install_dependencies():
                download_nltk_data()
                print("Step 2: Training model...")
                if train_model():
                    print("\n🎉 Setup completed successfully!")
                    print("✅ You can now use the system:")
                    print("   - Run 'python predict_live.py' for command line")
                    print("   - Run 'streamlit run app.py' for web interface")
                else:
                    print("❌ Setup failed at model training step.")
            else:
                print("❌ Setup failed at dependency installation step.")
        
        elif choice == '5':
            print("\n📖 Usage Instructions:")
            print("="*50)
            print("1. 📦 First, install dependencies (option 1)")
            print("2. 🧠 Train the model (option 2)")
            print("3. 🚀 Use the system:")
            print("   • Web interface: streamlit run app.py")
            print("   • Command line: python predict_live.py")
            print("   • Custom analysis: python -c \"from predict_live import LiveNewsPredictor; p=LiveNewsPredictor(); print(p.predict_text('Your text here'))\"")
            print("\n📋 File Structure:")
            print("   • train_model.py - Train the ML model")
            print("   • predict_live.py - Command line interface")
            print("   • app.py - Streamlit web interface")
            print("   • config.py - Configuration settings")
            print("   • models/ - Trained model files")
            print("   • data/ - Training datasets")
        
        elif choice == '6':
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1-6.")

if __name__ == "__main__":
    main()
