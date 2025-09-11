# cPanel Unicode Fix Guide

## Problem
You're getting this error on cPanel:
```
त्रुटि: त्रुटि भयो। कृपया पुनः प्रयास गर्नुहोस्। Error: 'ascii' codec can't encode characters in position 178-183: ordinal not in range(128)
```

This happens because cPanel servers often use ASCII encoding by default, but your Django app needs UTF-8 to handle Nepali characters.

## Solution

### 1. Upload the Files
Make sure these files are uploaded to your cPanel:

- `.htaccess` (in the root directory)
- `core/middleware.py`
- `core/utils.py`
- `cpanel_unicode_fix.py`

### 2. Set Environment Variables in cPanel

#### Option A: Through cPanel File Manager
1. Go to cPanel → File Manager
2. Navigate to your project root
3. Create/edit `.env` file with:
```
PYTHONIOENCODING=utf-8
LANG=en_US.UTF-8
LC_ALL=en_US.UTF-8
```

#### Option B: Through cPanel Terminal
```bash
export PYTHONIOENCODING=utf-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
```

### 3. Update Python Path (if needed)
In cPanel Terminal, run:
```bash
python3 cpanel_unicode_fix.py
```

### 4. Restart Your Application
- If using Passenger: Restart through cPanel
- If using WSGI: Touch the `wsgi.py` file to restart

### 5. Test the Fix
1. Go to your employment ad editor
2. Try uploading a document with Nepali text
3. Check if the error is resolved

## Files Added/Modified

### `.htaccess`
```apache
# Enable UTF-8 encoding
AddDefaultCharset UTF-8

# Set environment variables for Unicode support
SetEnv PYTHONIOENCODING utf-8
SetEnv LANG en_US.UTF-8
SetEnv LC_ALL en_US.UTF-8

# Force UTF-8 for all text files
<FilesMatch "\.(html|htm|css|js|txt|xml)$">
    ForceType text/plain; charset=utf-8
</FilesMatch>

# Python WSGI configuration
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ /rajdhani/wsgi.py/$1 [QSA,PT,L]
```

### `core/middleware.py`
- Unicode middleware to handle encoding issues
- Sets environment variables on each request

### `core/utils.py`
- Utility functions for Unicode handling
- Safe string conversion functions

### `rajdhani/settings.py`
- Added Unicode settings
- Added Unicode middleware
- Set default charset to UTF-8

## Troubleshooting

### If the error persists:

1. **Check file permissions**: Make sure all files are readable
2. **Check Python version**: Ensure you're using Python 3.6+
3. **Check server logs**: Look for more specific error messages
4. **Test with simple text**: Try with English text first

### Alternative Fix:
If the above doesn't work, add this to the top of your `wsgi.py`:

```python
import os
import sys

# Set environment variables
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['LANG'] = 'en_US.UTF-8'
os.environ['LC_ALL'] = 'en_US.UTF-8'

# Set locale
import locale
try:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_ALL, 'C.UTF-8')
    except:
        pass
```

## Testing
After implementing the fix, test with:
1. Nepali text in forms
2. PDF generation with Nepali content
3. OCR processing of Nepali documents

The error should be resolved and your app should handle Nepali characters properly.

