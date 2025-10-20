import os
import shutil
import platform
import subprocess

from database import get_db
from models.setting import Setting


class VLCMediaPlayerUtil:
    @staticmethod
    def get_vlc_media_player_path() -> str:
        # Try to find VLC in common locations or in PATH
        vlc_executables = {
            "Windows": [rf"C:\Program Files\VideoLAN\VLC\vlc.exe", rf"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe"],
            "Darwin": ["/Applications/VLC.app/Contents/MacOS/VLC"],
            "Linux": ["/usr/bin/vlc", "/snap/bin/vlc", "/usr/local/bin/vlc"],
        }

        system = platform.system()
        paths_to_check = vlc_executables.get(system, [])

        # Try to find VLC in the settings
        db = next(get_db())
        try:
            setting: Setting = db.query(Setting).filter(Setting.key == "vlc_media_player_path").first()
            if setting and setting.value:
                paths_to_check.insert(0, setting.value)
        finally:
            db.close()

        for path in paths_to_check:
            if os.path.isfile(path):
                return path

        # Fallback: check if 'vlc' is in PATH
        vlc_path = shutil.which("vlc")
        if vlc_path:
            return vlc_path

        raise FileNotFoundError("VLC media player not found on this system.")

    @staticmethod
    def open_file(file_path: str):
        file_dir = os.path.dirname(file_path)
        filename = os.path.basename(file_path)

        # Use cwd to set the working directory for the subprocess
        # Pass only the filename to VLC since we are in its directory
        VLCMediaPlayerUtil.run_vlc_with_options(filename, cwd=file_dir)

    @staticmethod
    def open_playlist_from_folder(folder_path: str):
        # Use cwd to set the working directory for the subprocess
        # Pass '.' to VLC to indicate the current directory (which we set via cwd)
        VLCMediaPlayerUtil.run_vlc_with_options(".", cwd=folder_path)

    @staticmethod
    def run_vlc_with_options(filename: str, cwd: str | None = None):
        vlc_path = VLCMediaPlayerUtil.get_vlc_media_player_path()
        is_windows = platform.system() == "Windows"
        is_wsl = "microsoft" in platform.release().lower()

        try:
            if is_windows:
                # On Windows, use start to open VLC in a new window
                subprocess.Popen(["start", "", vlc_path, filename], shell=True, cwd=cwd)
            elif is_wsl:
                # On WSL, open using Windows VLC using CMD
                # Remove mnt prefix for Windows path compatibility
                windows_path = filename.replace("/mnt/c/", "C:\\").replace("/", "\\")
                vlc_path = vlc_path.replace("/mnt/c/", "C:\\").replace("/", "\\")
                subprocess.run(["cmd.exe", "/C", "start", "", vlc_path, windows_path], cwd=cwd)
            else:
                # On macOS and Linux, just run VLC directly
                subprocess.Popen([vlc_path, filename], cwd=cwd)

        except FileNotFoundError:
            print(f"Could not start VLC in directory {cwd}. Trying with full path.")
            if is_windows:
                subprocess.Popen(["start", "", vlc_path, os.path.join(cwd, filename)], shell=True)
            elif is_wsl:
                # On WSL, open using Windows VLC using CMD
                # Remove mnt prefix for Windows path compatibility
                windows_path = os.path.join(cwd, filename).replace("/mnt/c/", "C:\\").replace("/", "\\")
                vlc_path = vlc_path.replace("/mnt/c/", "C:\\").replace("/", "\\")
                subprocess.run(["cmd.exe", "/C", "start", "", vlc_path, windows_path])
            else:
                # On macOS and Linux, just run VLC directly
                subprocess.Popen([vlc_path, filename], cwd=cwd)
