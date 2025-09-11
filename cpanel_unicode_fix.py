#!/usr/bin/env python3
"""
cPanel Unicode Fix Script
Run this script on cPanel to fix Unicode encoding issues
"""

import os
import sys

def fix_unicode_environment():
    """Fix Unicode environment for cPanel"""
    
    # Set environment variables
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['LANG'] = 'en_US.UTF-8'
    os.environ['LC_ALL'] = 'en_US.UTF-8'
    
    # Set locale
    import locale
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        print("✅ Locale set to en_US.UTF-8")
    except:
        try:
            locale.setlocale(locale.LC_ALL, 'C.UTF-8')
            print("✅ Locale set to C.UTF-8")
        except:
            print("⚠️ Could not set locale, but continuing...")
    
    # Ensure stdout/stderr are UTF-8
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        print("✅ stdout reconfigured to UTF-8")
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
        print("✅ stderr reconfigured to UTF-8")
    
    print("✅ Unicode environment fixed!")

if __name__ == "__main__":
    fix_unicode_environment()

