# OBS-Scene-Controller
The OBS Scene Controller is a powerful tool developed by Ritesh Verma to streamline OBS scene management and screen casting for content creators. It integrates a PySide6 GUI, Flask web server, and MSS-based screen capture for a seamless live production experience. All Cloudflare tunnel URLs are automatically copied to the clipboard for easy access.

OBS Scene Controller



  A powerful, user-friendly tool for managing OBS Studio scenes with real-time previews and remote control, developed by Ritesh Verma. This application integrates a PySide6-based GUI, a Flask web server, and a screen-casting module, all secured via Cloudflare tunnels. Ideal for content creators, live streamers, and video production professionals.


Table of Contents

  Features
  System Requirements
  Installation
  Usage
  Building the Executable
  Scientific Paper
  Website
  License
  Acknowledgments


Features

  
    Scene Management: Add, edit, and delete normal and temporary scenes via a modern PySide6 GUI.
    Real-Time Previews: Stream live thumbnails using MSS and Pillow, accessible via Cloudflare tunnels.
    Remote Control: Switch scenes remotely through a Flask-based web interface.
    Hotkey Support: Assign custom hotkeys for instant scene switching and temporary scene triggers.
    Temporary Scenes: Configure scenes with durations for automatic reversion, perfect for overlays.
    Automatic Clipboard Copying: Cloudflare tunnel URLs for both the main application and casting script are automatically copied to the clipboard.
    Cross-Platform: Compatible with Windows, macOS, and Linux.
  


System Requirements

  
    Operating System: Windows, macOS, or Linux
    Python: 3.8 or higher (for source code)
    Dependencies:
      
        PySide6
        Flask
        obswebsocket
        keyboard
        pyperclip
        MSS
        Pillow
      
    
    Cloudflared: Required for secure tunneling (download here)
    OBS Studio: Version 27.0 or higher with WebSocket plugin enabled
    Icon File: logo.ico (included in the repository for GUI and executable)
  


Installation

  
    
      Clone the Repository:
      git clone https://github.com/riteshverma/obs-scene-controller.git
cd obs-scene-controller
    
    
      Install Dependencies:
      pip install PySide6 flask obswebsocket keyboard pyperclip mss Pillow
    
    
      Install Cloudflared:
      Download and install Cloudflared for your operating system. Ensure cloudflared is in your system’s PATH or placed in the project directory.
    
    
      Prepare the Icon:
      Ensure logo.ico is in the project directory for the GUI and executable.
    
  


Usage

  The project consists of two scripts: obs_controller.py (main application) and caster.py (screen-casting module).

  Running the Casting Script
  
    Run the casting script to generate live thumbnails:
      python caster.py
    
    The Cloudflare tunnel URL will be automatically copied to your clipboard and displayed in the terminal.
  

  Running the Main Script
  
    Run the main script:
      python obs_controller.py
    
    Enter your OBS WebSocket IP (default: localhost) and password when prompted.
    The main script’s Cloudflare tunnel URL will be automatically copied to your clipboard and shown in the GUI.
  

  Configuring Scenes
  
    Normal Scenes:
      
        In the GUI, enter a scene name, hotkey (e.g., ctrl+f9), and the tunnel URL from caster.py (paste from clipboard).
        Click "Add Normal Scene" to save.
      
    
    Temporary Scenes:
      
        Enter a scene name, hotkey, thumbnail image path, and duration (in seconds).
        Click "Add Temporary Scene" to save.
      
    
    Use the "Edit" and "Delete" buttons to modify or remove scenes.
    Scene configurations are saved to controller_scenes.json and temporary_scenes.json.
  

  Accessing the Web Interface
  
    Open the main script’s Cloudflare tunnel URL (copied to clipboard and displayed in the GUI) in a browser.
    Normal scenes display live thumbnails from the casting script; temporary scenes use static thumbnails.
    Click "Switch" for normal scenes or "Trigger Temporary" for temporary scenes.
  

  Using Hotkeys
  
    Press assigned hotkeys to switch scenes instantly or trigger temporary scenes, which revert after the specified duration.
  

  Using the Executable
  
    Download the pre-built OBS.exe from the Releases page.
    Ensure logo.ico and cloudflared.exe are in the same directory as OBS.exe.
    Run OBS.exe and follow the same configuration steps as above.
  


Building the Executable

  To build the executable yourself:
  
    Ensure logo.ico is in the project directory.
    Run the following PyInstaller command:
      pyinstaller --onefile --windowed --icon=logo.ico --add-data "logo.ico;." --exclude-module PyQt5 obs_controller.py
    
    For the casting script:
      pyinstaller --onefile --icon=logo.ico --add-data "logo.ico;." --exclude-module PyQt5 caster.py
    
    Find the executables in the dist folder.
  
  Note: Include cloudflared.exe in the executable’s directory if not installed system-wide.


Scientific Paper

  A detailed scientific paper describing the design, implementation, and performance of the OBS Scene Controller is available:
  
    Download the Paper
  


Website

  Visit the official website for a user-friendly interface to download the source code, executable, and paper, along with a comprehensive tutorial:
  
    OBS Scene Controller Website
  


License

  All rights reserved to Team Emogi. The source code is available under a permissive license for non-commercial use. Contact the author (Ritesh Verma) at ritesh@example.com for commercial licensing inquiries.


Acknowledgments

  
    Developed by Ritesh Verma.
    Special thanks to Team Emogi for support and testing.
    Built with open-source libraries: PySide6, Flask, obswebsocket, MSS, Pillow, and pyperclip.
  
