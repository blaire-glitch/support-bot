"""
Support Bot Installer
Creates desktop shortcut and sets up the application.
"""

import os
import sys
import subprocess
from pathlib import Path

def create_desktop_shortcut():
    """Create a desktop shortcut for Windows."""
    
    app_dir = Path(__file__).parent.resolve()
    desktop = Path.home() / "Desktop"
    shortcut_path = desktop / "Support Bot.lnk"
    
    # PowerShell script to create shortcut
    ps_script = f'''
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
$Shortcut.TargetPath = "pythonw.exe"
$Shortcut.Arguments = '"{app_dir / "desktop_app.py"}"'
$Shortcut.WorkingDirectory = "{app_dir}"
$Shortcut.IconLocation = "shell32.dll,172"
$Shortcut.Description = "Support Bot - Your AI Assistant"
$Shortcut.Save()
'''
    
    try:
        subprocess.run(["powershell", "-Command", ps_script], check=True)
        print(f"✅ Desktop shortcut created: {shortcut_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to create shortcut: {e}")
        return False


def create_start_menu_entry():
    """Create a Start Menu entry."""
    
    app_dir = Path(__file__).parent.resolve()
    start_menu = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs"
    shortcut_path = start_menu / "Support Bot.lnk"
    
    ps_script = f'''
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
$Shortcut.TargetPath = "pythonw.exe"
$Shortcut.Arguments = '"{app_dir / "desktop_app.py"}"'
$Shortcut.WorkingDirectory = "{app_dir}"
$Shortcut.IconLocation = "shell32.dll,172"
$Shortcut.Description = "Support Bot - Your AI Assistant"
$Shortcut.Save()
'''
    
    try:
        subprocess.run(["powershell", "-Command", ps_script], check=True)
        print(f"✅ Start Menu entry created")
        return True
    except Exception as e:
        print(f"❌ Failed to create Start Menu entry: {e}")
        return False


def install_dependencies():
    """Install required Python packages."""
    print("\n📦 Installing dependencies...")
    
    requirements = [
        "agent-framework-azure-ai",
        "python-dotenv",
        "pydantic",
        "httpx",
    ]
    
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--pre", "-q"] + requirements,
            check=True
        )
        print("✅ Dependencies installed")
        return True
    except Exception as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def create_batch_launcher():
    """Create a .bat file for easy launching."""
    
    app_dir = Path(__file__).parent.resolve()
    bat_path = app_dir / "Start Support Bot.bat"
    
    bat_content = f'''@echo off
cd /d "{app_dir}"
start "" pythonw desktop_app.py
'''
    
    try:
        bat_path.write_text(bat_content)
        print(f"✅ Batch launcher created: {bat_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to create batch launcher: {e}")
        return False


def main():
    """Run the installer."""
    print("\n" + "="*50)
    print("🤖 SUPPORT BOT INSTALLER")
    print("="*50)
    
    print("\n📁 App Location:", Path(__file__).parent.resolve())
    
    # Install dependencies
    install_dependencies()
    
    # Create launchers
    print("\n🔧 Creating launchers...")
    create_batch_launcher()
    create_desktop_shortcut()
    create_start_menu_entry()
    
    print("\n" + "="*50)
    print("✅ INSTALLATION COMPLETE!")
    print("="*50)
    print("\nYou can now:")
    print("  1. Double-click 'Support Bot' on your Desktop")
    print("  2. Search 'Support Bot' in Start Menu")
    print("  3. Double-click 'Start Support Bot.bat' in this folder")
    print("\nThe bot will appear as a floating avatar in the corner!")
    print("="*50 + "\n")
    
    # Ask to launch now
    response = input("Launch Support Bot now? (y/n): ").strip().lower()
    if response == 'y':
        print("\n🚀 Launching Support Bot...")
        subprocess.Popen(
            ["pythonw", str(Path(__file__).parent / "desktop_app.py")],
            cwd=Path(__file__).parent
        )
        print("✅ Bot launched! Look for the 🤖 avatar on your screen.")


if __name__ == "__main__":
    main()
