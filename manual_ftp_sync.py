import os
import ftplib
import sys

# Configuration
FTP_HOST = "72.60.217.169"
FTP_USER = "u925520622"
FTP_PASS = "SriTech@2016$"
LOCAL_ROOT = os.path.abspath(".")
REMOTE_ROOT = "/domains/pradhica.com/public_html"

IGNORED_DIRS = {'.git', 'node_modules', 'ftp_content', '__pycache__', '.gemini', '.vscode', '__MACOSX'}
IGNORED_EXTENSIONS = {'.DS_Store', '.tmp', '.log'}

class ManualFTPSync:
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
            sys.exit(1)

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

    def ensure_remote_dir(self, remote_dir):
        """Recursively create remote directories."""
        if remote_dir == "/" or remote_dir == "":
            return

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

    def upload_file(self, local_path):
        if self.should_ignore(local_path):
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

    def sync_all(self):
        print(f"Starting Full FTP Sync...")
        print(f"Local: {LOCAL_ROOT}")
        print(f"Remote: {REMOTE_ROOT}")
        
        for root, dirs, files in os.walk(LOCAL_ROOT):
            # Modify dirs in-place to skip ignored directories
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
            
            for file in files:
                file_path = os.path.join(root, file)
                self.upload_file(file_path)
        
        print("Sync completed!")

if __name__ == "__main__":
    syncer = ManualFTPSync()
    syncer.sync_all()
