"""
Local Bot Runner - Run on your laptop and access from any device
"""
import os
import socket
import webbrowser
from dotenv import load_dotenv

load_dotenv()

def get_local_ip():
    """Get local IP address for network access"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def main():
    local_ip = get_local_ip()
    port = int(os.getenv("PORT", "8000"))
    
    print("\n" + "="*60)
    print("🤖 SUPPORT BOT - Local Server")
    print("="*60)
    print(f"\n📱 Access from ANY device on your network:\n")
    print(f"   Laptop:  http://localhost:{port}")
    print(f"   Mobile:  http://{local_ip}:{port}")
    print(f"\n   Web UI:  http://{local_ip}:{port}/ui")
    print("\n" + "="*60)
    print("Press Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    # Open browser automatically
    webbrowser.open(f"http://localhost:{port}/ui")
    
    # Start the server
    import uvicorn
    uvicorn.run(
        "server:app",
        host="0.0.0.0",  # Allow network access
        port=port,
        reload=False
    )

if __name__ == "__main__":
    main()
