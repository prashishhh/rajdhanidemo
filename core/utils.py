"""
Utility functions for Unicode handling
"""
import os
import sys
import locale


def ensure_unicode_environment():
    """
    Ensure the environment is properly configured for Unicode
    """
    # Set environment variables
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['LANG'] = 'en_US.UTF-8'
    os.environ['LC_ALL'] = 'en_US.UTF-8'
    
    # Set locale
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except:
        try:
            locale.setlocale(locale.LC_ALL, 'C.UTF-8')
        except:
            pass
    
    # Ensure stdout/stderr are UTF-8
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')


def safe_unicode_string(text):
    """
    Safely convert text to Unicode string
    """
    if isinstance(text, bytes):
        try:
            return text.decode('utf-8')
        except UnicodeDecodeError:
            return text.decode('utf-8', errors='replace')
    return str(text)


def convert_nepali_to_english_numbers(text):
    """
    Convert Nepali numbers to English numbers in text
    """
    if not text:
        return text
    
    # Mapping of Nepali numbers to English numbers
    nepali_to_english = {
        '०': '0', '१': '1', '२': '2', '३': '3', '४': '4',
        '५': '5', '६': '6', '७': '7', '८': '8', '९': '9'
    }
    
    # Convert each Nepali digit to English
    result = str(text)
    for nepali, english in nepali_to_english.items():
        result = result.replace(nepali, english)
    
    return result

