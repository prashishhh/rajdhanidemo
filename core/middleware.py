"""
Unicode middleware to handle encoding issues on cPanel
"""
import os
import sys
import locale
from django.utils.deprecation import MiddlewareMixin


class UnicodeMiddleware(MiddlewareMixin):
    """
    Middleware to ensure proper Unicode handling
    """
    
    def process_request(self, request):
        # Set environment variables for Unicode support
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
        
        return None

