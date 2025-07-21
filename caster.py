import io
import threading
import time
import subprocess
import re
import pyperclip
from flask import Flask, Response
from PIL import Image
import mss
import sys
import os

# ----------------- Settings -------------------
JPEG_QUALITY = 35        # Lower value = more compression
SCALE_FACTOR = 0.4       # Downscale factor (0.4 = 40% of original)
FRAME_DELAY = 0.2        # Seconds delay between frames (~5 FPS)
PORT = 5000
# ----------------------------------------------

app = Flask(__name__)

def generate_frames():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        while True:
            screenshot = sct.grab(monitor)
            img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
            img = img.resize((320, 180))  # Downscale to thumbnail size

            buf = io.BytesIO()
            img.save(buf, format='JPEG', quality=40)  # Reduce JPEG quality too
            frame_bytes = buf.getvalue()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            time.sleep(0.1)  # Reduce frame rate slightly if needed


@app.route('/')
def index():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def run_flask():
    app.run(host='0.0.0.0', port=5001, debug=False, use_reloader=False)

def start_cloudflare_tunnel():
    print("[Tunnel] Starting Cloudflare tunnel silently...")

    flags = 0
    if sys.platform == 'win32':
        flags = subprocess.CREATE_NO_WINDOW

    process = subprocess.Popen(
        ['cloudflared', 'tunnel', '--url', f'http://localhost:5001'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        creationflags=flags,
        text=True
    )

    for line in process.stdout:
        match = re.search(r'(https://[a-zA-Z0-9.-]+\.trycloudflare\.com)', line)
        if match:
            public_url = match.group(1)
            pyperclip.copy(public_url)
            print(f"[Tunnel URL] Copied to clipboard: {public_url}")
            break

if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
    time.sleep(2)
    start_cloudflare_tunnel()

    print("[Stream] Running permanently.")

    while True:
        time.sleep(1)
