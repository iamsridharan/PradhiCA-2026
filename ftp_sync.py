import os
import time
import ftplib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
FTP_HOST = "72.60.217.169"
FTP_USER = "u925520622"
FTP_PASS = "SriTech@2016$"
LOCAL_ROOT = os.path.abspath(".")
REMOTE_ROOT = "/domains/pradhica.com/public_html"

IGNORED_DIRS = {'.git', 'node_modules', 'ftp_content', '__pycache__', '.gemini', '.vscode'}
IGNORED_EXTENSIONS = {'.DS_Store', '.tmp', '.log'}

class FTPSyncHandler(FileSystemEventHandler):
    def __init__(self):
        self.ftp = None
        self.connect()

    def connect(self):
        try:
            if self.ftp:
                try:
                    self.ftp.quit()
                except:
                    pass
            self.ftp = ftplib.FTP(FTP_HOST)
            self.ftp.login(FTP_USER, FTP_PASS)
            print(f"Connected to FTP {FTP_HOST}")
        except Exception as e:
            print(f"Connection failed: {e}")
            self.ftp = None

    def should_ignore(self, path):
        rel_path = os.path.relpath(path, LOCAL_ROOT)
        parts = rel_path.split(os.sep)
        for part in parts:
            if part in IGNORED_DIRS:
                return True
        _, ext = os.path.splitext(path)
        if ext in IGNORED_EXTENSIONS:
            return True
        return False

    def upload_file(self, local_path):
        if self.should_ignore(local_path):
            return

        if not self.ftp:
            self.connect()
            if not self.ftp:
                return

        rel_path = os.path.relpath(local_path, LOCAL_ROOT)
        remote_path = os.path.join(REMOTE_ROOT, rel_path).replace("\\", "/")
        remote_dir = os.path.dirname(remote_path)

        print(f"Syncing: {rel_path} -> {remote_path}")

        try:
            # Ensure remote directory exists
            self.ensure_remote_dir(remote_dir)
            
            with open(local_path, 'rb') as f:
                self.ftp.storbinary(f'STOR {remote_path}', f)
            print(f"Uploaded: {remote_path}")
        except Exception as e:
            print(f"Failed to upload {remote_path}: {e}")
            # Try reconnecting once
            self.connect()
            try:
                self.ensure_remote_dir(remote_dir)
                with open(local_path, 'rb') as f:
                    self.ftp.storbinary(f'STOR {remote_path}', f)
                print(f"Uploaded (retry): {remote_path}")
            except Exception as e2:
                print(f"Retry failed: {e2}")

    def ensure_remote_dir(self, remote_dir):
        """Recursively create remote directories."""
        if remote_dir == "/" or remote_dir == "":
            return

        # Optimization: Don't check if we know it exists (could add cache here)
        try:
            self.ftp.cwd(remote_dir)
        except:
            parent = os.path.dirname(remote_dir)
            self.ensure_remote_dir(parent)
            try:
                self.ftp.mkd(remote_dir)
                print(f"Created remote dir: {remote_dir}")
            except Exception as e:
                pass

    def on_modified(self, event):
        if not event.is_directory:
            self.upload_file(event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            self.upload_file(event.src_path)

if __name__ == "__main__":
    print(f"Starting FTP Sync...")
    print(f"Local: {LOCAL_ROOT}")
    print(f"Remote: {REMOTE_ROOT}")
    
    event_handler = FTPSyncHandler()
    observer = Observer()
    observer.schedule(event_handler, LOCAL_ROOT, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
