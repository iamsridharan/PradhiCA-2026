#!/usr/bin/env python3
"""
Auto-Sync Script for PradhiCA Website
=====================================

This script watches index.html for changes and automatically synchronizes
headers and footers across all HTML files when changes are detected.

Requirements:
    pip install watchdog

Usage:
    python3 watch_and_sync.py

Features:
- Monitors index.html for file changes
- Automatically triggers header/footer sync when index.html is modified
- Runs in background and provides real-time updates
- Safe file handling with backup functionality
"""

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("ERROR: watchdog module not installed")
    print("Please install it with: pip install watchdog")
    import sys
    sys.exit(1)

import os
import time
import threading
from datetime import datetime
import subprocess
import sys

class IndexFileHandler(FileSystemEventHandler):
    """Handler for index.html file changes"""
    
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.index_path = os.path.join(root_dir, "index.html")
        self.script_path = os.path.join(root_dir, "update_headers_footers.py")
        self.last_sync = 0
        self.sync_cooldown = 2  # Prevent rapid fire syncs
        
    def on_modified(self, event):
        if event.is_directory:
            return
            
        if event.src_path == self.index_path:
            current_time = time.time()
            
            # Cooldown to prevent multiple rapid syncs
            if current_time - self.last_sync < self.sync_cooldown:
                return
                
            self.last_sync = current_time
            
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] index.html modified")
            print("Triggering header/footer synchronization...")
            
            # Run sync in separate thread to avoid blocking
            threading.Thread(target=self.sync_files, daemon=True).start()
    
    def sync_files(self):
        """Run the synchronization script"""
        try:
            if os.path.exists(self.script_path):
                result = subprocess.run([
                    sys.executable, self.script_path, self.root_dir
                ], capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    print("✓ Synchronization completed successfully")
                else:
                    print(f"✗ Synchronization failed: {result.stderr}")
            else:
                print(f"✗ Sync script not found: {self.script_path}")
                
        except subprocess.TimeoutExpired:
            print("✗ Synchronization timed out")
        except Exception as e:
            print(f"✗ Sync error: {e}")

def main():
    """Main function to start file watching"""
    
    root_dir = os.getcwd()
    index_path = os.path.join(root_dir, "index.html")
    
    if not os.path.exists(index_path):
        print("ERROR: index.html not found in current directory")
        print(f"Current directory: {root_dir}")
        return
    
    print("="*50)
    print("PradhiCA Auto-Sync Watcher")
    print("="*50)
    print(f"Monitoring: {index_path}")
    print("Waiting for changes...")
    print("Press Ctrl+C to stop")
    print()
    
    event_handler = IndexFileHandler(root_dir)
    observer = Observer()
    observer.schedule(event_handler, root_dir, recursive=False)
    
    try:
        observer.start()
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping watcher...")
        observer.stop()
        
    observer.join()
    print("Watcher stopped.")

if __name__ == "__main__":
    main()
