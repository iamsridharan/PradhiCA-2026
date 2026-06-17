#!/usr/bin/env python3
"""
Header/Footer Synchronization Script for PradhiCA Website
=========================================================

This script automatically updates headers and footers across all HTML files
based on the template defined in index.html.

Usage:
    python3 update_headers_footers.py

Features:
- Extracts header and footer from index.html as master template
- Updates all other HTML files to match
- Preserves file encoding and formatting
- Provides detailed logging of changes
"""

import os
import re
import glob
from pathlib import Path
import sys
from datetime import datetime

def extract_header_from_index(index_path):
    """Extract the standard header from index.html"""
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract header using regex
        header_pattern = r'(<header class="site-header bg-dark text-white-0_5">.*?</header><!-- END site header-->)'
        match = re.search(header_pattern, content, re.DOTALL)
        
        if match:
            return match.group(1)
        else:
            print("ERROR: Could not find header pattern in index.html")
            return None
            
    except Exception as e:
        print(f"ERROR reading index.html: {e}")
        return None

def extract_footer_copyright_from_index(index_path):
    """Extract the standard footer copyright from index.html"""
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract footer copyright using regex
        footer_pattern = r'(<p class="text-white-0_5 mb-0">&copy; \d{4} PradhiCA\..*?</p>)'
        match = re.search(footer_pattern, content, re.DOTALL)
        
        if match:
            return match.group(1)
        else:
            print("ERROR: Could not find footer pattern in index.html")
            return None
            
    except Exception as e:
        print(f"ERROR reading index.html: {e}")
        return None

def update_html_files(root_dir):
    """Main function to update all HTML files"""
    
    print("="*60)
    print("PradhiCA Header/Footer Synchronization Script")
    print("="*60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Root directory: {root_dir}")
    print()
    
    # Paths
    index_path = os.path.join(root_dir, "index.html")
    
    if not os.path.exists(index_path):
        print("ERROR: index.html not found in the specified directory")
        return False
    
    # Extract templates from index.html
    print("Extracting templates from index.html...")
    standard_header = extract_header_from_index(index_path)
    standard_footer = extract_footer_copyright_from_index(index_path)
    
    if not standard_header or not standard_footer:
        print("ERROR: Could not extract templates from index.html")
        return False
    
    print("✓ Header template extracted")
    print("✓ Footer template extracted")
    print()
    
    # Get all HTML files
    html_files = glob.glob(os.path.join(root_dir, "*.html"))
    html_files = [f for f in html_files if os.path.basename(f) != "index.html"]
    
    print(f"Found {len(html_files)} HTML files to update (excluding index.html)")
    print()
    
    # Update files
    updated_headers = 0
    updated_footers = 0
    errors = 0
    
    for file_path in html_files:
        filename = os.path.basename(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            file_updated = False
            
            # Update header
            header_pattern = r'<header class="site-header bg-dark text-white-0_5">.*?</header><!-- END site header-->'
            if re.search(header_pattern, content, re.DOTALL):
                content = re.sub(header_pattern, standard_header, content, flags=re.DOTALL)
                updated_headers += 1
                file_updated = True
                print(f"✓ Updated header: {filename}")
            
            # Update footer copyright
            footer_pattern = r'<p class="text-white-0_5 mb-0">&copy; \d{4} PradhiCA\..*?</p>'
            if re.search(footer_pattern, content, re.DOTALL):
                content = re.sub(footer_pattern, standard_footer, content, flags=re.DOTALL)
                updated_footers += 1
                file_updated = True
                print(f"✓ Updated footer: {filename}")
            
            # Write back if content changed
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            elif not file_updated:
                print(f"⚠ No changes needed: {filename}")
                
        except Exception as e:
            print(f"✗ ERROR processing {filename}: {e}")
            errors += 1
    
    # Summary
    print()
    print("="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Files processed: {len(html_files)}")
    print(f"Headers updated: {updated_headers}")
    print(f"Footers updated: {updated_footers}")
    print(f"Errors: {errors}")
    
    if errors == 0:
        print("✓ All files processed successfully!")
        return True
    else:
        print(f"⚠ Completed with {errors} errors")
        return False

if __name__ == "__main__":
    # Get current directory or use provided path
    if len(sys.argv) > 1:
        root_directory = sys.argv[1]
    else:
        root_directory = os.getcwd()
    
    success = update_html_files(root_directory)
    sys.exit(0 if success else 1)
