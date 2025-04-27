import os
import shutil
import platform
import subprocess


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
        vlc_path = VLCMediaPlayerUtil.get_vlc_media_player_path()
        file_dir = os.path.dirname(file_path)
        filename = os.path.basename(file_path)

        # Use cwd to set the working directory for the subprocess
        # Pass only the filename to VLC since we are in its directory
        try:
            subprocess.Popen([vlc_path, filename], cwd=file_dir)
        except FileNotFoundError:
            # Fallback if cwd fails or VLC needs full path even with cwd
            print(f"Could not start VLC in directory {file_dir}. Trying with full path.")
            subprocess.Popen([vlc_path, file_path])

    @staticmethod
    def open_playlist_from_folder(folder_path: str):
        vlc_path = VLCMediaPlayerUtil.get_vlc_media_player_path()

        # Use cwd to set the working directory for the subprocess
        # Pass '.' to VLC to indicate the current directory (which we set via cwd)
        try:
            # Some versions/OS might prefer '.' or the folder name itself when using cwd
            subprocess.Popen([vlc_path, "."], cwd=folder_path)
        except FileNotFoundError:
            # Fallback if cwd fails or VLC needs full path even with cwd
            print(f"Could not start VLC in directory {folder_path}. Trying with full path.")
            subprocess.Popen([vlc_path, folder_path])
