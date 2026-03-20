"""
Script to help install Tesseract OCR on Windows.
This script provides download links and installation instructions.
"""

import os
import subprocess
import sys

def check_tesseract_installed():
    """Check if Tesseract is installed."""
    try:
        # Try to run tesseract command
        result = subprocess.run(['tesseract', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Tesseract OCR is installed!")
            print(f"Version: {result.stdout.split('tesseract')[0].strip()}")
            return True
    except FileNotFoundError:
        pass
    return False

def check_tesseract_path():
    """Check if Tesseract is in common Windows locations."""
    common_paths = [
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files\Tesseract\tesseract.exe',
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            print(f"✓ Found Tesseract at: {path}")
            return path
    
    return None

def main():
    """Main installation helper."""
    print("=" * 70)
    print("Tesseract OCR Installation Helper for Windows")
    print("=" * 70)
    print()
    
    # Check if already installed
    if check_tesseract_installed():
        print("\n✓ Tesseract OCR is already installed and in your PATH!")
        return
    
    # Check common installation paths
    tesseract_path = check_tesseract_path()
    if tesseract_path:
        print("\n✓ Tesseract OCR is installed but not in PATH.")
        print(f"Configure it in Django settings to use: {tesseract_path}")
        return
    
    # Installation instructions
    print("Tesseract OCR is not installed.")
    print()
    print("Please follow these steps to install it:")
    print()
    print("1. Download Tesseract OCR installer:")
    print("   https://github.com/UB-Mannheim/tesseract/wiki")
    print()
    print("2. Or use direct download link:")
    print("   https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe")
    print()
    print("3. Run the installer with default settings")
    print("   (Install to: C:\\Program Files\\Tesseract-OCR)")
    print()
    print("4. After installation, run this script again to verify:")
    print("   python install_tesseract.py")
    print()
    print("=" * 70)

if __name__ == '__main__':
    main()



