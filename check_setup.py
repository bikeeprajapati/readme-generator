#!/usr/bin/env python3
"""
Setup checker for README Generator
Run this before starting the server to check your configuration
"""

import os
import sys
from pathlib import Path

def check_env_file():
    """Check if .env file exists and has required variables"""
    print("🔍 Checking .env file...")
    
    env_path = Path(".env")
    
    if not env_path.exists():
        print("❌ .env file not found!")
        print("   Run: cp .env.example .env")
        print("   Then edit .env and add your HUGGINGFACE_API_KEY")
        return False
    
    print("✅ .env file exists")
    
    # Read .env file
    with open(env_path, 'r') as f:
        content = f.read()
    
    # Check for required variables
    required_vars = {
        'HUGGINGFACE_API_KEY': 'hf_',
        'HUGGINGFACE_MODEL': 'mistralai'
    }
    
    missing = []
    invalid = []
    
    for var, expected_start in required_vars.items():
        if var not in content:
            missing.append(var)
        else:
            # Extract value
            for line in content.split('\n'):
                if line.startswith(var):
                    value = line.split('=', 1)[1].strip()
                    if value.startswith(expected_start):
                        print(f"✅ {var} is set")
                    elif value == f"{var.lower()}_here" or value == "":
                        invalid.append(var)
                        print(f"❌ {var} is not configured (still has placeholder)")
                    break
    
    if missing:
        print(f"\n❌ Missing variables in .env: {', '.join(missing)}")
        return False
    
    if invalid:
        print(f"\n❌ Invalid/placeholder values: {', '.join(invalid)}")
        print("   Get your HuggingFace token from: https://huggingface.co/settings/tokens")
        return False
    
    return True

def check_venv():
    """Check if virtual environment is activated"""
    print("\n🔍 Checking virtual environment...")
    
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment is activated")
        return True
    else:
        print("⚠️  Virtual environment not activated")
        print("   Run: source .venv/bin/activate")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print("\n🔍 Checking dependencies...")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'langchain',
        'langchain_huggingface',
        'gitpython'
    ]
    
    missing = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} installed")
        except ImportError:
            missing.append(package)
            print(f"❌ {package} not installed")
    
    if missing:
        print(f"\n❌ Missing packages. Run:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def check_folders():
    """Check if required folders exist"""
    print("\n🔍 Checking folder structure...")
    
    required_folders = [
        'backend',
        'backend/api',
        'backend/config',
        'backend/services',
        'backend/models',
        'backend/utils',
        'frontend'
    ]
    
    all_exist = True
    
    for folder in required_folders:
        path = Path(folder)
        if path.exists():
            print(f"✅ {folder}/ exists")
        else:
            print(f"❌ {folder}/ missing")
            all_exist = False
    
    return all_exist

def check_init_files():
    """Check if __init__.py files exist"""
    print("\n🔍 Checking __init__.py files...")
    
    required_inits = [
        'backend/__init__.py',
        'backend/api/__init__.py',
        'backend/config/__init__.py',
        'backend/services/__init__.py',
        'backend/models/__init__.py',
        'backend/utils/__init__.py'
    ]
    
    missing = []
    
    for init_file in required_inits:
        path = Path(init_file)
        if path.exists():
            print(f"✅ {init_file}")
        else:
            missing.append(init_file)
            print(f"❌ {init_file} missing")
    
    if missing:
        print("\n⚠️  Create missing __init__.py files:")
        for file in missing:
            print(f"   touch {file}")
        return False
    
    return True

def main():
    print("=" * 60)
    print("🚀 README Generator Setup Checker")
    print("=" * 60)
    
    checks = [
        ("Environment File", check_env_file),
        ("Virtual Environment", check_venv),
        ("Dependencies", check_dependencies),
        ("Folder Structure", check_folders),
        ("Init Files", check_init_files)
    ]
    
    results = []
    
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Error checking {name}: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Summary")
    print("=" * 60)
    
    all_passed = all(result for _, result in results)
    
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 All checks passed! You're ready to start the server:")
        print("   python run.py")
        print("   or")
        print("   uvicorn backend.main:app --reload")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print("\nQuick setup:")
        print("1. cp .env.example .env")
        print("2. Edit .env and add your HuggingFace API key")
        print("3. source .venv/bin/activate")
        print("4. pip install -r requirements.txt")
        print("5. Create missing __init__.py files: touch backend/__init__.py")
    
    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main()