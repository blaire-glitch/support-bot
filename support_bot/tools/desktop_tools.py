"""Desktop Automation Tools for Support Bot.

Provides tools for automating desktop tasks like:
- Opening applications
- Taking screenshots
- File operations
- System information
- Running commands
- Keyboard/mouse automation
"""

import os
import subprocess
import shutil
import platform
from pathlib import Path
from datetime import datetime
from typing import Optional, Annotated
from pydantic import Field


# ============== Application Control ==============

def open_application(app_name: str) -> str:
    """Open an application by name.
    
    Args:
        app_name: Name of the application to open (e.g., 'notepad', 'chrome', 'calculator', 'word', 'excel')
    
    Returns:
        Status message indicating success or failure
    """
    # Common application mappings for Windows
    app_mappings = {
        # Browsers
        "chrome": "chrome",
        "firefox": "firefox",
        "edge": "msedge",
        "browser": "msedge",
        
        # Microsoft Office
        "word": "winword",
        "excel": "excel",
        "powerpoint": "powerpnt",
        "outlook": "outlook",
        "teams": "teams",
        
        # System apps
        "notepad": "notepad",
        "calculator": "calc",
        "paint": "mspaint",
        "settings": "ms-settings:",
        "file explorer": "explorer",
        "explorer": "explorer",
        "cmd": "cmd",
        "terminal": "wt",
        "powershell": "powershell",
        
        # Media
        "spotify": "spotify",
        "vlc": "vlc",
        
        # Development
        "vscode": "code",
        "visual studio code": "code",
        "code": "code",
    }
    
    # Normalize app name
    app_lower = app_name.lower().strip()
    executable = app_mappings.get(app_lower, app_name)
    
    try:
        if executable.startswith("ms-settings"):
            os.startfile(executable)
        else:
            subprocess.Popen(executable, shell=True)
        return f"✅ Successfully opened {app_name}"
    except Exception as e:
        return f"❌ Failed to open {app_name}: {str(e)}"


def close_application(app_name: str) -> str:
    """Close an application by name.
    
    Args:
        app_name: Name of the application process to close
    
    Returns:
        Status message
    """
    try:
        # Use taskkill on Windows
        result = subprocess.run(
            ["taskkill", "/IM", f"{app_name}*", "/F"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return f"✅ Closed {app_name}"
        else:
            return f"⚠️ Could not find or close {app_name}"
    except Exception as e:
        return f"❌ Error closing {app_name}: {str(e)}"


def list_running_apps() -> str:
    """List currently running applications.
    
    Returns:
        List of running application names
    """
    try:
        result = subprocess.run(
            ["tasklist", "/FO", "CSV", "/NH"],
            capture_output=True,
            text=True
        )
        
        # Parse and get unique app names
        apps = set()
        for line in result.stdout.strip().split('\n'):
            if line:
                parts = line.split('","')
                if parts:
                    app_name = parts[0].strip('"')
                    if not app_name.lower().startswith(('system', 'svchost', 'runtime', 'conhost')):
                        apps.add(app_name)
        
        app_list = sorted(apps)[:30]  # Limit to 30 apps
        return "📋 **Running Applications:**\n" + "\n".join(f"• {app}" for app in app_list)
    except Exception as e:
        return f"❌ Error listing apps: {str(e)}"


# ============== Screenshot ==============

def take_screenshot(filename: Optional[str] = None) -> str:
    """Take a screenshot of the desktop.
    
    Args:
        filename: Optional custom filename (without extension). Defaults to timestamp.
    
    Returns:
        Path to the saved screenshot
    """
    try:
        from PIL import ImageGrab
        
        # Create screenshots folder
        screenshots_dir = Path.home() / "Pictures" / "Screenshots"
        screenshots_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        if not filename:
            filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        filepath = screenshots_dir / f"{filename}.png"
        
        # Take screenshot
        screenshot = ImageGrab.grab()
        screenshot.save(filepath)
        
        return f"📸 Screenshot saved to: {filepath}"
    except ImportError:
        return "❌ Pillow library not installed. Run: pip install Pillow"
    except Exception as e:
        return f"❌ Failed to take screenshot: {str(e)}"


# ============== File Operations ==============

def create_folder(folder_path: str) -> str:
    """Create a new folder.
    
    Args:
        folder_path: Path where to create the folder
    
    Returns:
        Status message
    """
    try:
        path = Path(folder_path).expanduser()
        path.mkdir(parents=True, exist_ok=True)
        return f"📁 Created folder: {path}"
    except Exception as e:
        return f"❌ Failed to create folder: {str(e)}"


def list_files(folder_path: str = ".", file_type: Optional[str] = None) -> str:
    """List files in a folder.
    
    Args:
        folder_path: Path to the folder (default: current directory)
        file_type: Optional file extension filter (e.g., 'txt', 'pdf')
    
    Returns:
        List of files in the folder
    """
    try:
        path = Path(folder_path).expanduser()
        if not path.exists():
            return f"❌ Folder not found: {folder_path}"
        
        files = []
        for item in path.iterdir():
            if file_type:
                if item.is_file() and item.suffix.lower() == f".{file_type.lower()}":
                    files.append(f"📄 {item.name}")
            else:
                icon = "📁" if item.is_dir() else "📄"
                files.append(f"{icon} {item.name}")
        
        if not files:
            return f"📂 Folder is empty: {folder_path}"
        
        return f"📂 **Contents of {path}:**\n" + "\n".join(files[:50])
    except Exception as e:
        return f"❌ Error listing files: {str(e)}"


def open_file(file_path: str) -> str:
    """Open a file with its default application.
    
    Args:
        file_path: Path to the file to open
    
    Returns:
        Status message
    """
    try:
        path = Path(file_path).expanduser()
        if not path.exists():
            return f"❌ File not found: {file_path}"
        
        os.startfile(str(path))
        return f"✅ Opened: {path.name}"
    except Exception as e:
        return f"❌ Failed to open file: {str(e)}"


def move_file(source: str, destination: str) -> str:
    """Move a file or folder to a new location.
    
    Args:
        source: Current path of the file/folder
        destination: New path for the file/folder
    
    Returns:
        Status message
    """
    try:
        src = Path(source).expanduser()
        dst = Path(destination).expanduser()
        
        if not src.exists():
            return f"❌ Source not found: {source}"
        
        shutil.move(str(src), str(dst))
        return f"✅ Moved {src.name} to {dst}"
    except Exception as e:
        return f"❌ Failed to move: {str(e)}"


def delete_file(file_path: str, confirm: bool = False) -> str:
    """Delete a file (requires confirmation).
    
    Args:
        file_path: Path to the file to delete
        confirm: Must be True to actually delete
    
    Returns:
        Status message
    """
    if not confirm:
        return f"⚠️ To delete '{file_path}', call this again with confirm=True"
    
    try:
        path = Path(file_path).expanduser()
        if not path.exists():
            return f"❌ File not found: {file_path}"
        
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
        
        return f"🗑️ Deleted: {file_path}"
    except Exception as e:
        return f"❌ Failed to delete: {str(e)}"


# ============== System Information ==============

def get_system_info() -> str:
    """Get system information.
    
    Returns:
        System details including OS, CPU, memory, etc.
    """
    try:
        info = []
        info.append(f"💻 **System Information**")
        info.append(f"• OS: {platform.system()} {platform.release()}")
        info.append(f"• Version: {platform.version()}")
        info.append(f"• Machine: {platform.machine()}")
        info.append(f"• Processor: {platform.processor()}")
        info.append(f"• Computer Name: {platform.node()}")
        info.append(f"• User: {os.getlogin()}")
        
        # Try to get more info with psutil if available
        try:
            import psutil
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            info.append(f"\n📊 **Resources:**")
            info.append(f"• CPU Usage: {psutil.cpu_percent()}%")
            info.append(f"• RAM: {memory.used // (1024**3)}GB / {memory.total // (1024**3)}GB ({memory.percent}%)")
            info.append(f"• Disk: {disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB ({disk.percent}%)")
            info.append(f"• Battery: {psutil.sensors_battery().percent if psutil.sensors_battery() else 'N/A'}%")
        except ImportError:
            pass
        
        return "\n".join(info)
    except Exception as e:
        return f"❌ Error getting system info: {str(e)}"


def get_battery_status() -> str:
    """Get battery status.
    
    Returns:
        Battery percentage and charging status
    """
    try:
        import psutil
        battery = psutil.sensors_battery()
        if battery:
            status = "🔌 Charging" if battery.power_plugged else "🔋 On Battery"
            return f"{status}: {battery.percent}%"
        return "❌ No battery detected (desktop PC?)"
    except ImportError:
        return "❌ psutil not installed. Run: pip install psutil"
    except Exception as e:
        return f"❌ Error: {str(e)}"


# ============== Command Execution ==============

def run_command(command: str) -> str:
    """Run a shell command.
    
    Args:
        command: The command to execute
    
    Returns:
        Command output or error message
    """
    # Block dangerous commands
    dangerous = ['format', 'del /s', 'rm -rf', 'shutdown', 'restart', ':(){', 'mkfs']
    if any(d in command.lower() for d in dangerous):
        return "❌ This command is blocked for safety reasons"
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = result.stdout or result.stderr or "Command executed (no output)"
        return f"💻 **Output:**\n```\n{output[:2000]}\n```"
    except subprocess.TimeoutExpired:
        return "❌ Command timed out (30s limit)"
    except Exception as e:
        return f"❌ Error running command: {str(e)}"


# ============== Web Operations ==============

def open_website(url: str) -> str:
    """Open a website in the default browser.
    
    Args:
        url: URL to open (can be without https://)
    
    Returns:
        Status message
    """
    import webbrowser
    
    # Add https if missing
    if not url.startswith(('http://', 'https://')):
        url = f"https://{url}"
    
    try:
        webbrowser.open(url)
        return f"🌐 Opened: {url}"
    except Exception as e:
        return f"❌ Failed to open URL: {str(e)}"


def search_google(query: str) -> str:
    """Search Google for a query.
    
    Args:
        query: Search query
    
    Returns:
        Status message
    """
    import webbrowser
    import urllib.parse
    
    encoded = urllib.parse.quote(query)
    url = f"https://www.google.com/search?q={encoded}"
    
    try:
        webbrowser.open(url)
        return f"🔍 Searching Google for: {query}"
    except Exception as e:
        return f"❌ Failed to search: {str(e)}"


# ============== Clipboard ==============

def copy_to_clipboard(text: str) -> str:
    """Copy text to clipboard.
    
    Args:
        text: Text to copy
    
    Returns:
        Status message
    """
    try:
        import pyperclip
        pyperclip.copy(text)
        return f"📋 Copied to clipboard: {text[:50]}..."
    except ImportError:
        # Fallback using Windows clip command
        try:
            subprocess.run(['clip'], input=text.encode(), check=True)
            return f"📋 Copied to clipboard"
        except:
            return "❌ Could not copy to clipboard"


def get_clipboard() -> str:
    """Get text from clipboard.
    
    Returns:
        Clipboard contents
    """
    try:
        import pyperclip
        content = pyperclip.paste()
        return f"📋 **Clipboard contents:**\n{content[:1000]}"
    except ImportError:
        try:
            result = subprocess.run(['powershell', 'Get-Clipboard'], capture_output=True, text=True)
            return f"📋 **Clipboard contents:**\n{result.stdout[:1000]}"
        except:
            return "❌ Could not read clipboard"


# ============== Volume Control ==============

def set_volume(level: int) -> str:
    """Set system volume level.
    
    Args:
        level: Volume level 0-100
    
    Returns:
        Status message
    """
    level = max(0, min(100, level))
    
    try:
        # Use PowerShell to set volume
        ps_script = f'''
        $obj = New-Object -ComObject WScript.Shell
        1..50 | ForEach-Object {{ $obj.SendKeys([char]174) }}
        1..{level // 2} | ForEach-Object {{ $obj.SendKeys([char]175) }}
        '''
        # Alternative: use nircmd if available, or pycaw
        
        # Simple approach using nircmd syntax via PowerShell
        subprocess.run([
            'powershell', '-Command',
            f'(New-Object -ComObject WScript.Shell).SendKeys([char]173)'  # Mute toggle first
        ], capture_output=True)
        
        return f"🔊 Volume set to approximately {level}%"
    except Exception as e:
        return f"❌ Could not set volume: {str(e)}"


def mute_volume() -> str:
    """Mute/unmute system volume.
    
    Returns:
        Status message
    """
    try:
        subprocess.run([
            'powershell', '-Command',
            '(New-Object -ComObject WScript.Shell).SendKeys([char]173)'
        ], capture_output=True)
        return "🔇 Toggled mute"
    except Exception as e:
        return f"❌ Could not toggle mute: {str(e)}"


# ============== Quick Actions ==============

def lock_screen() -> str:
    """Lock the computer screen.
    
    Returns:
        Status message
    """
    try:
        subprocess.run(['rundll32.exe', 'user32.dll,LockWorkStation'])
        return "🔒 Screen locked"
    except Exception as e:
        return f"❌ Could not lock screen: {str(e)}"


def empty_recycle_bin() -> str:
    """Empty the recycle bin.
    
    Returns:
        Status message
    """
    try:
        subprocess.run([
            'powershell', '-Command',
            'Clear-RecycleBin -Force -ErrorAction SilentlyContinue'
        ], capture_output=True)
        return "🗑️ Recycle bin emptied"
    except Exception as e:
        return f"❌ Could not empty recycle bin: {str(e)}"


def create_text_file(file_path: str, content: str) -> str:
    """Create a text file with content.
    
    Args:
        file_path: Path for the new file
        content: Text content to write
    
    Returns:
        Status message
    """
    try:
        path = Path(file_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        return f"📝 Created file: {path}"
    except Exception as e:
        return f"❌ Failed to create file: {str(e)}"


# ============== File Organization ==============

# File categories with their extensions
FILE_CATEGORIES = {
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico", ".tiff", ".raw"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".m4v"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".h", ".json", ".xml", ".yaml", ".yml", ".md"],
    "Executables": [".exe", ".msi", ".bat", ".cmd", ".ps1"],
    "Fonts": [".ttf", ".otf", ".woff", ".woff2"],
    "eBooks": [".epub", ".mobi", ".azw", ".azw3"],
    "Data": [".sql", ".db", ".sqlite", ".json", ".xml", ".csv"],
}

# Common folder locations
COMMON_FOLDERS = {
    "desktop": Path.home() / "Desktop",
    "downloads": Path.home() / "Downloads",
    "documents": Path.home() / "Documents",
    "pictures": Path.home() / "Pictures",
    "music": Path.home() / "Music",
    "videos": Path.home() / "Videos",
}


def get_file_category(file_extension: str) -> str:
    """Get the category for a file extension."""
    ext = file_extension.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    return "Other"


def organize_files(
    source_folder: str,
    create_in_source: bool = True,
    destination_folder: Optional[str] = None,
    preview_only: bool = False
) -> str:
    """Organize files in a folder by their type/format into categorized subfolders.
    
    Args:
        source_folder: Folder to organize. Can be 'desktop', 'downloads', 'documents', or a full path
        create_in_source: If True, create category folders inside the source folder. If False, use destination_folder
        destination_folder: Optional destination folder when create_in_source is False
        preview_only: If True, just show what would be moved without actually moving
    
    Returns:
        Summary of files organized or to be organized
    """
    try:
        # Resolve source folder
        source_lower = source_folder.lower().strip()
        if source_lower in COMMON_FOLDERS:
            source_path = COMMON_FOLDERS[source_lower]
        else:
            source_path = Path(source_folder).expanduser()
        
        if not source_path.exists():
            return f"❌ Folder not found: {source_folder}"
        
        # Determine destination base
        if create_in_source:
            dest_base = source_path
        elif destination_folder:
            dest_base = Path(destination_folder).expanduser()
        else:
            dest_base = source_path
        
        # Collect files to organize
        files_to_move = {}
        skipped = []
        
        for item in source_path.iterdir():
            # Skip directories and hidden files
            if item.is_dir() or item.name.startswith('.'):
                continue
            
            # Skip if it's already in a category folder
            if item.parent.name in FILE_CATEGORIES:
                continue
            
            category = get_file_category(item.suffix)
            if category not in files_to_move:
                files_to_move[category] = []
            files_to_move[category].append(item)
        
        if not files_to_move:
            return f"📁 No files to organize in {source_path.name}. Folder is already clean!"
        
        # Build summary
        summary = []
        total_moved = 0
        
        if preview_only:
            summary.append(f"📋 **Preview - Files to organize in {source_path.name}:**\n")
        else:
            summary.append(f"📁 **Organizing files in {source_path.name}:**\n")
        
        for category, files in sorted(files_to_move.items()):
            dest_folder = dest_base / category
            
            if preview_only:
                summary.append(f"\n📂 **{category}** ({len(files)} files)")
                for f in files[:5]:  # Show first 5
                    summary.append(f"  • {f.name}")
                if len(files) > 5:
                    summary.append(f"  • ... and {len(files) - 5} more")
            else:
                # Create category folder
                dest_folder.mkdir(exist_ok=True)
                
                moved_count = 0
                for file in files:
                    try:
                        dest_file = dest_folder / file.name
                        # Handle duplicates
                        if dest_file.exists():
                            base = file.stem
                            ext = file.suffix
                            counter = 1
                            while dest_file.exists():
                                dest_file = dest_folder / f"{base}_{counter}{ext}"
                                counter += 1
                        
                        shutil.move(str(file), str(dest_file))
                        moved_count += 1
                        total_moved += 1
                    except Exception as e:
                        skipped.append(f"{file.name}: {str(e)}")
                
                summary.append(f"📂 **{category}**: {moved_count} files moved")
        
        if preview_only:
            summary.append(f"\n💡 Run without preview_only to actually organize these files.")
        else:
            summary.append(f"\n✅ **Total: {total_moved} files organized!**")
            
            if skipped:
                summary.append(f"\n⚠️ Skipped {len(skipped)} files:")
                for s in skipped[:3]:
                    summary.append(f"  • {s}")
        
        return "\n".join(summary)
        
    except Exception as e:
        return f"❌ Error organizing files: {str(e)}"


def preview_organization(source_folder: str) -> str:
    """Preview how files would be organized without moving them.
    
    Args:
        source_folder: Folder to preview. Can be 'desktop', 'downloads', 'documents', or a full path
    
    Returns:
        Preview of file organization
    """
    return organize_files(source_folder, preview_only=True)


def organize_by_date(source_folder: str, preview_only: bool = False) -> str:
    """Organize files by their modification date (Year/Month folders).
    
    Args:
        source_folder: Folder to organize. Can be 'desktop', 'downloads', 'documents', or a full path
        preview_only: If True, just show what would be moved
    
    Returns:
        Summary of organization
    """
    try:
        # Resolve source folder
        source_lower = source_folder.lower().strip()
        if source_lower in COMMON_FOLDERS:
            source_path = COMMON_FOLDERS[source_lower]
        else:
            source_path = Path(source_folder).expanduser()
        
        if not source_path.exists():
            return f"❌ Folder not found: {source_folder}"
        
        # Collect files by date
        files_by_date = {}
        
        for item in source_path.iterdir():
            if item.is_dir() or item.name.startswith('.'):
                continue
            
            # Get modification date
            mtime = datetime.fromtimestamp(item.stat().st_mtime)
            date_folder = f"{mtime.year}/{mtime.strftime('%m - %B')}"
            
            if date_folder not in files_by_date:
                files_by_date[date_folder] = []
            files_by_date[date_folder].append(item)
        
        if not files_by_date:
            return f"📁 No files to organize in {source_path.name}"
        
        summary = []
        total_moved = 0
        
        if preview_only:
            summary.append(f"📋 **Preview - Organize by date in {source_path.name}:**\n")
            for date_folder, files in sorted(files_by_date.items()):
                summary.append(f"📅 **{date_folder}**: {len(files)} files")
            summary.append(f"\n💡 Run with preview_only=False to organize.")
        else:
            summary.append(f"📅 **Organizing by date in {source_path.name}:**\n")
            
            for date_folder, files in sorted(files_by_date.items()):
                dest_folder = source_path / date_folder
                dest_folder.mkdir(parents=True, exist_ok=True)
                
                for file in files:
                    try:
                        dest_file = dest_folder / file.name
                        if dest_file.exists():
                            base, ext = file.stem, file.suffix
                            counter = 1
                            while dest_file.exists():
                                dest_file = dest_folder / f"{base}_{counter}{ext}"
                                counter += 1
                        shutil.move(str(file), str(dest_file))
                        total_moved += 1
                    except:
                        pass
                
                summary.append(f"📅 **{date_folder}**: {len(files)} files")
            
            summary.append(f"\n✅ **Total: {total_moved} files organized by date!**")
        
        return "\n".join(summary)
        
    except Exception as e:
        return f"❌ Error: {str(e)}"


def cleanup_empty_folders(folder_path: str) -> str:
    """Remove empty folders from a directory.
    
    Args:
        folder_path: Folder to clean. Can be 'desktop', 'downloads', 'documents', or a full path
    
    Returns:
        Summary of removed folders
    """
    try:
        folder_lower = folder_path.lower().strip()
        if folder_lower in COMMON_FOLDERS:
            path = COMMON_FOLDERS[folder_lower]
        else:
            path = Path(folder_path).expanduser()
        
        if not path.exists():
            return f"❌ Folder not found: {folder_path}"
        
        removed = []
        
        # Walk bottom-up to remove empty folders
        for dirpath, dirnames, filenames in os.walk(str(path), topdown=False):
            dir_path = Path(dirpath)
            if dir_path == path:
                continue  # Don't remove the root folder
            
            try:
                if not any(dir_path.iterdir()):
                    dir_path.rmdir()
                    removed.append(dir_path.name)
            except:
                pass
        
        if removed:
            return f"🧹 Removed {len(removed)} empty folders:\n" + "\n".join(f"  • {f}" for f in removed[:10])
        else:
            return "✅ No empty folders found"
            
    except Exception as e:
        return f"❌ Error: {str(e)}"


def find_duplicates(folder_path: str) -> str:
    """Find potential duplicate files based on name and size.
    
    Args:
        folder_path: Folder to scan. Can be 'desktop', 'downloads', 'documents', or a full path
    
    Returns:
        List of potential duplicates
    """
    try:
        folder_lower = folder_path.lower().strip()
        if folder_lower in COMMON_FOLDERS:
            path = COMMON_FOLDERS[folder_lower]
        else:
            path = Path(folder_path).expanduser()
        
        if not path.exists():
            return f"❌ Folder not found: {folder_path}"
        
        # Group files by size
        size_groups = {}
        
        for item in path.rglob("*"):
            if item.is_file():
                size = item.stat().st_size
                if size not in size_groups:
                    size_groups[size] = []
                size_groups[size].append(item)
        
        # Find duplicates (same size = potential duplicate)
        duplicates = []
        for size, files in size_groups.items():
            if len(files) > 1 and size > 0:
                duplicates.append((size, files))
        
        if not duplicates:
            return "✅ No potential duplicates found"
        
        summary = [f"🔍 **Potential duplicates in {path.name}:**\n"]
        
        for size, files in sorted(duplicates, key=lambda x: -x[0])[:10]:
            size_str = f"{size / 1024:.1f} KB" if size < 1024*1024 else f"{size / (1024*1024):.1f} MB"
            summary.append(f"\n📄 **Size: {size_str}**")
            for f in files[:5]:
                rel_path = f.relative_to(path) if f.is_relative_to(path) else f.name
                summary.append(f"  • {rel_path}")
        
        summary.append(f"\n💡 Review these files manually to confirm duplicates.")
        return "\n".join(summary)
        
    except Exception as e:
        return f"❌ Error: {str(e)}"


def find_large_files(folder_path: str, min_size_mb: int = 100) -> str:
    """Find large files in a folder.
    
    Args:
        folder_path: Folder to scan. Can be 'desktop', 'downloads', 'documents', or a full path
        min_size_mb: Minimum file size in MB to report (default: 100)
    
    Returns:
        List of large files
    """
    try:
        folder_lower = folder_path.lower().strip()
        if folder_lower in COMMON_FOLDERS:
            path = COMMON_FOLDERS[folder_lower]
        else:
            path = Path(folder_path).expanduser()
        
        if not path.exists():
            return f"❌ Folder not found: {folder_path}"
        
        min_size = min_size_mb * 1024 * 1024
        large_files = []
        
        for item in path.rglob("*"):
            if item.is_file():
                size = item.stat().st_size
                if size >= min_size:
                    large_files.append((size, item))
        
        if not large_files:
            return f"✅ No files larger than {min_size_mb}MB found"
        
        # Sort by size descending
        large_files.sort(key=lambda x: -x[0])
        
        summary = [f"📊 **Large files in {path.name} (>{min_size_mb}MB):**\n"]
        
        total_size = 0
        for size, file in large_files[:15]:
            size_str = f"{size / (1024*1024):.1f} MB" if size < 1024*1024*1024 else f"{size / (1024*1024*1024):.2f} GB"
            rel_path = file.relative_to(path) if file.is_relative_to(path) else file.name
            summary.append(f"• {size_str} - {rel_path}")
            total_size += size
        
        if len(large_files) > 15:
            summary.append(f"• ... and {len(large_files) - 15} more")
        
        total_str = f"{total_size / (1024*1024*1024):.2f} GB"
        summary.append(f"\n📦 **Total: {total_str}** in {len(large_files)} files")
        
        return "\n".join(summary)
        
    except Exception as e:
        return f"❌ Error: {str(e)}"


def get_folder_stats(folder_path: str) -> str:
    """Get statistics about files in a folder.
    
    Args:
        folder_path: Folder to analyze. Can be 'desktop', 'downloads', 'documents', or a full path
    
    Returns:
        Folder statistics including file counts by type
    """
    try:
        folder_lower = folder_path.lower().strip()
        if folder_lower in COMMON_FOLDERS:
            path = COMMON_FOLDERS[folder_lower]
        else:
            path = Path(folder_path).expanduser()
        
        if not path.exists():
            return f"❌ Folder not found: {folder_path}"
        
        # Collect stats
        total_files = 0
        total_size = 0
        by_category = {}
        by_extension = {}
        
        for item in path.rglob("*"):
            if item.is_file():
                total_files += 1
                size = item.stat().st_size
                total_size += size
                
                ext = item.suffix.lower() or "(no extension)"
                category = get_file_category(item.suffix)
                
                if category not in by_category:
                    by_category[category] = {"count": 0, "size": 0}
                by_category[category]["count"] += 1
                by_category[category]["size"] += size
                
                if ext not in by_extension:
                    by_extension[ext] = 0
                by_extension[ext] += 1
        
        # Build summary
        size_str = f"{total_size / (1024*1024):.1f} MB" if total_size < 1024*1024*1024 else f"{total_size / (1024*1024*1024):.2f} GB"
        
        summary = [
            f"📊 **Folder Statistics: {path.name}**\n",
            f"📁 Total files: {total_files}",
            f"💾 Total size: {size_str}\n",
            "**By Category:**"
        ]
        
        for cat, stats in sorted(by_category.items(), key=lambda x: -x[1]["size"]):
            cat_size = f"{stats['size'] / (1024*1024):.1f} MB"
            summary.append(f"• {cat}: {stats['count']} files ({cat_size})")
        
        # Top extensions
        top_ext = sorted(by_extension.items(), key=lambda x: -x[1])[:5]
        summary.append("\n**Top Extensions:**")
        for ext, count in top_ext:
            summary.append(f"• {ext}: {count} files")
        
        return "\n".join(summary)
        
    except Exception as e:
        return f"❌ Error: {str(e)}"


# ============== Reminders & Notes ==============

import json
from datetime import timedelta

NOTES_FILE = Path.home() / ".support_bot_notes.json"
REMINDERS_FILE = Path.home() / ".support_bot_reminders.json"


def load_notes() -> dict:
    """Load notes from file."""
    if NOTES_FILE.exists():
        return json.loads(NOTES_FILE.read_text())
    return {"notes": []}


def save_notes(data: dict):
    """Save notes to file."""
    NOTES_FILE.write_text(json.dumps(data, indent=2))


def create_note(title: str, content: str) -> str:
    """Create a quick note.
    
    Args:
        title: Title of the note
        content: Content of the note
    
    Returns:
        Confirmation message
    """
    try:
        data = load_notes()
        note = {
            "id": len(data["notes"]) + 1,
            "title": title,
            "content": content,
            "created": datetime.now().isoformat(),
        }
        data["notes"].append(note)
        save_notes(data)
        return f"📝 Note created: **{title}**"
    except Exception as e:
        return f"❌ Error creating note: {str(e)}"


def list_notes() -> str:
    """List all saved notes.
    
    Returns:
        List of notes
    """
    try:
        data = load_notes()
        if not data["notes"]:
            return "📝 No notes yet. Create one with 'create a note'!"
        
        result = ["📝 **Your Notes:**\n"]
        for note in data["notes"]:
            created = datetime.fromisoformat(note["created"]).strftime("%b %d, %Y")
            result.append(f"**{note['id']}. {note['title']}** ({created})")
            result.append(f"   {note['content'][:100]}...")
        
        return "\n".join(result)
    except Exception as e:
        return f"❌ Error: {str(e)}"


def delete_note(note_id: int) -> str:
    """Delete a note by ID.
    
    Args:
        note_id: ID of the note to delete
    
    Returns:
        Confirmation message
    """
    try:
        data = load_notes()
        data["notes"] = [n for n in data["notes"] if n["id"] != note_id]
        save_notes(data)
        return f"🗑️ Note {note_id} deleted"
    except Exception as e:
        return f"❌ Error: {str(e)}"


def show_notification(title: str, message: str) -> str:
    """Show a desktop notification/popup.
    
    Args:
        title: Notification title
        message: Notification message
    
    Returns:
        Status message
    """
    try:
        # Use PowerShell to show Windows toast notification
        ps_script = f'''
        [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
        [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null
        $template = "<toast><visual><binding template='ToastText02'><text id='1'>{title}</text><text id='2'>{message}</text></binding></visual></toast>"
        $xml = New-Object Windows.Data.Xml.Dom.XmlDocument
        $xml.LoadXml($template)
        $toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
        [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Support Bot").Show($toast)
        '''
        subprocess.run(['powershell', '-Command', ps_script], capture_output=True)
        return f"🔔 Notification shown: {title}"
    except Exception as e:
        return f"❌ Error showing notification: {str(e)}"


# ============== Network & Connectivity ==============

def get_network_info() -> str:
    """Get network/WiFi information.
    
    Returns:
        Network details including IP, WiFi name, etc.
    """
    try:
        info = ["🌐 **Network Information:**\n"]
        
        # Get IP addresses
        result = subprocess.run(['ipconfig'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        
        for i, line in enumerate(lines):
            if 'IPv4 Address' in line:
                ip = line.split(':')[-1].strip()
                info.append(f"• Local IP: {ip}")
            if 'Default Gateway' in line and line.split(':')[-1].strip():
                gateway = line.split(':')[-1].strip()
                info.append(f"• Gateway: {gateway}")
        
        # Get WiFi name
        wifi_result = subprocess.run(
            ['netsh', 'wlan', 'show', 'interfaces'],
            capture_output=True, text=True
        )
        for line in wifi_result.stdout.split('\n'):
            if 'SSID' in line and 'BSSID' not in line:
                ssid = line.split(':')[-1].strip()
                if ssid:
                    info.append(f"• WiFi Network: {ssid}")
            if 'Signal' in line:
                signal = line.split(':')[-1].strip()
                info.append(f"• Signal Strength: {signal}")
        
        # Get public IP
        try:
            import urllib.request
            public_ip = urllib.request.urlopen('https://api.ipify.org', timeout=5).read().decode()
            info.append(f"• Public IP: {public_ip}")
        except:
            pass
        
        return "\n".join(info)
    except Exception as e:
        return f"❌ Error: {str(e)}"


def test_internet_connection() -> str:
    """Test internet connectivity.
    
    Returns:
        Connection status and speed info
    """
    try:
        import urllib.request
        import time
        
        results = ["🌐 **Internet Connection Test:**\n"]
        
        # Test connectivity
        sites = [
            ("Google", "https://www.google.com"),
            ("Cloudflare", "https://1.1.1.1"),
        ]
        
        for name, url in sites:
            try:
                start = time.time()
                urllib.request.urlopen(url, timeout=5)
                elapsed = (time.time() - start) * 1000
                results.append(f"✅ {name}: {elapsed:.0f}ms")
            except:
                results.append(f"❌ {name}: Failed")
        
        # Ping test
        ping_result = subprocess.run(
            ['ping', '-n', '3', '8.8.8.8'],
            capture_output=True, text=True
        )
        if 'Average' in ping_result.stdout:
            for line in ping_result.stdout.split('\n'):
                if 'Average' in line:
                    results.append(f"📊 Ping: {line.strip()}")
        
        return "\n".join(results)
    except Exception as e:
        return f"❌ Error: {str(e)}"


# ============== Process Management ==============

def get_resource_usage() -> str:
    """Get CPU, memory, and disk usage.
    
    Returns:
        System resource statistics
    """
    try:
        import psutil
        
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        results = ["📊 **Resource Usage:**\n"]
        
        # CPU
        results.append(f"🖥️ **CPU:** {cpu}%")
        
        # Memory
        mem_used = memory.used / (1024**3)
        mem_total = memory.total / (1024**3)
        results.append(f"🧠 **RAM:** {mem_used:.1f}GB / {mem_total:.1f}GB ({memory.percent}%)")
        
        # Disk
        disk_used = disk.used / (1024**3)
        disk_total = disk.total / (1024**3)
        results.append(f"💾 **Disk:** {disk_used:.0f}GB / {disk_total:.0f}GB ({disk.percent}%)")
        
        # Top processes by memory
        results.append("\n**Top Memory Consumers:**")
        processes = []
        for proc in psutil.process_iter(['name', 'memory_percent']):
            try:
                processes.append((proc.info['name'], proc.info['memory_percent']))
            except:
                pass
        
        for name, mem in sorted(processes, key=lambda x: -x[1])[:5]:
            results.append(f"• {name}: {mem:.1f}%")
        
        return "\n".join(results)
    except ImportError:
        return "❌ psutil not installed. Run: pip install psutil"
    except Exception as e:
        return f"❌ Error: {str(e)}"


def kill_process(process_name: str) -> str:
    """Kill an unresponsive process by name.
    
    Args:
        process_name: Name of the process to kill
    
    Returns:
        Status message
    """
    try:
        result = subprocess.run(
            ['taskkill', '/IM', process_name, '/F'],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            return f"✅ Killed process: {process_name}"
        else:
            return f"⚠️ Could not kill {process_name}: {result.stderr}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


# ============== Quick Workflows ==============

def morning_routine() -> str:
    """Execute morning routine - open common apps for starting work.
    
    Returns:
        Status of opened applications
    """
    apps = ["chrome", "outlook", "teams"]
    results = ["☀️ **Morning Routine - Starting work apps:**\n"]
    
    for app in apps:
        try:
            result = open_application(app)
            results.append(f"• {result}")
        except:
            results.append(f"• ⚠️ Could not open {app}")
    
    return "\n".join(results)


def end_of_day() -> str:
    """End of day routine - close work apps and show summary.
    
    Returns:
        Summary and status
    """
    results = ["🌙 **End of Day Routine:**\n"]
    
    # Get battery status
    try:
        import psutil
        battery = psutil.sensors_battery()
        if battery:
            results.append(f"🔋 Battery: {battery.percent}%")
    except:
        pass
    
    # Show notes
    data = load_notes()
    if data["notes"]:
        results.append(f"📝 You have {len(data['notes'])} notes saved")
    
    results.append("\n💡 Consider:")
    results.append("• Closing unused applications")
    results.append("• Emptying recycle bin")
    results.append("• Organizing Downloads folder")
    
    return "\n".join(results)


def quick_cleanup() -> str:
    """Perform quick system cleanup - empty recycle bin, clear temp files.
    
    Returns:
        Cleanup summary
    """
    results = ["🧹 **Quick Cleanup:**\n"]
    
    # Empty recycle bin
    try:
        subprocess.run([
            'powershell', '-Command',
            'Clear-RecycleBin -Force -ErrorAction SilentlyContinue'
        ], capture_output=True)
        results.append("✅ Recycle bin emptied")
    except:
        results.append("⚠️ Could not empty recycle bin")
    
    # Clear temp files
    try:
        temp_path = Path(os.environ.get('TEMP', ''))
        if temp_path.exists():
            count = 0
            for item in temp_path.iterdir():
                try:
                    if item.is_file():
                        item.unlink()
                        count += 1
                    elif item.is_dir():
                        shutil.rmtree(item)
                        count += 1
                except:
                    pass
            results.append(f"✅ Cleared {count} temp items")
    except:
        results.append("⚠️ Could not clear all temp files")
    
    return "\n".join(results)


# ============== Weather ==============

def get_weather(city: str = "auto") -> str:
    """Get current weather information.
    
    Args:
        city: City name or 'auto' for automatic location
    
    Returns:
        Weather information
    """
    try:
        import urllib.request
        import json
        
        # Use wttr.in for simple weather
        url = f"https://wttr.in/{city}?format=j1"
        response = urllib.request.urlopen(url, timeout=10)
        data = json.loads(response.read().decode())
        
        current = data['current_condition'][0]
        location = data['nearest_area'][0]
        
        city_name = location['areaName'][0]['value']
        country = location['country'][0]['value']
        temp_c = current['temp_C']
        feels_like = current['FeelsLikeC']
        desc = current['weatherDesc'][0]['value']
        humidity = current['humidity']
        wind = current['windspeedKmph']
        
        result = [
            f"🌤️ **Weather in {city_name}, {country}:**\n",
            f"🌡️ Temperature: {temp_c}°C (feels like {feels_like}°C)",
            f"☁️ Condition: {desc}",
            f"💧 Humidity: {humidity}%",
            f"💨 Wind: {wind} km/h",
        ]
        
        return "\n".join(result)
    except Exception as e:
        return f"❌ Could not get weather: {str(e)}"


# ============== Timer ==============

def set_timer(minutes: int, message: str = "Timer done!") -> str:
    """Set a timer that shows a notification when done.
    
    Args:
        minutes: Minutes until notification
        message: Message to show when timer ends
    
    Returns:
        Confirmation
    """
    try:
        import threading
        
        def timer_done():
            show_notification("⏰ Timer", message)
        
        timer = threading.Timer(minutes * 60, timer_done)
        timer.daemon = True
        timer.start()
        
        return f"⏰ Timer set for {minutes} minutes. I'll notify you when it's done!"
    except Exception as e:
        return f"❌ Error setting timer: {str(e)}"


# ============== Brightness Control ==============

def set_brightness(level: int) -> str:
    """Set screen brightness level.
    
    Args:
        level: Brightness level 0-100
    
    Returns:
        Status message
    """
    level = max(0, min(100, level))
    try:
        # Use PowerShell WMI to set brightness
        ps_script = f'''
        (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{level})
        '''
        result = subprocess.run(['powershell', '-Command', ps_script], capture_output=True, text=True)
        return f"☀️ Brightness set to {level}%"
    except Exception as e:
        return f"❌ Could not set brightness: {str(e)}"


def get_brightness() -> str:
    """Get current screen brightness.
    
    Returns:
        Current brightness level
    """
    try:
        ps_script = '''
        (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightness).CurrentBrightness
        '''
        result = subprocess.run(['powershell', '-Command', ps_script], capture_output=True, text=True)
        brightness = result.stdout.strip()
        return f"☀️ Current brightness: {brightness}%"
    except Exception as e:
        return f"❌ Could not get brightness: {str(e)}"


# ============== Text Operations ==============

def text_to_speech(text: str) -> str:
    """Read text aloud using text-to-speech.
    
    Args:
        text: Text to speak
    
    Returns:
        Status message
    """
    try:
        ps_script = f'''
        Add-Type -AssemblyName System.Speech
        $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer
        $speak.Speak("{text.replace('"', "'")}")
        '''
        subprocess.Popen(['powershell', '-Command', ps_script])
        return f"🔊 Speaking: {text[:50]}..."
    except Exception as e:
        return f"❌ Error: {str(e)}"


def type_text(text: str) -> str:
    """Type text automatically (simulates keyboard input).
    
    Args:
        text: Text to type
    
    Returns:
        Status message
    """
    try:
        ps_script = f'''
        Add-Type -AssemblyName System.Windows.Forms
        Start-Sleep -Milliseconds 500
        [System.Windows.Forms.SendKeys]::SendWait("{text.replace('{', '{{').replace('}', '}}')}")
        '''
        subprocess.Popen(['powershell', '-Command', ps_script])
        return f"⌨️ Typing text... (switch to target window quickly!)"
    except Exception as e:
        return f"❌ Error: {str(e)}"


# ============== Startup Management ==============

def list_startup_apps() -> str:
    """List applications that run at startup.
    
    Returns:
        List of startup applications
    """
    try:
        results = ["🚀 **Startup Applications:**\n"]
        
        # Check registry startup
        ps_script = '''
        Get-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" | 
        Select-Object -Property * -ExcludeProperty PS* | 
        Format-List
        '''
        result = subprocess.run(['powershell', '-Command', ps_script], capture_output=True, text=True)
        
        # Also check startup folder
        startup_folder = Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"
        if startup_folder.exists():
            for item in startup_folder.iterdir():
                results.append(f"• {item.name}")
        
        if len(results) == 1:
            results.append("No startup applications found in user startup folder")
        
        return "\n".join(results)
    except Exception as e:
        return f"❌ Error: {str(e)}"


# ============== Window Management ==============

def minimize_all_windows() -> str:
    """Minimize all windows (show desktop).
    
    Returns:
        Status message
    """
    try:
        ps_script = '''
        (New-Object -ComObject Shell.Application).MinimizeAll()
        '''
        subprocess.run(['powershell', '-Command', ps_script], capture_output=True)
        return "🪟 All windows minimized"
    except Exception as e:
        return f"❌ Error: {str(e)}"


def restore_all_windows() -> str:
    """Restore all minimized windows.
    
    Returns:
        Status message
    """
    try:
        ps_script = '''
        (New-Object -ComObject Shell.Application).UndoMinimizeAll()
        '''
        subprocess.run(['powershell', '-Command', ps_script], capture_output=True)
        return "🪟 All windows restored"
    except Exception as e:
        return f"❌ Error: {str(e)}"
