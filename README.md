# OBS-Scene-Controller
The OBS Scene Controller is a powerful tool developed by Ritesh Verma to streamline OBS scene management and screen casting for content creators. It integrates a PySide6 GUI, Flask web server, and MSS-based screen capture for a seamless live production experience. All Cloudflare tunnel URLs are automatically copied to the clipboard for easy access.

# Know about OBS scene control(Source code, Executable, Scientific paper): https://imimi328.github.io/OBS-Scene-Controller/

<html>
  <body>
      <section id="tutorial" className="section">
        <h2 className="text-3xl font-bold text-green-400 mb-6 text-center">Tutorial</h2>
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h3 className="text-xl font-semibold text-green-400 mb-4">Getting Started with OBS Scene Controller</h3>
          <ol className="list-decimal list-inside text-gray-300 space-y-4">
            <li>
              <strong>Install Dependencies</strong>: Ensure Python 3.8+ is installed. Install required libraries:
              <pre className="bg-gray-900 p-2 rounded mt-2">pip install PySide6 flask obswebsocket keyboard pyperclip mss Pillow</pre>
            </li>
            <li>
              <strong>Install Cloudflared</strong>: Download and install <a href="https://www.cloudflare.com/products/tunnel/" className="text-green-400 hover:underline">Cloudflared</a> for secure tunneling.
            </li>
            <li>
              <strong>Run the Casting Script</strong>: Save the casting script as <code>caster.py</code> and run it:
              <pre className="bg-gray-900 p-2 rounded mt-2">python caster.py</pre>
              The Cloudflare tunnel URL will be automatically copied to your clipboard.
            </li>
            <li>
              <strong>Run the Main Script</strong>: Save the main script as <code>obs_controller.py</code> and run it:
              <pre className="bg-gray-900 p-2 rounded mt-2">python obs_controller.py</pre>
              Enter your OBS WebSocket IP (default: localhost) and password when prompted. The main script's tunnel URL will also be copied to your clipboard.
            </li>
            <li>
              <strong>Configure Scenes</strong>:
              <ul className="list-disc list-inside ml-4">
                <li>Add normal scenes with a name, hotkey (e.g., <code>ctrl+f9</code>), and the tunnel URL from the casting script (available in your clipboard).</li>
                <li>Add temporary scenes with a name, hotkey, thumbnail image path, and duration (in seconds).</li>
                <li>Use the Edit and Delete buttons to modify or remove scenes.</li>
              </ul>
            </li>
            <li>
              <strong>Access the Web Interface</strong>: Open the main script's Cloudflare tunnel URL (copied to your clipboard and displayed in the GUI) in a browser to switch scenes remotely. Normal scenes display live thumbnails, while temporary scenes use static thumbnails.
            </li>
            <li>
              <strong>Use Hotkeys</strong>: Press assigned hotkeys to switch scenes instantly or trigger temporary scenes.
            </li>
          </ol>
          <p className="text-gray-300 mt-4">For the executable, run <code>OBS.exe</code> and ensure <code>logo.png</code> and <code>cloudflared</code> are in the same directory. Tunnel URLs are automatically copied to the clipboard for ease of use.</p>
        </div>
      </section>
    );
      <section id="about" className="section">
        <h2 className="text-3xl font-bold text-green-400 mb-6 text-center">About</h2>
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h3 className="text-xl font-semibold text-green-400 mb-2">Overview</h3>
          <p className="text-gray-300 mb-4">The OBS Scene Controller is a powerful tool developed by Ritesh Verma to streamline OBS scene management and screen casting for content creators. It integrates a PySide6 GUI, Flask web server, and MSS-based screen capture for a seamless live production experience. All Cloudflare tunnel URLs are automatically copied to the clipboard for easy access.</p>
          <h3 className="text-xl font-semibold text-green-400 mb-2">System Requirements</h3>
          <ul className="list-disc list-inside text-gray-300 mb-4">
            <li>Operating System: Windows, macOS, or Linux</li>
            <li>Python: 3.8 or higher (for source code)</li>
            <li>Dependencies: PySide6, Flask, obswebsocket, keyboard, pyperclip, MSS, Pillow</li>
            <li>Cloudflared: Required for tunneling</li>
            <li>OBS Studio: Version 27.0 or higher with WebSocket enabled</li>
          </ul>
          <h3 className="text-xl font-semibold text-green-400 mb-2">Technical Details</h3>
          <p className="text-gray-300 mb-4">The application uses:
            <ul className="list-disc list-inside">
              <li><strong>PySide6</strong> for the GUI, providing a modern interface for scene management.</li>
              <li><strong>Flask</strong> for the web server, enabling remote control via a browser.</li>
              <li><strong>OBS WebSocket</strong> for seamless integration with OBS Studio.</li>
              <li><strong>MSS and Pillow</strong> for efficient screen capture and thumbnail generation.</li>
              <li><strong>Cloudflare Tunnel</strong> for secure, public access to the web interface and live streams, with URLs automatically copied to the clipboard.</li>
            </ul>
          </p>
          <h3 className="text-xl font-semibold text-green-400 mb-2">Scientific Paper</h3>
          <p className="text-gray-300 mb-4">A detailed scientific paper describing the system's design and performance is available in the <a href="#download" className="text-green-400 hover:underline">Download</a> section.</p>
          <h3 className="text-xl font-semibold text-green-400 mb-2">License</h3>
          <p className="text-gray-300">All rights reserved to Team Emogi. The source code is available under a permissive license for commercial use.</p>
        </div>
      </section>
</body>
</html>

Acknowledgments

  
    Developed by Ritesh Verma.
    Special thanks to Team Emogi for support and testing.
    Built with open-source libraries: PySide6, Flask, obswebsocket, MSS, Pillow, and pyperclip.
  
